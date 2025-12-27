import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

def play_intro():
    art = r"""
_   _       _       _     _                _    
 | | | |     | |     | |   | |              | |   
 | |_| | __ _| |_ ___| |__ | |__   __ _  ___| | __
 |  _  |/ _` | __/ __| '_ \| '_ \ / _` |/ __| |/ /
 | | | | (_| | || (__| | | | |_) | (_| | (__|   < 
 \_| |_/\__,_|\__\___|_| |_|_.__/ \__,_|\___|_|\_\
"""
    console.print(Panel(Text(art, style="bold cyan"), title="Hatchback", border_style="blue", expand=False))


def get_venv_executable(name):
    """Returns the path to the executable in the virtual environment if it exists."""
    if os.name == 'nt':
        path = os.path.join("venv", "Scripts", name + ".exe")
    else:
        path = os.path.join("venv", "bin", name)
    if os.path.exists(path):
        return path
    return name

def to_pascal_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))
