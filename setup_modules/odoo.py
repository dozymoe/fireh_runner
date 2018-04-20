import os
from subprocess import check_call


def setup(loader, variant):
    venv_type = loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    work_dir = os.path.join(loader.config['work_dir'], 'lib', 'odoo')

    binargs = [python_bin, 'setup.py', 'install']
    if venv_type == 'python':
        binargs.append('--user')

    os.chdir(work_dir)
    check_call(binargs)
