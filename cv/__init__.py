""" cv python module, cross-platform for Windows and Linux. """

import os
import platform
import shutil
import subprocess
import sys

from pathlib import Path

DIR_VIRT = "venv"
PLATFORM = platform.system()
PATH_SCRIPTS = Path(Path(__file__).resolve().parent, "scripts")

if PLATFORM == "Darwin":
  print(
    "Not supporting Mac due lack of hardware access for testing.",
    file=sys.stderr
  )
  sys.exit(-1)

PATH_VIRT = Path(DIR_VIRT)
PY = Path(
  PATH_VIRT, *("bin", "python") if PLATFORM == "Linux" else ("Script","python.exe")
)
PATH_BIN = PY.parent
PATH_ACTIVATE_THIS = Path(PATH_BIN, "activate_this.py")

def call(command):
  """ Wrapper around subprocess call with auto-splitting. """
  if type(command) == str:
    command = command.split()
  return subprocess.call(command)

def load_virt():
  """ Load the virtual environment for running process. """
  with open(PATH_ACTIVATE_THIS, 'r') as fh:
    exec(fh.read(), {'__file__': PATH_ACTIVATE_THIS})

if not PATH_VIRT.is_dir():
  # Create virtual environment.
  call(f"python -m venv {PATH_VIRT}")
  # Copy the activate_this.py, lifted from virtualenv.
  shutil.copyfile(Path(PATH_SCRIPTS, "activate_this.py"), PATH_ACTIVATE_THIS)
  load_virt()
  # Upgrade pip.
  call(f"{PY} -m pip install --upgrade pip")
  # Install dependencies.
  call(f"{PY} -m pip install -r requirements.txt")
else:
  load_virt()
