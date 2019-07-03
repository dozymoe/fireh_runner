""" Python module.
"""
import os

def python(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    python_bin = loader.get_python_bin()

    binargs = [python_bin] + list(args)
    os.execvp(binargs[0], binargs)


commands = (python,)
