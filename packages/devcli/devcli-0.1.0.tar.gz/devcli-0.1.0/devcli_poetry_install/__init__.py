import os
from pathlib import Path

import subprocess


def install_script(path: Path):
    print(path)
    if (path/'pyproject.toml').exists():

        p = subprocess.Popen(['poetry', 'install'], cwd=path.absolute())
        p.wait()
        print('bla')