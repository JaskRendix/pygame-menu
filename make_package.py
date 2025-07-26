"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUILD
Build file.
"""

import os
import shutil
import sys

assert len(sys.argv) == 2, 'Argument is required, usage: make_package.py pip/twine'
mode = sys.argv[1].strip()

def clean_dist():
    if os.path.isdir('dist'):
        for k in os.listdir('dist'):
            if 'pygame_menu-' in k or 'pygame-menu-' in k:
                os.remove(os.path.join('dist', k))

def clean_build():
    if os.path.isdir('build'):
        for k in os.listdir('build'):
            if 'bdist.' in k or k == 'lib':
                shutil.rmtree(os.path.join('build', k))

if mode == 'pip':
    clean_dist()
    clean_build()
    print("Building with pyproject.toml ...")
    os.system('python -m build')

elif mode == 'twine':
    if os.path.isdir('dist'):
        print("Uploading to PyPI ...")
        os.system('python -m twine upload dist/*')
    else:
        raise FileNotFoundError('No distribution found. Run: make_package.py pip')

else:
    raise ValueError(f'Unknown mode: {mode}')
