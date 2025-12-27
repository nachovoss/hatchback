import os
import time
import random
import string
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel

console = Console()

class DigitalReveal:
    def __init__(self):
        self.width = 80
        self.height = 15
        self.target_text = "FAST-FAST-API"
        self.pixel_map = self._generate_pixel_map()
        self.current_frame = 0
        self.total_frames = 50
        
        self.chars = [[random.choice(string.ascii_uppercase + string.digits) 
                       for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]

    def _get_char_bitmap(self, char):
        bitmaps = {
            'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
            'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
            'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
            'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
            '-': ["     ", "     ", "     ", " ### ", "     ", "     ", "     "],
            'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
            'I': ["###", " # ", " # ", " # ", " # ", " # ", "###"],
        }
        return bitmaps.get(char, ["     "] * 7)

    def _generate_pixel_map(self):
        pixel_map = [[False for _ in range(self.width)] for _ in range(self.height)]
        start_x = (self.width - (len(self.target_text) * 6)) // 2
        start_y = (self.height - 7) // 2
        for i, char in enumerate(self.target_text):
            bitmap = self._get_char_bitmap(char)
            char_x = start_x + (i * 6)
            for r, row in enumerate(bitmap):
                for c, pixel in enumerate(row):
                    if pixel == '#':
                        pixel_map[start_y + r][char_x + c] = True
        return pixel_map

    def get_frame(self):
        output = Text()
        for y in range(self.height):
            for x in range(self.width):
                if not self.revealed[y][x]:
                    if random.random() < 0.1:
                        self.chars[y][x] = random.choice(string.ascii_uppercase + string.digits)
        progress = self.current_frame / self.total_frames
        for y in range(self.height):
            for x in range(self.width):
                char = self.chars[y][x]
                is_target = self.pixel_map[y][x]
                if is_target:
                    if not self.revealed[y][x] and random.random() < (progress * 1.5):
                        self.revealed[y][x] = True
                    if self.revealed[y][x]:
                        output.append("█", style="bold cyan")
                    else:
                        output.append(char, style="dim blue")
                else:
                    output.append(char, style="grey23")
            output.append("\n")
        self.current_frame += 1
        return output

def play_intro():
    animation = DigitalReveal()
    with Live(console=console, refresh_per_second=12) as live:
        for _ in range(animation.total_frames + 15):
            frame = animation.get_frame()
            live.update(Panel(frame, title="Fast-FastAPI", border_style="blue", expand=False))
            time.sleep(0.05)

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
