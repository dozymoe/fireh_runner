"""Pip module.

Pip is python package manager.
"""
import os
import shlex

def pip(loader, *args):
    """Install or uninstall python packages."""
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    binargs = ['pip'] + list(args)
    os.execvp(binargs[0], binargs)


def pip_install(loader, *args):
    """Install or uninstall python packages."""
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    cmds_pip_install = ['pip', 'install']
    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    binargs = cmds_pip_install + list(args)
    os.execvp(binargs[0], binargs)


commands = (pip, pip_install)
