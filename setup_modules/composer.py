from distutils.spawn import find_executable
import os
from shutil import copyfile
import sys
from subprocess import check_call

def setup(loader, variant=None):
    _, variant = loader.setup_project_env(None, variant)
    work_dir = loader.config['work_dir']

    use_symlink = not loader.config.get('no_symlink_please', False)
    if use_symlink:
        link_fn = loader.force_symlink
    else:
        link_fn = copyfile

    composer_bin = find_executable('composer.phar')
    if composer_bin is None:
        composer_bin = find_executable('composer')
    if composer_bin is None:
        sys.stderr.write('Cannot find composer.phar\n')
        return -1

    package_path = os.path.join(work_dir, 'composer.json')
    package_var_path = os.path.join(work_dir, 'composer-%s.json' % variant)
    if os.path.exists(package_var_path):
        link_fn(package_var_path, package_path)

    if os.path.exists(package_path):
        print("Setup composer packages")
        check_call([composer_bin, 'install'], cwd=work_dir)

    return 0
