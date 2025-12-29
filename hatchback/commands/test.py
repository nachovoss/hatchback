import subprocess
from ..utils import console, get_venv_executable

def handle_test(args):
    pytest_cmd = get_venv_executable("pytest")
    console.print("[bold green]Running tests...[/bold green]")
    try:
        subprocess.run([pytest_cmd], check=True)
    except subprocess.CalledProcessError:
        console.print("[bold red]Tests failed.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error running tests:[/bold red] {e}")
