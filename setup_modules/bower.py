import os
from shutil import copyfile
from subprocess import check_call

def setup(loader, variant):
    work_dir = loader.config['work_dir']

    use_symlink = not loader.config.get('no_symlink_please', False)
    if use_symlink:
        link_fn = loader.force_symlink
    else:
        link_fn = copyfile

    package_path = os.path.join(work_dir, 'bower.json')
    package_var_path = os.path.join(work_dir, 'bower-%s.json' % variant)
    if os.path.exists(package_var_path):
        link_fn(package_var_path, package_path)

    os.chdir(work_dir)

    if os.path.exists(package_path):
        print("Setup bower_components")
        check_call(['bower', 'install'])
