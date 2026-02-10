import argparse
import sys
from .commands.init import handle_init
from .commands.run import handle_run
from .commands.migrate import handle_migrate
from .commands.make import handle_make
from .commands.remove import handle_remove
from .commands.upgrade import handle_upgrade
from .commands.seed import handle_seed
from .commands.test import handle_test
from .commands.inspect import handle_inspect
from .utils import console, play_intro
from . import __version__

def main():
    parser = argparse.ArgumentParser(
        description="Hatchback CLI - A production-ready FastAPI boilerplate generator and manager.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples (tip: 'hbk' is a shortcut for 'hatchback'):
  # Initialize a new project
  hbk init my_awesome_project

  # Run the development server
  hbk run --host 0.0.0.0 --port 8000

  # Create a new migration
  hbk migrate create -m "create users table"

  # Apply migrations
  hbk migrate apply

  # Scaffold a new resource (Model, Service, Repository, etc.)
  hbk make product

  # Remove a scaffolded resource and clean up imports
  hbk remove product

  # Seed the database with default tenant and admin user
  hbk seed

  # Inspect an existing database and generate models
  hbk inspect --url postgresql://user:pass@localhost/db --output app/models/legacy.py

  # Upgrade skills and infrastructure in an existing project
  hbk upgrade

  # Run tests
  hbk test
"""
    )
    
    parser.add_argument("--version", action="version", version=f"Hatchback CLI v{__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    init_parser = subparsers.add_parser(
        "init", 
        help="Initialize a new project with Docker, Alembic, and best practices",
        description="Bootstrap a new FastAPI project. Sets up directory structure, virtual environment, and configuration."
    )
    init_parser.add_argument("project_name", nargs="?", help="Project name")
    init_parser.add_argument("--install", action="store_true", help="Install dependencies")
    init_parser.add_argument("--no-install", action="store_true", help="Skip installation")
    init_parser.add_argument("--use-uv", action="store_true", help="Use uv for faster installation")
    init_parser.add_argument("--docker", action="store_true", help="Include Docker")
    init_parser.add_argument("--no-docker", action="store_true", help="Skip Docker")

    run_parser = subparsers.add_parser(
        "run", 
        help="Run the development server with hot-reload",
        description="Start the Uvicorn server with hot-reload enabled. Useful for development."
    )
    run_parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    run_parser.add_argument("--host", default="127.0.0.1", help="Host to run on")

    migrate_parser = subparsers.add_parser(
        "migrate", 
        help="Manage database migrations (create/apply)",
        description="Wrapper around Alembic to easily create and apply database migrations."
    )
    migrate_parser.add_argument("action", choices=["create", "apply"], help="Action: create or apply")
    migrate_parser.add_argument("-m", "--message", help="Migration message (required for create)")

    make_parser = subparsers.add_parser(
        "make", 
        help="Scaffold a new resource (Model, Service, Repository, etc.)",
        description="Generate a new resource. Creates Model, Schema, Repository, Service, and Controller files automatically."
    )
    make_parser.add_argument("resource", help="Name of the resource (snake_case)")

    remove_parser = subparsers.add_parser(
        "remove",
        help="Remove a scaffolded resource and clean up all imports",
        description="Remove a previously scaffolded resource. Deletes model, schema, repository, service, route and test files, and cleans up __init__.py imports."
    )
    remove_parser.add_argument("resource", help="Name of the resource to remove (snake_case)")
    remove_parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation prompt")

    seed_parser = subparsers.add_parser(
        "seed", 
        help="Seed the database with default tenant and admin user",
        description="Run the seed.py script to populate the database with initial data."
    )
    seed_parser.add_argument("--password", help="Admin password (optional, will prompt if not provided)")

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect an existing database and generate SQLAlchemy models",
        description="Reflects tables from a database URL and generates SQLAlchemy model code using sqlacodegen."
    )
    inspect_parser.add_argument("--url", help="Database connection URL")
    inspect_parser.add_argument("--output", help="Output file path (default: app/models/imported.py)")
    inspect_parser.add_argument("--scaffold", action="store_true", help="Automatically scaffold full architecture (Service, Repo, etc.) for each table")

    upgrade_parser = subparsers.add_parser(
        "upgrade",
        help="Sync latest skills and infrastructure files into this project",
        description="Update an existing project with the latest agent skills and infrastructure files from the installed version of Hatchback. Does not touch Docker files, user code, or config."
    )

    test_parser = subparsers.add_parser(
        "test", 
        help="Run tests using pytest",
        description="Run the test suite."
    )

    args = parser.parse_args()
    if args.command == "init": handle_init(args)
    elif args.command == "run": handle_run(args)
    elif args.command == "migrate": handle_migrate(args)
    elif args.command == "make": handle_make(args)
    elif args.command == "remove": handle_remove(args)
    elif args.command == "seed": handle_seed(args)
    elif args.command == "inspect": handle_inspect(args)
    elif args.command == "upgrade": handle_upgrade(args)
    elif args.command == "test": handle_test(args)
    else:
        play_intro()
        console.print("[bold blue]Hatchback CLI[/bold blue]")
        console.print("Usage: hatchback [command] [options]")
        console.print("\nAvailable commands:")
        console.print("  [green]init[/green]      Initialize a new project")
        console.print("  [green]run[/green]       Run the development server")
        console.print("  [green]migrate[/green]   Manage database migrations")
        console.print("  [green]make[/green]      Scaffold a new resource")
        console.print("  [green]remove[/green]    Remove a scaffolded resource")
        console.print("  [green]seed[/green]      Seed database with default data")
        console.print("  [green]inspect[/green]   Inspect existing DB and scaffold")
        console.print("  [green]upgrade[/green]   Sync latest skills and infra files")
        console.print("  [green]test[/green]      Run tests")
        console.print("\nRun 'hatchback [command] --help' for more information.")

if __name__ == "__main__":
    main()
