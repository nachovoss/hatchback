# Fast Boilerplate Package

A CLI tool to generate a production-ready FastAPI project with Alembic, SQLAlchemy, and a multi-tenant architecture.

## Installation

You can install this package locally:

```bash
pip install .
```

Or if you publish it to PyPI:

```bash
pip install fast-boilerplate
```

## Usage

To create a new project, simply run:

```bash
mkdir my-new-project
cd my-new-project
fast-boilerplate
```

This will scaffold the following structure in your current directory:

- **FastAPI** app with `app/main.py`
- **SQLAlchemy** setup with `app/config/database.py`
- **Alembic** migrations setup
- **Multi-tenant** architecture (User & Tenant models)
- **Repository Pattern** implementation
- **JWT Authentication**

## Development

To develop on this package:

1.  Clone the repository
2.  Install in editable mode: `pip install -e .`
3.  Make changes to `fast_boilerplate/template`
4.  Test by running `fast-boilerplate` in a test directory
