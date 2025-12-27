import os
import glob
import re
import subprocess
from ..utils import console, get_venv_executable

def handle_migrate(args):
    alembic_cmd = get_venv_executable("alembic")
    if args.action == "create":
        if not args.message:
            console.print("[bold red]Error: Migration message is required for 'create'. Use -m 'message'[/bold red]")
            return
        console.print(f"[bold green]Creating migration: {args.message}[/bold green]")
        try:
            subprocess.run([alembic_cmd, "revision", "--autogenerate", "-m", args.message], check=True)
            
            versions_dir = "alembic/versions"
            if os.path.exists(versions_dir):
                files = [f for f in glob.glob(os.path.join(versions_dir, "*.py")) if not os.path.basename(f).startswith("__")]
                if files:
                    newest_file = max(files, key=os.path.getctime)
                    max_num = 0
                    for f in files:
                        match = re.match(r"^(\d+)_", os.path.basename(f))
                        if match:
                            max_num = max(max_num, int(match.group(1)))
                    
                    next_num = max_num + 1
                    base_name = os.path.basename(newest_file)
                    parts = base_name.split("_", 1)
                    slug = parts[1] if len(parts) > 1 else base_name
                    new_name = f"{next_num}_{slug}"
                    os.rename(newest_file, os.path.join(versions_dir, new_name))
                    console.print(f"[bold green]Renamed migration file to: {new_name}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error creating migration:[/bold red] {e}")
            
    elif args.action == "apply":
        console.print("[bold green]Applying migrations...[/bold green]")
        try:
            subprocess.run([alembic_cmd, "upgrade", "head"], check=True)
        except Exception as e:
            console.print(f"[bold red]Error applying migrations:[/bold red] {e}")
