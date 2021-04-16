import os
from shutil import copyfile, rmtree
from subprocess import check_call
import sys


def setup(loader, variant):
    work_dir = loader.config['work_dir']
    python_bin = loader.get_python_bin()
    use_symlink = not loader.config.get('no_symlink_please', False)

    if use_symlink:
        link_fn = loader.force_symlink
    else:
        link_fn = copyfile

    ## python virtualenv

    venv_type = loader.config.get('virtualenv_type', 'python')
    venv_dir = loader.get_virtualenv_dir()

    if os.path.exists(venv_dir):
        rmtree(venv_dir, ignore_errors=True)

    if venv_type == 'venv':
        check_call([python_bin, '-m', 'venv', venv_dir])
    elif venv_type == 'virtualenv':
        check_call([python_bin, '-m', 'virtualenv', venv_dir])

    loader.setup_virtualenv()
    python_bin = loader.get_python_bin(cache=False)

    cmds_pip_install = [python_bin, '-m', 'pip', 'install']
    if venv_type == 'python':
        cmds_pip_install.append('--user')

    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    ## update python pip

    check_call(cmds_pip_install + ['--upgrade', 'pip', 'wheel'])

    ## python requirements.txt

    reqtxt_path = os.path.join(work_dir, 'requirements.txt')
    reqtxt_var_path = os.path.join(work_dir, 'requirements-%s.txt' % variant)
    if os.path.exists(reqtxt_var_path):
        link_fn(reqtxt_var_path, reqtxt_path)

    if os.path.exists(reqtxt_path):
        check_call(cmds_pip_install + ['--ignore-installed', '-r', reqtxt_path])

    if use_symlink:
        modules_link = os.path.abspath(os.path.join(work_dir, 'python_modules'))

        lib_dir = os.path.join(venv_dir, 'lib')
        if not os.path.exists(lib_dir):
            # see: https://stackoverflow.com/a/9964440
            if sys.maxsize > 2**32:
                arch = 64
            else:
                arch = 32
            lib_dir = os.path.join(venv_dir, 'lib%i' % arch)

        if os.path.exists(lib_dir):
            sitepackages = os.path.join(lib_dir,
                'python%s' % loader.config['python_version'], 'site-packages')

            loader.force_symlink(sitepackages, modules_link)
