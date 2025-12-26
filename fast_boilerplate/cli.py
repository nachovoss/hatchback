import os
import shutil
import sys
import argparse

def init_project():
    """
    Initializes a new FastAPI Alembic project.
    """
    parser = argparse.ArgumentParser(description="Initialize a new FastAPI Alembic project.")
    parser.add_argument("project_name", nargs="?", help="The name of the project (and directory) to create.")
    
    args = parser.parse_args()
    
    project_name = args.project_name
    
    if not project_name:
        project_name = input("Enter project name (leave empty to use current directory): ").strip()

    # Get the directory where this script is located
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(package_dir, "template")
    
    if project_name:
        target_dir = os.path.join(os.getcwd(), project_name)
    else:
        target_dir = os.getcwd()
    
    print(f"Initializing new project in {target_dir}...")
    
    try:
        # Copy all files from template_dir to target_dir
        # dirs_exist_ok=True allows copying into an existing directory (Python 3.8+)
        shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
        
        print("Project initialized successfully!")
        print("\nNext steps:")
        if project_name:
            print(f"cd {project_name}")
        print("1. python -m venv venv")
        print("2. source venv/bin/activate (or venv\\Scripts\\activate)")
        print("3. pip install -r requirements.txt")
        print("4. Configure .env (copy from .env.example if you create one)")
        print("5. alembic revision --autogenerate -m 'init'")
        print("6. alembic upgrade head")
        print("7. uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"Error initializing project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_project()
