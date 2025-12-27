# Hatchback CLI

A powerful CLI tool to bootstrap and manage production-ready FastAPI applications with Alembic, SQLAlchemy, and Docker.

## Installation

```bash
pip install hatchback
```

## Usage

### 1. Initialize a new project

Create a new FastAPI project with a robust directory structure, pre-configured database connection, and authentication.

```bash
hatchback init my_project
```

This will:
- Create a new directory `my_project`
- Set up the project structure (models, schemas, repositories, services, routes)
- Optionally create a virtual environment and install dependencies
- Optionally include Docker and Docker Compose files

### 2. Run the development server

Start the Uvicorn server with hot-reloading enabled.

```bash
cd my_project
hatchback run
```
*Options:*
- `--port`: Port to run on (default: 8000)
- `--host`: Host to run on (default: 127.0.0.1)

### 3. Manage Database Migrations

Simplify Alembic migration commands.

**Create a new migration:**
Automatically generates a migration file with a sequential prefix (e.g., `1_initial.py`) to keep files ordered.

```bash
hatchback migrate create -m "initial_schema"
```

**Apply migrations:**
Upgrades the database to the latest head.

```bash
hatchback migrate apply
```

### 4. Scaffold New Resources

Generate all necessary files for a new resource (Model, Schema, Repository, Service, Route) in one command.

```bash
hatchback make item
```

This will create:
- `app/models/item.py`
- `app/schemas/item.py`
- `app/repositories/item.py`
- `app/services/item.py`
- `app/routes/item.py`
- And update `app/models/__init__.py`

## Project Structure

The generated project follows a clean architecture pattern:

```
app/
  config/       # Database and app configuration
  models/       # SQLAlchemy models
  schemas/      # Pydantic schemas
  repositories/ # Data access layer
  services/     # Business logic
  routes/       # API endpoints
  dependencies.py
  main.py
alembic/        # Migration scripts
tests/          # Pytest tests
```
