#!/usr/bin/env python
"""
Jarvis AI Voice Assistant - Quick Start Script
Run this script to automatically set up Jarvis
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print colored header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def run_command(command, description):
    """Run command and check for errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Done!")
            return True
        else:
            print(f"❌ {description} - Failed!")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python():
    """Check Python version"""
    print_header("Checking Python Installation")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required!")
        sys.exit(1)
    print("✅ Python version OK")

def create_venv():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    is_windows = platform.system() == "Windows"
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists at {venv_path}")
        return True
    
    if run_command(f"python -m venv {venv_path}", "Creating virtual environment"):
        print()
        print("Virtual environment created!")
        if is_windows:
            print(f"To activate: {venv_path}\\Scripts\\activate")
        else:
            print(f"To activate: source {venv_path}/bin/activate")
        return True
    return False

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    is_windows = platform.system() == "Windows"
    pip_cmd = "pip" if is_windows else "pip3"
    
    if run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements")
    return False

def setup_database():
    """Set up database"""
    print_header("Setting Up Database")
    
    is_windows = platform.system() == "Windows"
    py_cmd = "python" if is_windows else "python3"
    
    success = True
    success = run_command(f"{py_cmd} manage.py makemigrations", "Creating migrations") and success
    success = run_command(f"{py_cmd} manage.py migrate", "Applying migrations") and success
    success = run_command(f"{py_cmd} manage.py collectstatic --noinput", "Collecting static files") and success
    
    return success

def create_superuser():
    """Create admin user"""
    print_header("Creating Admin User")
    
    is_windows = platform.system() == "Windows"
    py_cmd = "python" if is_windows else "python3"
    
    print("You will now create an admin account...")
    print("(You can use: admin / admin@example.com / password123)")
    print()
    
    os.system(f"{py_cmd} manage.py createsuperuser")
    return True

def print_final_message():
    """Print final instructions"""
    print_header("Setup Complete! 🎉")
    
    print("""
Your Jarvis AI Voice Assistant is ready!

Next steps:
1. Start the server:
   python manage.py runserver

2. Open in browser:
   http://localhost:8000

3. Allow microphone access when prompted

4. Say "Jarvis" to activate, then give commands!

5. Access admin panel:
   http://localhost:8000/admin

Admin commands:
- "Jarvis, open YouTube"
- "Jarvis, what time is it?"
- "Jarvis, tell me a joke"
- "Jarvis, search for [query]"

For help: Read SETUP_GUIDE.md or README.md

Enjoy your personal AI assistant! 🤖
    """)

def main():
    """Main setup flow"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║       JARVIS AI VOICE ASSISTANT - SETUP SCRIPT         ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    steps = [
        ("Python version check", check_python),
        ("Virtual environment", create_venv),
        ("Install dependencies", install_dependencies),
        ("Database setup", setup_database),
        ("Create admin user", create_superuser),
    ]
    
    for i, (name, step_func) in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {name}")
        try:
            if not step_func():
                print(f"\n❌ Setup failed at: {name}")
                print("Try running the failing step manually.")
                sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error during setup: {e}")
            sys.exit(1)
    
    print_final_message()

if __name__ == "__main__":
    main()
