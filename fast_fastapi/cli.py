import argparse
import sys
from .commands.init import handle_init
from .commands.run import handle_run
from .commands.migrate import handle_migrate
from .commands.make import handle_make
from .utils import console, play_intro

def main():
    parser = argparse.ArgumentParser(
        description="Fast-FastAPI CLI - A production-ready FastAPI boilerplate generator and manager.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Initialize a new project
  fast-fastapi init my_awesome_project

  # Run the development server
  fast-fastapi run --host 0.0.0.0 --port 8000

  # Create a new migration
  fast-fastapi migrate create -m "create users table"

  # Apply migrations
  fast-fastapi migrate apply

  # Scaffold a new resource (Model, Service, Repository, etc.)
  fast-fastapi make product
"""
    )
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

    args = parser.parse_args()
    if args.command == "init": handle_init(args)
    elif args.command == "run": handle_run(args)
    elif args.command == "migrate": handle_migrate(args)
    elif args.command == "make": handle_make(args)
    else:
        play_intro()
        console.print("[bold blue]Fast-FastAPI CLI[/bold blue]")
        console.print("Usage: fast-fastapi [command] [options]")
        console.print("\nAvailable commands:")
        console.print("  [green]init[/green]      Initialize a new project")
        console.print("  [green]run[/green]       Run the development server")
        console.print("  [green]migrate[/green]   Manage database migrations")
        console.print("  [green]make[/green]      Scaffold a new resource")
        console.print("\nRun 'fast-fastapi [command] --help' for more information.")

if __name__ == "__main__":
    main()
