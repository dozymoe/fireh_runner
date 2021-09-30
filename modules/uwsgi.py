"""uwsgi-for-Django module.

Website: https://uwsgi-docs.readthedocs.io/en/latest/
"""
import os
import shutil
import subprocess
import sys

def uwsgi(loader, *args):
    loader.setup_virtualenv()
    venv_dir = loader.get_virtualenv_dir()
    binargs = [os.path.join(venv_dir, 'bin', 'uwsgi')] + list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_run(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    venv_dir = loader.get_virtualenv_dir()
    binargs = [os.path.join(venv_dir, 'bin', 'uwsgi'), '--master',
            '--die-on-term']
    if not loader.is_production():
        binargs.append('--honour-stdin')

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)
    os.chdir(work_dir)

    binargs += list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_build_cheaper2(loader):
    url = 'https://github.com/KLab/uwsgi-cheaper-spare2'
    exe = sys.argv[0]
    workdir = os.path.dirname(exe)
    subprocess.check_call([exe, 'uwsgi', f'--build-plugin={url}'])
    # cleanup
    tmpdir = os.path.join(workdir, '.uwsgi_plugins_builder')
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)
    tmpdir = os.path.join(workdir, 'uwsgi-cheaper-spare2')
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


commands = (uwsgi, uwsgi_run, uwsgi_build_cheaper2)
