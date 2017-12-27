import os
from subprocess import check_call


def setup(loader, variant):
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    work_dir = os.path.join(loader.config['work_dir'], 'lib', 'odoo')

    binargs = [python_bin, 'setup.py', 'install', '--user']
    os.chdir(work_dir)
    check_call(binargs)
