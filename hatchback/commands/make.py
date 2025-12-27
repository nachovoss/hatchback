import os
from ..utils import console, to_pascal_case

def handle_make(args):
    resource = args.resource.lower()
    Resource = to_pascal_case(resource)
    
    console.print(f"[bold green]Scaffolding resource: {Resource}[/bold green]")
    
    # Define paths
    base_dir = os.getcwd()
    app_dir = os.path.join(base_dir, "app")
    
    if not os.path.exists(app_dir):
        console.print("[bold red]Error: 'app' directory not found. Are you in the project root?[/bold red]")
        return

    # Locate templates directory
    # __file__ is .../hatchback/commands/make.py
    # os.path.dirname(__file__) is .../hatchback/commands
    # os.path.dirname(...) is .../hatchback
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(package_dir, "scaffold_templates")

    files_map = {
        "model.tpl": f"app/models/{resource}.py",
        "schema.tpl": f"app/schemas/{resource}.py",
        "repository.tpl": f"app/repositories/{resource}.py",
        "service.tpl": f"app/services/{resource}.py",
        "route.tpl": f"app/routes/{resource}.py",
        "test.tpl": f"tests/test_{resource}s.py",
    }

    for tpl_file, target_path in files_map.items():
        tpl_path = os.path.join(templates_dir, tpl_file)
        if not os.path.exists(tpl_path):
            console.print(f"[bold red]Error: Template {tpl_file} not found at {tpl_path}[/bold red]")
            continue

        with open(tpl_path, "r") as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace("__Resource__", Resource)
        content = content.replace("__resource__", resource)
        
        full_target_path = os.path.join(base_dir, target_path)
        os.makedirs(os.path.dirname(full_target_path), exist_ok=True)
        
        if os.path.exists(full_target_path):
             console.print(f"[yellow]Skipping {target_path} (already exists)[/yellow]")
        else:
            with open(full_target_path, "w") as f:
                f.write(content)
            console.print(f"[green]Created {target_path}[/green]")

    # Update models/__init__.py
    init_path = os.path.join(app_dir, "models", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "a") as f:
            f.write(f"\nfrom app.models.{resource} import {Resource}")
        console.print(f"[green]Updated app/models/__init__.py[/green]")
