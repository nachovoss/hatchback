import os
import shutil
import filecmp
from rich.prompt import Confirm
from ..utils import console


# Files that are safe to sync from the template into existing projects.
# These are "infrastructure" files managed by hatchback, not user code.
# Docker files are explicitly excluded per design decision.
UPGRADE_PATHS = [
    ".github/skills",
]

# Files that should NEVER be overwritten by upgrade
EXCLUDE_FILES = {
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore",
    ".env",
    ".env.example",
    "requirements.txt",
    "pyproject.toml",
    "alembic.ini",
    "seed.py",
    "seeds.json",
    "README.md",
}

# Directories containing user code — never touched
EXCLUDE_DIRS = {
    "app",
    "tests",
    "alembic",
    "venv",
    "__pycache__",
}


def handle_upgrade(args):
    target_dir = os.getcwd()

    # Sanity check: are we in a hatchback project?
    app_dir = os.path.join(target_dir, "app")
    if not os.path.exists(app_dir):
        console.print("[bold red]Error: 'app' directory not found. Are you in a Hatchback project root?[/bold red]")
        return

    # Locate the template directory from the installed package
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(package_dir, "template")

    if not os.path.exists(template_dir):
        console.print("[bold red]Error: Template directory not found in the installed package.[/bold red]")
        return

    console.print("[bold blue]🔄 Hatchback Upgrade[/bold blue]")
    console.print(f"[dim]Template source: {template_dir}[/dim]\n")

    added = []
    updated = []
    skipped = []

    for rel_path in UPGRADE_PATHS:
        src = os.path.join(template_dir, rel_path)
        dst = os.path.join(target_dir, rel_path)

        if not os.path.exists(src):
            continue

        if os.path.isdir(src):
            _sync_directory(src, dst, rel_path, added, updated, skipped)
        else:
            _sync_file(src, dst, rel_path, added, updated, skipped)

    # Print summary
    console.print("")
    if added:
        console.print(f"[bold green]Added ({len(added)}):[/bold green]")
        for f in added:
            console.print(f"  [green]+ {f}[/green]")

    if updated:
        console.print(f"[bold yellow]Updated ({len(updated)}):[/bold yellow]")
        for f in updated:
            console.print(f"  [yellow]~ {f}[/yellow]")

    if skipped:
        console.print(f"[dim]Unchanged ({len(skipped)}):[/dim]")
        for f in skipped:
            console.print(f"  [dim]  {f}[/dim]")

    if not added and not updated:
        console.print("[bold green]✅ Everything is up to date![/bold green]")
    else:
        total = len(added) + len(updated)
        console.print(f"\n[bold green]✅ Upgrade complete — {total} file(s) synced.[/bold green]")


def _sync_directory(src_dir, dst_dir, rel_base, added, updated, skipped):
    """Recursively sync a directory from template to project."""
    for root, dirs, files in os.walk(src_dir):
        # Compute relative path from the source directory
        rel_root = os.path.relpath(root, src_dir)
        if rel_root == ".":
            current_rel = rel_base
        else:
            current_rel = os.path.join(rel_base, rel_root)

        # Create target directory if needed
        target_root = os.path.join(os.path.dirname(dst_dir), current_rel) if rel_base != current_rel else dst_dir
        # Simpler: compute from the overall target
        target_root = os.path.join(dst_dir, rel_root) if rel_root != "." else dst_dir

        for filename in files:
            if filename in EXCLUDE_FILES:
                continue
            if filename.endswith(".pyc") or filename == "__pycache__":
                continue

            src_file = os.path.join(root, filename)
            dst_file = os.path.join(target_root, filename)
            rel_file = os.path.join(current_rel, filename)

            _sync_file(src_file, dst_file, rel_file, added, updated, skipped)


def _sync_file(src, dst, rel_path, added, updated, skipped):
    """Sync a single file from template to project."""
    if not os.path.exists(dst):
        # New file — always add
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        added.append(rel_path)
    elif not filecmp.cmp(src, dst, shallow=False):
        # File exists but differs — overwrite (these are hatchback-managed files)
        shutil.copy2(src, dst)
        updated.append(rel_path)
    else:
        # Identical — skip
        skipped.append(rel_path)
