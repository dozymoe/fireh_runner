"""Pip module.

Pip is python package manager.
"""
import os
try:
    import xmlrpclib # pylint:disable=unused-import
except ImportError:
    import xmlrpc.client as xmlrpclib # pylint:disable=unused-import


def pip(loader, *args):
    """Install or uninstall python packages."""
    loader.setup_virtualenv()

    binargs = ['pip'] + list(args)
    os.execvp(binargs[0], binargs)


def pip_install(loader, save=None, *args):
    """Install python packages."""
    loader.setup_virtualenv()

    cmds_pip_install = ['pip', 'install']
    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    binargs = cmds_pip_install + list(args)
    os.execvp(binargs[0], binargs)


def pip_uninstall(loader, save=None, *args):
    """Uninstall python packages."""
    loader.setup_virtualenv()

    cmds_pip_install = ['pip', 'uninstall']

    binargs = cmds_pip_install + list(args)
    os.execvp(binargs[0], binargs)


commands = (pip, pip_install, pip_uninstall)
