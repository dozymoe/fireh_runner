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
    python_bin = loader.get_python_bin()

    pip_args = list(args)
    for arg in args:
        if arg.startswith('-'):
            continue
        elif arg == 'install' or arg == 'freeze':
            pip_args.append('--user')
        else:
            break

    binargs = [python_bin, '-m', 'pip'] + pip_args
    os.execvp(binargs[0], binargs)


def pip_install(loader, save=None, *args):
    """Install python packages."""
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    cmds_pip_install = [python_bin, '-m', 'pip', 'install', '--user']
    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    binargs = cmds_pip_install + list(args)
    os.execvp(binargs[0], binargs)


def pip_uninstall(loader, save=None, *args):
    """Uninstall python packages."""
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    cmds_pip_uninstall = [python_bin, '-m', 'pip', 'uninstall']

    binargs = cmds_pip_uninstall + list(args)
    os.execvp(binargs[0], binargs)


commands = (pip, pip_install, pip_uninstall)
