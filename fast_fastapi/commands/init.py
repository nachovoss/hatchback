import os
import shutil
import sys
import subprocess
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from ..utils import console, play_intro

def handle_init(args):
    play_intro()
    console.print(Panel.fit("Fast-FastAPI Generator", style="bold blue"))
    console.print(Panel(
        "Welcome to the Fast-FastAPI Generator!\n\n"
        "This tool will help you bootstrap a production-ready FastAPI application.\n",
        title="Guide", border_style="green"
    ))
    
    project_name = args.project_name
    if not project_name:
        project_name = Prompt.ask("[bold green]Enter project name[/bold green] (leave empty to use current directory)")

    should_install = args.install if args.install or args.no_install else Confirm.ask("[bold green]Create virtual environment and install requirements?[/bold green]", default=True)
    
    use_uv = False
    if should_install:
        uv_path = shutil.which("uv")
        if args.use_uv:
            if not uv_path:
                console.print("[yellow]Warning: --use-uv specified but 'uv' not found. Falling back to pip.[/yellow]")
            else:
                use_uv = True
        elif uv_path:
             use_uv = Confirm.ask("[bold green]uv found! Use uv for faster installation?[/bold green]", default=True)

    should_include_docker = args.docker if args.docker or args.no_docker else Confirm.ask("[bold green]Include Docker files?[/bold green]", default=True)

    # Adjust package_dir to point to the parent of 'commands' (i.e., fast_fastapi)
    # __file__ is .../fast_fastapi/commands/init.py
    # os.path.dirname(__file__) is .../fast_fastapi/commands
    # os.path.dirname(...) is .../fast_fastapi
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(package_dir, "template")
    target_dir = os.path.join(os.getcwd(), project_name) if project_name else os.getcwd()
    
    console.print(f"\nInitializing new project in [bold yellow]{target_dir}[/bold yellow]...")
    
    try:
        with console.status("[bold green]Copying template files...[/bold green]", spinner="dots"):
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
            if not should_include_docker:
                for f in ["Dockerfile", "docker-compose.yml", ".dockerignore"]:
                    f_path = os.path.join(target_dir, f)
                    if os.path.exists(f_path):
                        os.remove(f_path)
        console.print("[bold green]✓ Template files copied.[/bold green]")

        if should_install:
            venv_dir = os.path.join(target_dir, "venv")
            
            if use_uv:
                with console.status("[bold green]Creating virtual environment with uv...[/bold green]", spinner="dots"):
                    subprocess.run(["uv", "venv", venv_dir], check=True, capture_output=True)
            else:
                with console.status("[bold green]Creating virtual environment...[/bold green]", spinner="dots"):
                    subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            console.print("[bold green]✓ Virtual environment created.[/bold green]")
            
            with console.status("[bold green]Installing requirements...[/bold green]", spinner="dots"):
                if use_uv:
                    venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")
                    subprocess.run(["uv", "pip", "install", "-p", venv_python, "-r", os.path.join(target_dir, "requirements.txt")], check=True, capture_output=True)
                else:
                    pip_exe = os.path.join(venv_dir, "Scripts", "pip") if os.name == 'nt' else os.path.join(venv_dir, "bin", "pip")
                    subprocess.run([pip_exe, "install", "-r", os.path.join(target_dir, "requirements.txt")], check=True, capture_output=True)
            console.print("[bold green]✓ Dependencies installed.[/bold green]")
        
        console.print(Panel("[bold green]Project initialized successfully![/bold green]", expand=False))
        
        next_steps = Text()
        next_steps.append("\nNext steps:\n", style="bold underline")
        if project_name: next_steps.append(f"- cd {project_name}\n")
        next_steps.append("- fast-fastapi migrate create -m 'init'\n")
        next_steps.append("- fast-fastapi migrate apply\n")
        next_steps.append("- fast-fastapi run\n")
        console.print(next_steps)
        
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error running command:[/bold red] {e.cmd}")
        if e.stderr:
            console.print(f"[red]{e.stderr.decode()}[/red]")
        if e.stdout:
            console.print(f"[dim]{e.stdout.decode()}[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error initializing project:[/bold red] {e}")
        sys.exit(1)
