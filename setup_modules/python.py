import distutils.spawn
import os
from shutil import rmtree
from subprocess import check_call

try:
    input = raw_input
except NameError:
    pass


def setup(loader, variant):
    work_dir = loader.config['work_dir']
    python_version = loader.config['python_version']

    ## python bin

    python_bin = 'python' + python_version
    if distutils.spawn.find_executable(python_bin) is None:
        shellenv_key = python_bin.upper() + '_BIN'
        if shellenv_key in os.environ:
            python_bin = os.environ[shellenv_key]
        else:
            python_bin = input(python_bin + ' executable location: ')

    ## python virtualenv

    venv_dir = os.path.realpath(os.path.join(work_dir,
            loader.config['virtualenv_dir']))

    if os.path.exists(venv_dir):
        rmtree(venv_dir)

    check_call(['virtualenv', '--python=' + python_bin, venv_dir])

    modules_link = os.path.abspath(os.path.join(work_dir, 'python_modules'))
    loader.force_symlink(os.path.join(venv_dir, 'lib',
            'python' + python_version, 'site-packages'), modules_link)

    loader.setup_virtualenv()

    cmds_pip_install = ['pip', 'install']
    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    ## update python pip

    check_call(cmds_pip_install + ['--upgrade', 'pip'])

    ## python requirements.txt

    reqtxt_path = os.path.join(work_dir, 'requirements.txt')
    reqtxt_var_path = os.path.join(work_dir, 'requirements-%s.txt' % variant)
    if os.path.exists(reqtxt_var_path):
        loader.force_symlink(reqtxt_var_path, reqtxt_path)

    if os.path.exists(reqtxt_path):
        check_call(cmds_pip_install + ['-r', reqtxt_path])
