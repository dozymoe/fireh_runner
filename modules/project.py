""" Generic project helper.
"""
import os

def python_project(loader, project, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """Execute project as a python package."""
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    python_bin = loader.get_python_bin()

    binargs = [python_bin, '-m', project] + list(args)
    os.execvp(binargs[0], binargs)


commands = (python_project,)
