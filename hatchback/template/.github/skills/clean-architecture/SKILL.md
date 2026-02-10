---
name: clean-architecture
description: >
  Guide for following clean architecture patterns in this FastAPI project.
  Use this skill when creating new features, adding endpoints, writing services,
  or modifying the data layer. Ensures consistent layered separation.
---

# Clean Architecture Skill

This project enforces a strict **layered architecture**. Every feature must be split
across four layers, each with a single responsibility. Never skip a layer.

## The Four Layers

```
Route  →  Service  →  Repository  →  Model
(HTTP)    (Logic)     (Data Access)   (ORM)
```

| Layer | Directory | Responsibility | Depends On |
|---|---|---|---|
| **Model** | `app/models/` | Define database tables, columns, relationships | Nothing |
| **Repository** | `app/repositories/` | Query the database, extend `BaseRepository` | Model |
| **Service** | `app/services/` | Business logic, validation, orchestration | Repository |
| **Route** | `app/routes/` | HTTP interface, request/response handling | Service |
| **Schema** | `app/schemas/` | Pydantic models for input validation and serialization | Nothing |

## Rules

### 1. Routes must be thin

Routes only handle HTTP concerns — parse input, call a service, return a response.
**No business logic in routes.** No direct database queries.

```python
# ✅ CORRECT — route delegates to service
@router.post("/", response_model=ProductResponse)
def create(item: ProductCreate, service: ProductService = Depends(get_service)):
    return service.create(item.model_dump())

# ❌ WRONG — route contains business logic and DB access
@router.post("/")
def create(item: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**item.model_dump())
    db.add(product)
    db.commit()
    return product
```

### 2. Services own business logic

Services orchestrate repositories, apply rules, and raise HTTP exceptions when needed.
A service receives a `db: Session` in its constructor and creates its own repository.

```python
class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def create(self, data: dict):
        # Business rule: validate, transform, then persist
        return self.repo.create(data)

    def get(self, id: UUID):
        return self.repo.get_by_id(id)
```

Services may depend on **other services** (e.g. `AuthService` uses `UserService`),
but never on routes.

### 3. Repositories handle data access only

Every repository extends `BaseRepository` which provides standard CRUD:
- `get_all()` — list all records
- `get_by_id(id)` — find by primary key
- `create(obj)` — insert and commit
- `update(id, data)` — partial update and commit
- `delete(id)` — remove and commit

Add custom query methods as needed:

```python
class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)

    def get_by_email(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_all_by_tenant(self, tenant_id: UUID, skip=0, limit=100):
        return (
            self.db.query(self.model)
            .filter(self.model.tenant_id == tenant_id)
            .offset(skip).limit(limit).all()
        )
```

**No business logic in repositories.** They only translate method calls into SQL.

### 4. Models define the database schema

Models use SQLAlchemy declarative base from `app/config/database.py`:

```python
class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    name = Column(String(100), nullable=True)
```

Conventions:
- Table names are **plural** snake_case (`products`, `blog_posts`)
- Primary keys are always **UUID**
- Always include `created_at`

### 5. Schemas validate and serialize

Use Pydantic v2 with three schema classes per resource:

```python
class ProductBase(BaseModel):
    name: Optional[str] = None

class ProductCreate(ProductBase):
    pass  # Add required fields

class ProductUpdate(ProductBase):
    pass  # All fields optional

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

Key rules:
- Use `model_dump()` (Pydantic v2), never `.dict()`
- Use `model_dump(exclude_unset=True)` for partial updates
- `Response` schemas must have `model_config = ConfigDict(from_attributes=True)`

## Dependency Injection

Routes inject services using FastAPI's `Depends()`:

```python
def get_service(db: Session = Depends(get_db)):
    return ProductService(db)

@router.get("/")
def list_all(service: ProductService = Depends(get_service)):
    return service.get_all()
```

For auth-protected routes, use dependencies from `app/dependencies.py`:
- `get_current_user` — any authenticated user
- `get_current_active_user` — active users only
- `RoleChecker(["admin"])` — role-based check

## Registering a New Resource

After creating all layer files, register them in the `__init__.py` files:

1. **`app/models/__init__.py`** — import the model
2. **`app/routes/__init__.py`** — import router, add to `routers` list
3. **`app/services/__init__.py`** — import service, add to `__all__`
4. **`app/repositories/__init__.py`** — import repo, add to `__all__`

Or simply run `hbk make <resource>` which does all of this automatically.

## Testing Pattern

Each resource gets a test file in `tests/` with CRUD test functions:

```python
def test_create_product(client, db_session):
    payload = {"name": "Widget"}
    response = client.post("/products/", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"

def test_read_products(client, db_session):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Tests use fixtures from `tests/conftest.py` for `client` and `db_session`.
