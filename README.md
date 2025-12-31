
![Animated_Logo_GIF_Creation-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2a0bb698-bec4-4501-899e-fd4ab842d132)

**The high-performance, drift-ready boilerplate for FastAPI.**

Hatchback is a powerful CLI tool designed to bootstrap and manage production-ready FastAPI applications. It comes pre-loaded with best practices, security hardening, and a modular architecture that scales.

## ✨ Features

- **🚀 Production Ready**: SQLAlchemy 2.0, Pydantic v2, and Alembic pre-configured.
- **🛡️ Secure by Default**: Rate limiting (SlowAPI), hardened Auth (JWT), secure secret generation, and non-root Docker containers.
- **⚡ Blazing Fast**: Optional `uv` support for lightning-fast dependency management.
- **🏗️ Clean Architecture**: Service-Repository pattern for maintainable code.
- **✅ Testing Ready**: Integrated `pytest` setup with `hatchback test`.
- **🐳 Dockerized**: Ready-to-deploy `docker-compose` setup with healthchecks.
- **🏎️ Drift Mode**: A CLI that drives as good as it looks.

## 📦 Installation

```bash
pip install hatchback
```

## 🏁 Quick Start

### 1. Initialize a new project

```bash
hatchback init my_project_name
```

You will be prompted for:

- Database Name
- Docker inclusion
- **`uv` usage** (if installed, for faster setup)

**Options:**

- `--use-uv`: Force usage of `uv` for virtualenv creation.
- `--no-docker`: Skip Docker file generation.

### 2. Start the Engine

Before hitting the gas, ensure your database is running and the schema is initialized.

**1. Start Database:**

```bash
cd my_project_name
docker-compose up -d db
```

*(Or configure a local Postgres instance in `.env`)*

**2. Initialize Database:**
Create and apply the first migration for the built-in models (User, Tenant).

```bash
hatchback migrate create -m "initial_setup"
hatchback migrate apply
```

**3. Run Server:**
Start the development server with hot-reloading.

```bash
hatchback run
```

🎉 **Success!** Your API is now live.

- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Scaffold Resources

Don't write boilerplate. Generate Models, Schemas, Repositories, Services, and Routes in one go.
Hatchback automatically registers your new routes and services, so they are ready to use immediately.

```bash
hatchback make Product
```

### 4. Manage Migrations

Wrapper around Alembic to keep your database in sync.

```bash
# Create a migration
hatchback migrate create -m "add products table"

# Apply migrations
hatchback migrate apply
```

# 5. Seed Data

Populate your database with initial data (default tenant and admin user).

```bash
hatchback seed
```

## 🏗️ Architecture Explained

Hatchback follows a **Service-Repository** pattern to keep your code modular and testable.

1. **Routes (`app/routes/`)**: Handle HTTP requests/responses and dependency injection. They delegate business logic to Services.
2. **Services (`app/services/`)**: Contain the business logic. They orchestrate data operations using Repositories.
3. **Repositories (`app/repositories/`)**: Handle direct database interactions (CRUD). They abstract the SQL/ORM details from the rest of the app.
4. **Models (`app/models/`)**: SQLAlchemy database definitions.
   hatchback test

# Run with coverage (pass arguments to pytest)

hatchback test --
Hatchback projects come with `pytest` configured.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## 📂 Project Structure

```
my_project/
├── app/
│   ├── config/       # Database, Security, Limiter config
│   ├── models/       # SQLAlchemy Database Models
│   ├── schemas/      # Pydantic Data Schemas
│   ├── repositories/ # Data Access Layer (CRUD)
│   ├── services/     # Business Logic
│   ├── routes/       # API Endpoints
│   ├── dependencies.py
│   └── main.py
├── alembic/          # Database Migrations
├── tests/            # Pytest Suite
├── docker-compose.yml
└── requirements.txt
```

## 🛡️ Security Features

- **Rate Limiting**: Built-in protection against brute-force attacks.
- **Secure Headers**: Trusted host middleware configuration.
- **Password Hashing**: Argon2/Bcrypt support via Passlib.
- **Docker Security**: Runs as a non-root user to prevent container breakout.

---

*Built with 💖 and 🏎️ by Ignacio Bares(nachovoss) and the Hatchback Team.*
