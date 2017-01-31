"""Waf setup virtualenv and project."""
import os
from shutil import rmtree
from subprocess import check_call
import sys

def setup(loader, variant=None):
    """Setup virtualenv and project."""

    if variant is None:
        variant = os.environ.get('PROJECT_VARIANT',
                loader.config['default_variant'])

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})

    work_dir = loader.config['work_dir']
    python_version = loader.config['python_version']

    venv_dir = os.path.realpath(os.path.join(work_dir,
            loader.config['virtualenv_dir']))

    if os.path.exists(venv_dir):
        rmtree(venv_dir)

    check_call(['virtualenv', '--python=python' + python_version, venv_dir])

    modules_link = os.path.abspath(os.path.join(work_dir, 'python_modules'))

    if os.path.exists(modules_link):
        os.remove(modules_link)

    os.symlink(os.path.join(venv_dir, 'lib', 'python' + python_version,
            'site-packages'), modules_link)

    os.environ['PATH'] = os.path.join(venv_dir, 'bin') + ':' +\
            os.environ['PATH']

    sys.path.insert(1, modules_link)

    check_call(['pip', 'install', '--upgrade', 'pip'])

    if os.path.exists(os.path.join(work_dir, 'requirements.txt')):
        check_call(['pip', 'install', '-r', os.path.join(work_dir,
                'requirements.txt')])

    for python_pkg in config.get('python_modules', []):
        check_call(['pip', 'install', python_pkg])

    if os.path.exists(os.path.join(work_dir, '.git')):
        check_call(['git', 'submodule', 'update', '--init', '--recursive'])

    if os.path.exists(os.path.join(work_dir, 'package.json')):
        check_call(['npm', 'install'])

    if os.path.exists(os.path.join(work_dir, 'bower.json')):
        check_call(['bower', 'install'])

    if os.path.exists(os.path.join(work_dir, 'wscript')):
        check_call(['waf', 'configure'])
        check_call(['waf', 'clean', 'build'])

    if os.path.exists(os.path.join(work_dir, 'alembic.ini')):
        check_call(['alembic', 'upgrade', 'head'])


commands = (setup,)
