import os
from subprocess import check_call


def setup(loader, variant=None):
    _, variant = loader.setup_project_env(None, variant)
    venv_type = loader.setup_virtualenv()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    odoo_dir = os.path.join(loader.config['work_dir'],
            config.get('odoo_dir', 'lib/odoo'))

    binargs = [python_bin, 'setup.py', 'install']
    if venv_type == 'python':
        binargs.append('--user')

    check_call(binargs, cwd=odoo_dir)
