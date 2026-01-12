import os
import subprocess
import sys
import re
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from ..utils import console, to_pascal_case
import shutil
from sqlalchemy import create_engine, inspect
from .make import scaffold_resource

def handle_inspect(args):
    """
    Inspect an existing database and generate SQLAlchemy models.
    """
    console.print(Panel("Database Inspector", style="bold blue"))

    # Try to load .env to get default DB connection if not provided
    db_url = args.url
    if not db_url:
        # Check for .env file
        env_path = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_path):
            from dotenv import load_dotenv
            load_dotenv(env_path)
            
            db_user = os.getenv("DATABASE_USERNAME", "postgres")
            db_password = os.getenv("DATABASE_PASSWORD", "postgres")
            db_host = os.getenv("DATABASE_HOSTNAME", "localhost")
            db_port = os.getenv("DATABASE_PORT", "5432")
            db_name = os.getenv("DATABASE_NAME", "app_db") # default in init.py
            
            # Construct default URL for suggestion
            default_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            default_url = "postgresql://user:password@localhost/dbname"

        db_url = Prompt.ask("[bold green]Enter Database URL[/bold green]", default=default_url)

    if args.scaffold:
        # Full automatic scaffold mode
        try:
            engine = create_engine(db_url)
            console.print(f"[bold green]Connecting to {db_url}...[/bold green]")
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            console.print(f"[bold green]Found {len(tables)} tables: {', '.join(tables)}[/bold green]")
            
            if not Confirm.ask("Do you want to scaffold all these tables?"):
                return

            # Create mapping for singularization
            # table_name -> SingularClassName
            table_to_class = {}
            for t in tables:
                if t == "alembic_version": continue
                res_name = t[:-1] if t.endswith('s') else t
                table_to_class[t] = to_pascal_case(res_name)

            for table in tables:
                if table == "alembic_version": continue
                
                # Simple singularization: remove 's' at end if present
                resource = table[:-1] if table.endswith('s') else table
                TargetClass = to_pascal_case(resource)
                
                console.print(f"\nProcessing table [cyan]{table}[/cyan] -> resource [green]{resource}[/green] (Class: {TargetClass})")
                
                # 1. Scaffold files (Service, Repo, Route, etc.)
                # This creates app/models/resource.py too, but we will overwrite it
                scaffold_resource(resource)
                
                # 2. Overwrite model with sqlacodegen for just this table
                model_path = os.path.join(os.getcwd(), f"app/models/{resource}.py")
                
                # We use --nobase if available, or just handle stripping
                # sqlacodegen doesn't have --nobase by default in all versions.
                # using subprocess to run it
                cmd = [
                    "sqlacodegen",
                    db_url,
                    "--tables", table,
                    "--outfile", model_path
                ]
                
                # Fallback mechanism for running sqlacodegen
                if not shutil.which("sqlacodegen"):
                    cmd = [sys.executable, "-m", "sqlacodegen", db_url, "--tables", table, "--outfile", model_path]

                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    console.print(f"  [green]Generated model from DB for {table}[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"  [red]Failed to generate model for {table}: {e}[/red]")
                    continue

                # 3. Post-process model file to fix Base and imports
                try:
                    with open(model_path, 'r') as f:
                        content = f.read()

                    lines = content.splitlines()
                    
                    # Separate imports and class logic
                    raw_imports = []
                    class_lines = []
                    
                    is_processing_class = False
                    is_target_class = False
                    current_class_buffer = []
                    
                    for line in lines:
                        stripped = line.strip()
                        
                        # Collect imports
                        if line.startswith("import ") or line.startswith("from "):
                            if "declarative_base" in line or "Base =" in line:
                                continue 
                            if "create_engine" in line or "engine =" in line:
                                continue
                            if "app.config.database" in line: # Avoid duplicating if somehow present
                                continue
                            raw_imports.append(line)
                            continue

                        # Detect Class Start
                        if line.startswith("class "):
                            # If we were processing a class, and it was the target, save it
                            if current_class_buffer and is_target_class:
                                class_lines.extend(current_class_buffer)
                                # Only one class per file in this architecture
                                pass

                            # Start new buffer
                            current_class_buffer = [line]
                            is_processing_class = True
                            is_target_class = False # Reset
                            
                            if "class Base" in line:
                                is_processing_class = False
                                current_class_buffer = []

                        elif is_processing_class:
                           current_class_buffer.append(line)
                           if "__tablename__ =" in line:
                                extracted = line.split("=")[1].strip().strip("'").strip('"')
                                if extracted == table:
                                    is_target_class = True
                    
                    # Flush last buffer
                    if current_class_buffer and is_target_class:
                        class_lines.extend(current_class_buffer)

                    # Optimize Imports
                    class_content = "\n".join(class_lines)
                    final_imports = ["from app.config.database import Base"]
                    
                    for imp in raw_imports:
                        # Simple unused import removal
                        # Case 1: from X import A, B, C
                        if "import " in imp and "from " in imp:
                            parts = imp.split(" import ")
                            module_part = parts[0]
                            names_part = parts[1]
                            
                            # remove comments if any
                            names_part = names_part.split("#")[0].strip()
                            
                            # parse names (careful with parens which sqlacodegen uses for long imports)
                            # sqlacodegen generated imports are usually clean single lines or parens
                            # Simple regex approach to find words
                            import_names = [n.strip() for n in names_part.replace("(", "").replace(")", "").split(",") if n.strip()]
                            
                            used_names = []
                            for name in import_names:
                                # Check usage whole word
                                if re.search(r'\b' + re.escape(name) + r'\b', class_content):
                                    used_names.append(name)
                            
                            if used_names:
                                final_imports.append(f"{module_part} import {', '.join(sorted(used_names))}")
                                
                        # Case 2: import X
                        elif imp.startswith("import "):
                             name = imp.split("import ")[1].strip()
                             if re.search(r'\b' + re.escape(name) + r'\b', class_content):
                                 final_imports.append(imp)

                    # Assemble final file
                    # Imports + 2 blank lines + Class
                    class_content = "\n".join(class_lines)
                    
                    # Fix Class Name Mismatch (Plural -> Singular)
                    # sqlacodegen uses PascalCase(table_name). e.g. 'users' -> 'Users', 'shifts' -> 'Shifts'
                    # We want 'User', 'Shift'
                    # We also need to fix relationships: related classes will be 'Shifts', 'Tenants'
                    # We need to map them to 'Shift', 'Tenant'
                    
                    # 1. Rename the class definition
                    # Find "class Plural(Base):" and replace with "class Singular(Base):"
                    # We don't know exactly what sqlacodegen generated, but it usually matches table name
                    # We can try to regex replace the class definition line we found
                    
                    # A safer way is to just replace the class name if it starts with "class "
                    # But we need to know the old name.
                    # We can parse it from class_lines[0] usually
                    
                    old_class_name = None
                    for i, l in enumerate(class_lines):
                        if l.startswith("class "):
                            old_class_name = l.split("class ")[1].split("(")[0]
                            # Replace with TargetClass
                            class_lines[i] = l.replace(f"class {old_class_name}", f"class {TargetClass}")
                            break
                    
                    class_content = "\n".join(class_lines)

                    # 2. Fix Relationship types
                    # Replace Mapped['OldName'] with Mapped['NewName']
                    # Replace relationship('OldName') with relationship('NewName')
                    
                    for t_name, new_cls_name in table_to_class.items():
                         # sqlacodegen likely used PascalCase(t_name)
                         # e.g. t_name='tenants' -> likely 'Tenants'
                         # We can try strict checking but usually Capitalizing first letter is enough if table is lower
                         # or removing underscores
                         
                         # Heuristic: convert table name to pascal case to guess what sqlacodegen did
                         # e.g. 'users' -> 'Users'. 'user_roles' -> 'UserRoles'.
                         # This usually matches to_pascal_case(t_name)
                         
                         probable_old_class = to_pascal_case(t_name)
                         
                         if probable_old_class != new_cls_name:
                             # Replace string references
                             # relationship('Old') -> relationship('New')
                             class_content = class_content.replace(f"'{probable_old_class}'", f"'{new_cls_name}'")
                             class_content = class_content.replace(f'"{probable_old_class}"', f'"{new_cls_name}"')
                             class_content = class_content.replace(f"[{probable_old_class}]", f"[{new_cls_name}]") # for List[Old]
                             # Also Mapped['Old']
                             class_content = class_content.replace(f"Mapped['{probable_old_class}']", f"Mapped['{new_cls_name}']")

                    final_content = "\n".join(final_imports) + "\n\n\n" + class_content + "\n"
                    
                    with open(model_path, 'w') as f:
                        f.write(final_content)
                        
                except Exception as e:
                     console.print(f"  [yellow]Warning: Could not post-process model file: {e}[/yellow]")

            console.print("\n[bold green]✅ Full scaffold complete![/bold green]")
            console.print("Don't forget to review the generated models and schemas.")
            return

        except Exception as e:
            console.print(f"[bold red]Error inspecting database: {e}[/bold red]")
            return

    # Non-scaffold mode (just dump models to one file)
    # Output file
    output_file = args.output
    if not output_file:
        output_file = Prompt.ask("[bold green]Enter output file path[/bold green]", default="app/models/imported.py")

    # Check if sqlacodegen is available
    if not shutil.which("sqlacodegen"):
        console.print("[yellow]sqlacodegen not found in PATH. Attempting to install or run via python -m...[/yellow]")
        # In a real scenario, we might want to pip install it or ensure it's in the hatchback env
        # Since we added it to setup.py, it should be available where hatchback is running.
    
    console.print(f"[bold green]Running sqlacodegen against {db_url}...[/bold green]")
    
    cmd = [
        "sqlacodegen",
        db_url,
        "--outfile", output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        console.print(f"[bold green]✅ Models generated successfully in {output_file}[/bold green]")
        console.print("[dim]Note: You may need to adjust the generated models to match your project structure (e.g. inheriting from your project's Base).[/dim]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error running sqlacodegen: {e}[/bold red]")
    except FileNotFoundError:
        # Fallback: try running with current python executable
        try:
             # This assumes sqlacodegen is installed in the same env as hatchback
            cmd = [sys.executable, "-m", "sqlacodegen", db_url, "--outfile", output_file]
            subprocess.run(cmd, check=True)
            console.print(f"[bold green]✅ Models generated successfully in {output_file}[/bold green]")
        except Exception as e:
            console.print("[bold red]Could not find or run sqlacodegen. Please ensure it is installed.[/bold red]")
            console.print(f"[red]{e}[/red]")

