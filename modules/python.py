""" Python module.
"""
import os

def pip(loader, project=None, variant=None, *args):
    """Install or uninstall python packages."""
    loader.setup_project_env(project, variant)
    venv_type = loader.setup_virtualenv()
    loader.setup_shell_env()
    python_bin = loader.get_python_bin()

    pip_args = list(args)
    for arg in args:
        if arg.startswith('-'):
            continue
        if arg == 'install':
            if venv_type == 'python':
                pip_args.append('--user')
            pip_args.extend(loader.config.get('pip_install_args', []))

        elif arg == 'freeze':
            if venv_type == 'python':
                pip_args.append('--user')
        else:
            break

    binargs = [python_bin, '-m', 'pip'] + pip_args
    os.execvp(binargs[0], binargs)


def python(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """Python shell."""
    project_selected = project is not None
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    python_bin = loader.get_python_bin()

    if project_selected:
        config = loader.get_project_config()
        work_dir = config.get('work_dir', project)
        work_dir = loader.expand_path(work_dir)
        os.chdir(work_dir)

    binargs = [python_bin] + list(args)
    os.execvp(binargs[0], binargs)


commands = (pip, python)
