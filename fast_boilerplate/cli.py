import os
import shutil
import sys
import argparse
import subprocess

def init_project():
    """
    Initializes a new FastAPI Alembic project.
    """
    parser = argparse.ArgumentParser(description="Initialize a new FastAPI Alembic project.")
    parser.add_argument("project_name", nargs="?", help="The name of the project (and directory) to create.")
    parser.add_argument("--install", action="store_true", help="Create venv and install requirements automatically.")
    parser.add_argument("--no-install", action="store_true", help="Do not create venv and install requirements.")
    parser.add_argument("--docker", action="store_true", help="Include Docker files.")
    parser.add_argument("--no-docker", action="store_true", help="Do not include Docker files.")
    
    args = parser.parse_args()
    
    # 1. Get Project Name
    project_name = args.project_name
    if not project_name:
        project_name = input("Enter project name (leave empty to use current directory): ").strip()

    # 2. Get Install Preference
    should_install = False
    if args.install:
        should_install = True
    elif args.no_install:
        should_install = False
    else:
        # Only ask if not specified via flags
        response = input("Create virtual environment and install requirements? (y/n) [y]: ").strip().lower()
        should_install = response in ["", "y", "yes"]

    # 3. Get Docker Preference
    should_include_docker = False
    if args.docker:
        should_include_docker = True
    elif args.no_docker:
        should_include_docker = False
    else:
        response = input("Include Docker files (Dockerfile, docker-compose.yml)? (y/n) [y]: ").strip().lower()
        should_include_docker = response in ["", "y", "yes"]

    # 4. Define paths
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(package_dir, "template")
    
    if project_name:
        target_dir = os.path.join(os.getcwd(), project_name)
    else:
        target_dir = os.getcwd()
    
    print(f"\nInitializing new project in {target_dir}...")
    
    try:
        # 5. Copy Files
        # dirs_exist_ok=True allows copying into an existing directory (Python 3.8+)
        shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
        
        # Remove Docker files if not requested
        if not should_include_docker:
            docker_files = ["Dockerfile", "docker-compose.yml"]
            for f in docker_files:
                f_path = os.path.join(target_dir, f)
                if os.path.exists(f_path):
                    os.remove(f_path)

        # 6. Install Dependencies (if requested)
        if should_install:
            print("Creating virtual environment...")
            venv_dir = os.path.join(target_dir, "venv")
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            
            print("Installing requirements...")
            if os.name == 'nt':
                pip_exe = os.path.join(venv_dir, "Scripts", "pip")
            else:
                pip_exe = os.path.join(venv_dir, "bin", "pip")
                
            requirements_file = os.path.join(target_dir, "requirements.txt")
            subprocess.run([pip_exe, "install", "-r", requirements_file], check=True)
            print("Dependencies installed successfully!")
        
        # 7. Print Success and Next Steps
        print("\nProject initialized successfully!")
        print("\nNext steps:")
        if project_name:
            print(f"- cd {project_name}")
        
        if should_include_docker:
            print("- docker-compose up -d --build")
        else:
            if not should_install:
                print("- python -m venv venv")
                print("- source venv/bin/activate (or venv\\Scripts\\activate)")
                print("- pip install -r requirements.txt")
            else:
                print("- source venv/bin/activate (or venv\\Scripts\\activate)")
                
            print("- Configure .env (copy from .env.example if you create one)")
            print("- alembic revision --autogenerate -m 'init'")
            print("- alembic upgrade head")
            print("- uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"Error initializing project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_project()
