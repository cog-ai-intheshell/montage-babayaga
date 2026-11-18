#!/usr/bin/env python3
"""Install the Python runtime inside this skill, without changing system Python."""
from pathlib import Path
import os
import subprocess
import sys
import venv


def main():
    root = Path(__file__).resolve().parents[1]
    env = root / '.venv'
    python = env / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(env)
    subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                    '-r', str(root / 'requirements.txt')], check=True)
    subprocess.run([str(python), '-c', 'import numpy, PIL, onnxruntime; '
                    'print("Runtime Babayaga prêt.")'], check=True)
    print(python)


if __name__ == '__main__':
    main()
