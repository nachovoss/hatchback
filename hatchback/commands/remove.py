import os
from rich.prompt import Confirm
from ..utils import console, to_pascal_case


def remove_resource(resource, force=False):
    resource = resource.lower()
    Resource = to_pascal_case(resource)

    console.print(f"[bold red]Removing resource: {Resource}[/bold red]")

    base_dir = os.getcwd()
    app_dir = os.path.join(base_dir, "app")

    if not os.path.exists(app_dir):
        console.print("[bold red]Error: 'app' directory not found. Are you in the project root?[/bold red]")
        return

    # Files that hatchback make creates
    files_to_remove = [
        f"app/models/{resource}.py",
        f"app/schemas/{resource}.py",
        f"app/repositories/{resource}.py",
        f"app/services/{resource}.py",
        f"app/routes/{resource}.py",
        f"tests/test_{resource}s.py",
    ]

    existing_files = [f for f in files_to_remove if os.path.exists(os.path.join(base_dir, f))]

    if not existing_files:
        console.print(f"[yellow]No files found for resource '{resource}'. Nothing to remove.[/yellow]")
        return

    console.print(f"\n[bold]The following files will be deleted:[/bold]")
    for f in existing_files:
        console.print(f"  [red]✗[/red] {f}")

    console.print(f"\n[bold]The following __init__.py files will be cleaned up:[/bold]")
    console.print(f"  [yellow]~[/yellow] app/models/__init__.py")
    console.print(f"  [yellow]~[/yellow] app/routes/__init__.py")
    console.print(f"  [yellow]~[/yellow] app/services/__init__.py")
    console.print(f"  [yellow]~[/yellow] app/repositories/__init__.py")

    if not force:
        if not Confirm.ask(f"\n[bold red]Are you sure you want to remove '{Resource}'?[/bold red]", default=False):
            console.print("[dim]Aborted.[/dim]")
            return

    # Delete resource files
    for f in existing_files:
        full_path = os.path.join(base_dir, f)
        os.remove(full_path)
        console.print(f"[red]Deleted {f}[/red]")

    # Clean up models/__init__.py
    _remove_line_from_file(
        os.path.join(app_dir, "models", "__init__.py"),
        f"from app.models.{resource} import {Resource}",
        "app/models/__init__.py"
    )

    # Clean up routes/__init__.py
    routes_init = os.path.join(app_dir, "routes", "__init__.py")
    if os.path.exists(routes_init):
        with open(routes_init, "r") as f:
            content = f.read()

        import_line = f"from .{resource} import router as {resource}_router\n"
        content = content.replace(import_line, "")

        # Remove from routers list
        content = content.replace(f"{resource}_router, ", "")
        content = content.replace(f", {resource}_router", "")
        content = content.replace(f"{resource}_router", "")

        with open(routes_init, "w") as f:
            f.write(content)
        console.print(f"[yellow]Cleaned app/routes/__init__.py[/yellow]")

    # Clean up services/__init__.py
    services_init = os.path.join(app_dir, "services", "__init__.py")
    if os.path.exists(services_init):
        with open(services_init, "r") as f:
            content = f.read()

        import_line = f"from .{resource} import {Resource}Service\n"
        content = content.replace(import_line, "")
        content = content.replace(f"\"{Resource}Service\", ", "")
        content = content.replace(f", \"{Resource}Service\"", "")
        content = content.replace(f"\"{Resource}Service\"", "")

        with open(services_init, "w") as f:
            f.write(content)
        console.print(f"[yellow]Cleaned app/services/__init__.py[/yellow]")

    # Clean up repositories/__init__.py
    repos_init = os.path.join(app_dir, "repositories", "__init__.py")
    if os.path.exists(repos_init):
        with open(repos_init, "r") as f:
            content = f.read()

        import_line = f"from .{resource} import {Resource}Repository\n"
        content = content.replace(import_line, "")
        content = content.replace(f"\"{Resource}Repository\", ", "")
        content = content.replace(f", \"{Resource}Repository\"", "")
        content = content.replace(f"\"{Resource}Repository\"", "")

        with open(repos_init, "w") as f:
            f.write(content)
        console.print(f"[yellow]Cleaned app/repositories/__init__.py[/yellow]")

    console.print(f"\n[bold green]✅ Resource '{Resource}' removed successfully.[/bold green]")
    console.print(f"[dim]Note: If you had Alembic migrations for this resource, you may want to create a new migration to drop the table.[/dim]")


def _remove_line_from_file(filepath, line_to_remove, display_name):
    """Remove all lines containing the exact text from a file."""
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        lines = f.readlines()

    new_lines = [l for l in lines if line_to_remove not in l]

    if len(new_lines) != len(lines):
        with open(filepath, "w") as f:
            f.writelines(new_lines)
        console.print(f"[yellow]Cleaned {display_name}[/yellow]")


def handle_remove(args):
    remove_resource(args.resource, force=args.force)
