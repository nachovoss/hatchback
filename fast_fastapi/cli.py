import os
import shutil
import sys
import argparse
import subprocess
import time
import random
import string
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

console = Console()

class DigitalReveal:
    def __init__(self):
        self.width = 80
        self.height = 15
        self.target_text = "FAST-FAST-API"
        self.pixel_map = self._generate_pixel_map()
        self.current_frame = 0
        self.total_frames = 50  # Slower animation
        
        # Initialize background characters to prevent full-screen blinking
        self.chars = [[random.choice(string.ascii_uppercase + string.digits) 
                       for _ in range(self.width)] for _ in range(self.height)]
        # Track revealed pixels to prevent flickering
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]

    def _get_char_bitmap(self, char):
        bitmaps = {
            'F': [
                "#####",
                "#    ",
                "#    ",
                "#### ",
                "#    ",
                "#    ",
                "#    "
            ],
            'A': [
                " ### ",
                "#   #",
                "#   #",
                "#####",
                "#   #",
                "#   #",
                "#   #"
            ],
            'S': [
                " ####",
                "#    ",
                "#    ",
                " ### ",
                "    #",
                "    #",
                "#### "
            ],
            'T': [
                "#####",
                "  #  ",
                "  #  ",
                "  #  ",
                "  #  ",
                "  #  ",
                "  #  "
            ],
            '-': [
                "     ",
                "     ",
                "     ",
                " ### ",
                "     ",
                "     ",
                "     "
            ],
            'P': [
                "#### ",
                "#   #",
                "#   #",
                "#### ",
                "#    ",
                "#    ",
                "#    "
            ],
            'I': [
                "###",
                " # ",
                " # ",
                " # ",
                " # ",
                " # ",
                "###"
            ],
        }
        return bitmaps.get(char, ["     "] * 7)

    def _generate_pixel_map(self):
        grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        char_height = 7
        full_bitmap = [""] * char_height
        
        for char in self.target_text:
            bmp = self._get_char_bitmap(char)
            for i in range(char_height):
                full_bitmap[i] += bmp[i] + " "
        
        text_width = len(full_bitmap[0])
        start_x = max(0, (self.width - text_width) // 2)
        start_y = (self.height - char_height) // 2
        
        for r in range(char_height):
            for c in range(text_width):
                if c + start_x < self.width and full_bitmap[r][c] != ' ':
                    grid[start_y + r][start_x + c] = True
        return grid

    def get_frame(self):
        output = Text()
        progress = min(1.0, self.current_frame / self.total_frames)
        
        # Update only a small percentage of background characters per frame
        # This creates a "digital noise" effect without the chaotic blinking
        changes = int(self.width * self.height * 0.05)
        for _ in range(changes):
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)
            self.chars[ry][rx] = random.choice(string.ascii_uppercase + string.digits)

        for y in range(self.height):
            for x in range(self.width):
                is_target = self.pixel_map[y][x]
                char = self.chars[y][x]
                
                if is_target:
                    if self.revealed[y][x]:
                        output.append("█", style="bold blue")
                    else:
                        # Check if we should reveal this pixel now
                        # Probability increases with progress
                        if progress > 0.1 and random.random() < (progress - 0.1) * 0.1:
                            self.revealed[y][x] = True
                            output.append("█", style="bold blue")
                        elif progress > 0.95: # Force reveal at the end
                            self.revealed[y][x] = True
                            output.append("█", style="bold blue")
                        else:
                            output.append(char, style="white")
                else:
                    output.append(char, style="grey23")
            output.append("\n")
            
        self.current_frame += 1
        return output

def play_intro():
    animation = DigitalReveal()
    with Live(console=console, refresh_per_second=12) as live:
        for _ in range(animation.total_frames + 15):  # Run a bit longer to hold the final state
            frame = animation.get_frame()
            live.update(Panel(frame, title="Fast-FastAPI", border_style="blue", expand=False))
            time.sleep(0.05)

def init_project():
    """
    Initializes a new FastAPI Alembic project.
    """
    parser = argparse.ArgumentParser(description="Initialize a new Fast-FastAPI project.")
    parser.add_argument("project_name", nargs="?", help="The name of the project (and directory) to create.")
    parser.add_argument("--install", action="store_true", help="Create venv and install requirements automatically.")
    parser.add_argument("--no-install", action="store_true", help="Do not create venv and install requirements.")
    parser.add_argument("--docker", action="store_true", help="Include Docker files.")
    parser.add_argument("--no-docker", action="store_true", help="Do not include Docker files.")
    
    args = parser.parse_args()

    play_intro()
    console.print(Panel.fit("Fast-FastAPI Generator", style="bold blue"))

    console.print(Panel(
        "Welcome to the Fast-FastAPI Generator!\n\n"
        "This tool will help you bootstrap a production-ready FastAPI application with:\n"
        "• Alembic for database migrations\n"
        "• SQLAlchemy for ORM\n"
        "• Docker & Docker Compose setup\n"
        "• Pytest for testing\n\n"
        "Follow the prompts to configure your project.",
        title="Guide",
        border_style="green"
    ))
    
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
