
![Animated_Logo_GIF_Creation-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2a0bb698-bec4-4501-899e-fd4ab842d132)

**The high-performance, drift-ready boilerplate for FastAPI.**

Hatchback is a powerful CLI tool designed to bootstrap and manage production-ready FastAPI applications. It comes pre-loaded with best practices, security hardening, and a modular architecture that scales.

## ✨ Features

- **🚀 Production Ready**: SQLAlchemy 2.0, Pydantic v2, and Alembic pre-configured.
- **🛡️ Secure by Default**: Rate limiting (SlowAPI), hardened Auth (JWT), secure secret generation, and non-root Docker containers.
- **⚡ Blazing Fast**: Optional `uv` support for lightning-fast dependency management.
- **🏗️ Clean Architecture**: Service-Repository pattern for maintainable code.
- **✅ Testing Ready**: Integrated `pytest` setup with `hbk test`.
- **🐳 Dockerized**: Ready-to-deploy `docker-compose` setup with healthchecks.
- **🤖 AI-Powered**: Built-in Agent Skills for GitHub Copilot and VS Code agent mode.
- **🏎️ Drift Mode**: A CLI that drives as good as it looks.

## 📦 Installation

```bash
pip install hatchback
```

> **Tip:** Use `hbk` as a shortcut for `hatchback` — all commands work with either.
> For example, `hbk make product` is equivalent to `hatchback make product`.

## 🏁 Quick Start

### 1. Initialize a new project

```bash
hbk init my_project_name
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
hbk migrate create -m "initial_setup"
hbk migrate apply
```

**3. Run Server:**
Start the development server with hot-reloading.

```bash
hbk run
```

🎉 **Success!** Your API is now live.

- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Scaffold Resources

Don't write boilerplate. Generate Models, Schemas, Repositories, Services, and Routes in one go.
Hatchback automatically registers your new routes and services, so they are ready to use immediately.

```bash
hbk make product
```

### 4. Remove Resources

Changed your mind? Remove a scaffolded resource and clean up all imports automatically.

```bash
hbk remove product          # asks for confirmation
hbk remove product --force  # skips confirmation
```

### 5. Manage Migrations

Wrapper around Alembic to keep your database in sync.

```bash
# Create a migration
hbk migrate create -m "add products table"

# Apply migrations
hbk migrate apply

# Rollback the last migration
hbk migrate downgrade

# Rollback multiple steps
hbk migrate downgrade -r -2

# Rollback everything
hbk migrate downgrade -r base
```

### 6. Seed Data

Populate your database with initial data (default tenant and admin user).

```bash
hbk seed
```

### 7. Import Existing Database

Have an existing database? Hatchback can inspect it and generate your entire project architecture automatically.

```bash
# Output models only to a file
hbk inspect --url postgresql://user:pass@localhost:5432/mydb --output app/models/legacy.py

# Full Scaffold Mode (Recommended)
# Generates Models, Services, Repositories, Schemas, and Routes for every table
hbk inspect --scaffold --url postgresql://user:pass@localhost:5432/mydb
```

### 8. Upgrade Existing Projects

After upgrading Hatchback, sync the latest agent skills and infrastructure files into your project.

```bash
pip install --upgrade hatchback
hbk upgrade
```

This syncs new files (like agent skills) without touching your Docker config, user code, or environment files.

### 9. Run Tests

Hatchback projects come with `pytest` configured.

```bash
hbk test
```

## 🏗️ Architecture Explained

Hatchback follows a **Service-Repository** pattern to keep your code modular and testable.

1. **Routes (`app/routes/`)**: Handle HTTP requests/responses and dependency injection. They delegate business logic to Services.
2. **Services (`app/services/`)**: Contain the business logic. They orchestrate data operations using Repositories.
3. **Repositories (`app/repositories/`)**: Handle direct database interactions (CRUD). They abstract the SQL/ORM details from the rest of the app.
4. **Models (`app/models/`)**: SQLAlchemy database definitions.
5. **Schemas (`app/schemas/`)**: Pydantic validation and serialization schemas.

## 🤖 Agent Skills

Hatchback projects ship with built-in [Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) in `.github/skills/`:

- **`hatchback`** — Full project overview, CLI commands, database config, auth system, and conventions.
- **`clean-architecture`** — Layered architecture rules, code examples, anti-patterns, and testing patterns.

These help AI coding assistants (GitHub Copilot, VS Code agent mode) understand your project structure and follow established patterns automatically.

## 📂 Project Structure

```
my_project/
├── .github/
│   └── skills/       # Agent Skills for AI assistants
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

## 🔧 CLI Reference

| Command | Description |
|---|---|
| `hbk init <name>` | Initialize a new project |
| `hbk run` | Start dev server with hot-reload |
| `hbk make <resource>` | Scaffold a new resource |
| `hbk remove <resource>` | Remove a resource and clean up imports |
| `hbk migrate create -m "msg"` | Create a new Alembic migration |
| `hbk migrate apply` | Apply pending migrations |
| `hbk migrate downgrade` | Rollback last migration (`-r -2` for multiple) |
| `hbk seed` | Seed database with initial data |
| `hbk inspect --url <db_url>` | Inspect existing DB and generate models |
| `hbk upgrade` | Sync latest skills and infra files |
| `hbk test` | Run the test suite |

---

*Built with 💖 and 🏎️ by Ignacio Bares(nachovoss) and the Hatchback Team.*


##  Support

Hatchback is an open-source project. If you'd like to support the development, you can donate via Bitcoin:

**BTC Address:** \c1q9fznxyf0skq8ux5ysrggw3veuqf92xtr25cccq\

![Bitcoin QR Code](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1q9fznxyf0skq8ux5ysrggw3veuqf92xtr25cccq)

Thank you for your support!

