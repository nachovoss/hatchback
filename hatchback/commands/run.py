import os
import subprocess
from ..utils import console, get_venv_executable

def handle_run(args):
    if not os.path.exists("app"):
        console.print("[bold red]Error: 'app' directory not found. Are you in the project root?[/bold red]")
        return

    # Use python -m uvicorn instead of uvicorn executable directly to avoid path issues on Windows
    if os.name == 'nt':
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")
    
    if not os.path.exists(python_exe):
        python_exe = "python"

    console.print(f"[bold green]Starting server on {args.host}:{args.port}...[/bold green]")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    try:
        subprocess.run(
            [python_exe, "-m", "uvicorn", "app.main:app", "--reload", "--host", args.host, "--port", str(args.port)], 
            check=True,
            env=env
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error running server:[/bold red] {e}")
