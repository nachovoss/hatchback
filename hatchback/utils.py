import os
import time
import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live

console = Console()

def play_intro():
    width = 50
    
    # A classic hatchback shape
    car = [
        r"""                                                                                                          
                                                                                                          
                                                                                                          
                                                                                                          
                              $&&&&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&                                
                            &X&++++++++++++++++++++++++++++++++++++++++++&$&                              
                           $$&++++++++++++++++++++++++++++++++++++++++++++&&$                             
                          &&&++++++++++++++++++++++++++++++++++++++++++++++&X&                           
                         &&&++++++++++++++++++++++++++++++++++++++++++++++++&$&                          
                        &&&++++++++++++++++++++          ++++++++++++++++++++&X&                         
                &&&&&; &&&+++++++++x;X$&&&&&&&&+++x+;xx;;+++$+++++++++++++++&&&&X& x&&&&$                 
               ;;;;;;;&&&&&&&&&&&&&&X+xx++++              ++++x+;;;X&&&&&&&&&&&&&&x;;;;;;;                
               ;;;;;;$&+++++++++++++++++++++++;;+xx.X&++++++++++++++++++;++;:;&&&&&;;;;;;;                
                   ;x$&+++++++++++++++++++++++++++++++++++++++++++++++++++++&&&&&&&$;;                    
                  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                   
                 &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                  
                &&++++XXx;+X+:::+XXx::::;:::::;;;:::::::::;::;::;;:::;xx+::::++;+xx+;;;;&                 
               x+;;x&&&&&&X;: .$&&&&&+                             .$&&&&&;  ;x&$$$$$X.;;x                
             &&x;;;&$X&&&&&+. ;&&&&&&&                             ;&&&&&&$  +&&&Xx;+X+;;;&               
            &&&+;;+&&$&&&&&X. :&&&&&&x          HATCHBACK CLI      .&&&&&&X  +$$$&$X&&+.;;&&&             
            &&;x;;.$&&&&&&&;    :X&+                                 .$&X    :$&&&&$&&::;;xXX             
            XX;;;;;;;X&&X+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;x$$X;;;;;;+;;             
            ;;$&&x+++++x+++++++++++++++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;++;;;;XX;.:             
            ;:.;::. .  ...:+++++++++++;$&&&&&&$$$$$$$$$XXXXXXXXXXX+++++++++++++;;;;;;;;;;;:::             
           ::. .           .:::::::::.:&&X$&&&&$X$$&&&&$$&&&$$&$&&&........                 :.            
           ::.                ..      :&&X&&&&&&&&$$X$&&&&&&;&&;&&&.                       ..             
           :: ;;;;;;;;;;;;;;;;;;;;;;;;;X&&&&&&&&&&&&&&&&&&&&&&&&&&$;;;;;;;;;;;;;;;;;;;;;;;;               
           ..  ;;;;       ;;           .                         .           ;;       :;;;;               
                ;;;;      ;;;  ....:.. ;            :            ;          :;;       ;;;;                
                .;:;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;                                                                                                          
"""
    ]
    title = r"""  
 &&&&&  &&&& &&&&&&&&&&  &&&&&&&&&&X &&&&&&&&& &&&&   &&&& &&&&&&&&&&X &&&&&&&&&&  &&&&&&&&&& &&&&$  &&& 
 &&&&&  &&&& &&&&&&&&&&  &&&&&&&&&&X &&&&&&&&& &&&&   &&&& &&&&&&&&&&& &&&&&$&&&&& &&&&&&&&&& &&&&& &&&& 
 &&&&&&&&&&& &&&&   &&&$ && &&&& &&x &&&&&     &&&&&&&&&&& &&&     &&. &&&&   &&&& &&&&&      &&&&&&  
 XXXXX  XXXx XXXXXXXXXX;    XXXX     XXXXX     XXXX   XXXX XXXXXXXX    XXXXXXXXXXX XXXXX      XXXXXXXX 
 +++++  ++++ ++++   ++++    ++++     +++++++++ ++++   ++++ +++     +++ +++++  ++++ ++++++++++ ++++  ++++ 
 +++++  ++++ ++++   ++++    ++++     ;++++++x+ +++x   ++++ ++++++++++  +++++  ++++  +++++++++ ++++  ++++ 
                                                                                                     
"""

    with Live(console=console, refresh_per_second=20) as live:
        # Phase 1: Car drives in fast from right
        for i in range(width, 0, -4):
            frame = Text()
            padding = " " * i
            
            for line in car:
                frame.append(padding + line + "\n", style="bold cyan")
            
            live.update(Panel(frame, title="Hatchback", border_style="blue", height=16))
            time.sleep(0.05)
            
        # Phase 2: "Drift" stop (shake effect)
        for _ in range(10):
            frame = Text()
            shake = " " * random.randint(0, 2)
            for i, line in enumerate(car):
                # Only add smoke to the bottom lines (wheels)
                smoke = "  💨" if i >= len(car) - 3 else ""
                frame.append(shake + line + smoke + "\n", style="bold cyan")
            live.update(Panel(frame, title="Hatchback", border_style="blue", height=16))
            time.sleep(0.05)

        # Phase 3: Reveal Title
        final_frame = Text()
        for line in car:
            final_frame.append(line + "\n", style="bold cyan")
        final_frame.append(title, style="bold magenta")
        
        live.update(Panel(final_frame, title="Hatchback", border_style="blue", expand=False))
        time.sleep(0.5)


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
