#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path
import venv

ROOT = Path(__file__).parent.resolve()
VENV_DIR = ROOT / ".venv"

def create_venv():
    if not VENV_DIR.exists():
        venv.create(VENV_DIR, with_pip=True)
        print("Created venv")

def run_pip_install():
    pip_exe = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "pip"
    if (ROOT / "requirements.txt").exists():
        subprocess.check_call([str(pip_exe), "install", "-r", str(ROOT / "requirements.txt")])

def start_app():
    py_exe = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "python"
    # start app in a new process
    proc = subprocess.Popen([str(py_exe), "app.py"], cwd=str(ROOT))
    return proc

def main():
    create_venv()
    run_pip_install()
    proc = start_app()
    time.sleep(1)
    webbrowser.open("http://localhost:5000")
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()

if __name__ == "__main__":
    main()
