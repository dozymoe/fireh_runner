import os
from subprocess import check_call


def setup(loader, variant):
    venv_type = loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    project, variant = loader.setup_project_env(None, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    odoo_dir = os.path.join(loader.config['work_dir'],
            config.get('odoo_dir', 'lib/odoo'))

    binargs = [python_bin, 'setup.py', 'install']
    if venv_type == 'python':
        binargs.append('--user')

    os.chdir(odoo_dir)
    check_call(binargs)
