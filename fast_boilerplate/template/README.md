# FastAPI Alembic Boilerplate

This is a boilerplate project for FastAPI with Alembic and SQLAlchemy, featuring a multi-tenant architecture with User and Tenant models.

## Features

- **FastAPI**: Modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: The Python SQL Toolkit and Object Relational Mapper.
- **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- **Multi-tenancy**: Built-in support for multi-tenant architecture.
- **Authentication**: JWT-based authentication.
- **Repository Pattern**: Clean architecture using the repository pattern.

## Setup

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file in the root directory (copy from `.env.example` if available) and configure your database connection.
    ```env
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=boilerplate_db
    SECRET_KEY=your_secret_key
    ```

4.  **Database Migrations**:
    ```bash
    # Create a new migration
    alembic revision --autogenerate -m "Initial migration"

    # Apply migrations
    alembic upgrade head
    ```

5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Project Structure

```
fastapi-alembic-boilerplate/
├── alembic/                # Alembic migration scripts
├── app/
│   ├── config/             # Configuration files
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── routes/             # API endpoints
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── dependencies.py     # Dependency injection
│   └── main.py             # Application entry point
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```
