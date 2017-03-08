import os
from shutil import copyfile, rmtree
from subprocess import check_call


def setup(loader, variant):
    work_dir = loader.config['work_dir']
    python_bin = loader.get_python_bin()
    use_symlink = not loader.config.get('no_symlink_please', False)

    if use_symlink:
        link_fn = loader.force_symlink
    else:
        link_fn = copyfile

    ## python virtualenv

    venv_dir = os.path.realpath(os.path.join(work_dir,
            loader.config['virtualenv_dir']))

    if os.path.exists(venv_dir):
        rmtree(venv_dir, ignore_errors=True)

    check_call([python_bin, '-m', 'virtualenv', venv_dir])

    if use_symlink:
        modules_link = os.path.abspath(os.path.join(work_dir, 'python_modules'))
        loader.force_symlink(loader.get_virtualenv_sitepackages(), modules_link)

    loader.setup_virtualenv()

    cmds_pip_install = ['pip', 'install']
    cmds_pip_install.extend(loader.config.get('pip_install_args', []))

    ## update python pip

    check_call(cmds_pip_install + ['--upgrade', 'pip'])

    ## python requirements.txt

    reqtxt_path = os.path.join(work_dir, 'requirements.txt')
    reqtxt_var_path = os.path.join(work_dir, 'requirements-%s.txt' % variant)
    if os.path.exists(reqtxt_var_path):
        link_fn(reqtxt_var_path, reqtxt_path)

    if os.path.exists(reqtxt_path):
        check_call(cmds_pip_install + ['-r', reqtxt_path])
