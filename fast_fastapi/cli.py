import argparse
import sys
from .commands.init import handle_init
from .commands.run import handle_run
from .commands.migrate import handle_migrate
from .commands.make import handle_make
from .utils import console

def main():
    parser = argparse.ArgumentParser(description="Fast-FastAPI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("project_name", nargs="?", help="Project name")
    init_parser.add_argument("--install", action="store_true", help="Install dependencies")
    init_parser.add_argument("--no-install", action="store_true", help="Skip installation")
    init_parser.add_argument("--docker", action="store_true", help="Include Docker")
    init_parser.add_argument("--no-docker", action="store_true", help="Skip Docker")

    run_parser = subparsers.add_parser("run", help="Run the development server")
    run_parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    run_parser.add_argument("--host", default="127.0.0.1", help="Host to run on")

    migrate_parser = subparsers.add_parser("migrate", help="Manage database migrations")
    migrate_parser.add_argument("action", choices=["create", "apply"], help="Action: create or apply")
    migrate_parser.add_argument("-m", "--message", help="Migration message (required for create)")

    make_parser = subparsers.add_parser("make", help="Scaffold a new resource")
    make_parser.add_argument("resource", help="Name of the resource (snake_case)")

    args = parser.parse_args()
    if args.command == "init": handle_init(args)
    elif args.command == "run": handle_run(args)
    elif args.command == "migrate": handle_migrate(args)
    elif args.command == "make": handle_make(args)
    else: parser.print_help()

if __name__ == "__main__":
    main()
