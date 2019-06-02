""" Run any executable in virtualenv/bin directory.
"""
import os

def bin(loader, project=None, variant=None, *args): #pylint:disable=redefined-builtin
    """ Run executable in virtualenv bin
    """
    loader.setup_virtualenv()
    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    venv_dir = loader.get_virtualenv_dir()
    binargs = [os.path.join(venv_dir, 'bin', args[0])] + args[1:]
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def pybin(loader, project=None, variant=None, *args):
    """ Run executable in virtualenv bin
    """
    loader.setup_virtualenv()
    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = loader.get_binargs(args[0], *args[1:])
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def lsbin(loader):
    """ List executables in virtualenv bin
    """
    bin_dir = os.path.join(loader.get_virtualenv_dir(), 'bin')
    for fname in os.listdir(bin_dir):
        path = os.path.realpath(os.path.join(bin_dir, fname))
        if not os.path.isfile(path):
            continue
        if os.stat(path).st_mode & (os.st.S_IXUSR | os.st.S_IXGRP\
                | os.st.S_IXOTH):
            print(fname)


commands = (bin, lsbin, pybin)
