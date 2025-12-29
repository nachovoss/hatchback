import os
import subprocess
from rich.prompt import Prompt
from ..utils import console, get_venv_executable

def handle_seed(args):
    python_cmd = get_venv_executable("python")
    seed_script = "seed.py"
    
    if not os.path.exists(seed_script):
        console.print("[bold red]Error: seed.py not found in current directory.[/bold red]")
        console.print("Please make sure you are in the root of your Hatchback project.")
        return

    console.print("[bold green]Running seed script...[/bold green]")
    
    env = os.environ.copy()
    # Ensure PYTHONPATH includes current directory so app modules can be imported
    env["PYTHONPATH"] = os.getcwd()
    
    if args.password:
        env["ADMIN_PASSWORD"] = args.password
    else:
        password = Prompt.ask("Enter admin password", password=True, default="admin")
        env["ADMIN_PASSWORD"] = password

    try:
        subprocess.run([python_cmd, seed_script], check=True, env=env)
    except Exception as e:
        console.print(f"[bold red]Error running seed script:[/bold red] {e}")
