import glob
import os
from subprocess import check_call


def setup(loader, variant=None):
    _, variant = loader.setup_project_env(None, variant)
    venv_type = loader.setup_virtualenv()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    odoo_dir = os.path.join(loader.config['work_dir'],
            config.get('odoo_dir', 'lib/odoo'))

    # Is directory writable?
    if os.access(odoo_dir, os.W_OK):
        binargs = [python_bin, 'setup.py', 'install']
        if venv_type == 'python':
            binargs.append('--user')

        return check_call(binargs, cwd=odoo_dir)

    odoo_ver = config.get('odoo_version')
    if odoo_ver:
        # Check sdist of specific version.
        filename = os.path.join(odoo_dir, 'dist', 'odoo-%s.0.tar.gz' % odoo_ver)
        if not os.path.exists(filename):
            filename = None
    else:
        # Check any sdist.
        files = glob.glob(os.path.join(odoo_dir, 'dist', 'odoo-*.tar.gz'))
        if files:
            # Get latest version.
            files.sort(reverse=True)
            filename = files[0]
        else:
            filename = None

    if not filename:
        raise RuntimeError("Odoo directory is not writable for setup.py and "
                "source dist tarball not found.")

    binargs = [python_bin, '-m', 'pip', 'install', filename]
    if venv_type == 'python':
        binargs.append('--user')

    return check_call(binargs)
