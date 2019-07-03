"""Doxygen module.

Create project's documentation.

Website: http://www.doxygen.org
"""
import os

def doxygen(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = ['doxygen', config['doxygen.config']] + list(args)
    os.execvp(binargs[0], binargs)


commands = (doxygen,)
