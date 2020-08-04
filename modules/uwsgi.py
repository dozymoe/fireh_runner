"""uwsgi-for-Django module.

Website: https://uwsgi-docs.readthedocs.io/en/latest/
"""
import os

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


commands = (uwsgi, uwsgi_run)
