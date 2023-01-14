"""uwsgi-for-Django module.

Website: https://uwsgi-docs.readthedocs.io/en/latest/
"""
import os
import shutil
import subprocess

def _find_uwsgi_bin(loader):
    venv_dir = loader.get_virtualenv_dir()
    uwsgi_bin = os.path.join(venv_dir, 'bin', 'uwsgi')
    if os.path.exists(uwsgi_bin):
        return [uwsgi_bin]
    uwsgi_bin = shutil.which('uwsgi')
    if os.path.exists(uwsgi_bin):
        return [uwsgi_bin, '--plugin=python3']
    raise Exception("Cannot find uwsgi binary.\n")


def uwsgi(loader, *args):
    loader.setup_virtualenv()
    binargs = _find_uwsgi_bin(loader) + list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_run(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = _find_uwsgi_bin(loader) + ['--master', '--die-on-term']
    if not loader.is_production():
        binargs.append('--honour-stdin')

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)
    os.chdir(work_dir)

    binargs += list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_build_cheaper2(loader):
    url = 'https://github.com/KLab/uwsgi-cheaper-spare2'
    loader.setup_virtualenv()
    binargs = _find_uwsgi_bin(loader) + [f'--build-plugin={url}']

    subprocess.check_call(binargs)
    # cleanup
    if os.path.exists('.uwsgi_plugins_builder'):
        shutil.rmtree('.uwsgi_plugins_builder')
    if os.path.exists('uwsgi-cheaper-spare2'):
        shutil.rmtree('uwsgi-cheaper-spare2')


commands = (uwsgi, uwsgi_run, uwsgi_build_cheaper2)
