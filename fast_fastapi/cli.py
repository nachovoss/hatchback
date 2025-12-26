import os
import shutil
import sys
import argparse
import subprocess
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

console = Console()

def init_project():
    """
    Initializes a new FastAPI Alembic project.
    """
    console.print(Panel.fit("Fast-FastAPI Generator", style="bold blue"))

    parser = argparse.ArgumentParser(description="Initialize a new Fast-FastAPI project.")
    parser.add_argument("project_name", nargs="?", help="The name of the project (and directory) to create.")
    parser.add_argument("--install", action="store_true", help="Create venv and install requirements automatically.")
    parser.add_argument("--no-install", action="store_true", help="Do not create venv and install requirements.")
    parser.add_argument("--docker", action="store_true", help="Include Docker files.")
    parser.add_argument("--no-docker", action="store_true", help="Do not include Docker files.")
    
    args = parser.parse_args()
    
    # 1. Get Project Name
    project_name = args.project_name
    if not project_name:
        project_name = Prompt.ask("[bold green]Enter project name[/bold green] (leave empty to use current directory)")

    # 2. Get Install Preference
    should_install = False
    if args.install:
        should_install = True
    elif args.no_install:
        should_install = False
    else:
        should_install = Confirm.ask("[bold green]Create virtual environment and install requirements?[/bold green]", default=True)

    # 3. Get Docker Preference
    should_include_docker = False
    if args.docker:
        should_include_docker = True
    elif args.no_docker:
        should_include_docker = False
    else:
        should_include_docker = Confirm.ask("[bold green]Include Docker files (Dockerfile, docker-compose.yml)?[/bold green]", default=True)

    # 4. Define paths
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(package_dir, "template")
    
    if project_name:
        target_dir = os.path.join(os.getcwd(), project_name)
    else:
        target_dir = os.getcwd()
    
    console.print(f"\nInitializing new project in [bold yellow]{target_dir}[/bold yellow]...")
    
    try:
        # 5. Copy Files
        with console.status("[bold green]Copying template files...[/bold green]", spinner="dots"):
            # dirs_exist_ok=True allows copying into an existing directory (Python 3.8+)
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
            
            # Remove Docker files if not requested
            if not should_include_docker:
                docker_files = ["Dockerfile", "docker-compose.yml"]
                for f in docker_files:
                    f_path = os.path.join(target_dir, f)
                    if os.path.exists(f_path):
                        os.remove(f_path)
        
        console.print("[bold green]✓ Template files copied.[/bold green]")

        # 6. Install Dependencies (if requested)
        if should_install:
            venv_dir = os.path.join(target_dir, "venv")
            
            with console.status("[bold green]Creating virtual environment...[/bold green]", spinner="dots"):
                subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            console.print("[bold green]✓ Virtual environment created.[/bold green]")
            
            with console.status("[bold green]Installing requirements (this may take a while)...[/bold green]", spinner="dots"):
                if os.name == 'nt':
                    pip_exe = os.path.join(venv_dir, "Scripts", "pip")
                else:
                    pip_exe = os.path.join(venv_dir, "bin", "pip")
                    
                requirements_file = os.path.join(target_dir, "requirements.txt")
                # Capture output to avoid cluttering the console unless there's an error
                subprocess.run([pip_exe, "install", "-r", requirements_file], check=True, capture_output=True)
            console.print("[bold green]✓ Dependencies installed.[/bold green]")
        
        # 7. Print Success and Next Steps
        console.print(Panel("[bold green]Project initialized successfully![/bold green]", expand=False))
        
        next_steps = Text()
        next_steps.append("\nNext steps:\n", style="bold underline")
        
        if project_name:
            next_steps.append(f"- cd {project_name}\n")
        
        if should_include_docker:
            next_steps.append("- docker-compose up -d --build\n")
        else:
            if not should_install:
                next_steps.append("- python -m venv venv\n")
                if os.name == 'nt':
                    next_steps.append("- venv\\Scripts\\activate\n")
                else:
                    next_steps.append("- source venv/bin/activate\n")
                next_steps.append("- pip install -r requirements.txt\n")
            else:
                if os.name == 'nt':
                    next_steps.append("- venv\\Scripts\\activate\n")
                else:
                    next_steps.append("- source venv/bin/activate\n")
                
            next_steps.append("- Configure .env (copy from .env.example if you create one)\n")
            next_steps.append("- alembic revision --autogenerate -m 'init'\n")
            next_steps.append("- alembic upgrade head\n")
            next_steps.append("- uvicorn app.main:app --reload\n")
            
        console.print(next_steps)
        
    except Exception as e:
        console.print(f"[bold red]Error initializing project:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_project()
