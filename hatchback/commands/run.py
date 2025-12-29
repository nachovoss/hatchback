import os
import subprocess
from ..utils import console, get_venv_executable

def handle_run(args):
    if not os.path.exists("app"):
        console.print("[bold red]Error: 'app' directory not found. Are you in the project root?[/bold red]")
        return

    uvicorn_cmd = get_venv_executable("uvicorn")
    console.print(f"[bold green]Starting server on {args.host}:{args.port}...[/bold green]")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    try:
        subprocess.run(
            [uvicorn_cmd, "app.main:app", "--reload", "--host", args.host, "--port", str(args.port)], 
            check=True,
            env=env
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error running server:[/bold red] {e}")
