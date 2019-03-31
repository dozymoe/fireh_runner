from distutils.spawn import find_executable
import os
import sys
from subprocess import check_call

def setup(loader, variant=None):
    loader.setup_virtualenv()

    composer_bin = find_executable('composer.phar')
    if composer_bin is None:
        composer_bin = find_executable('composer')
    if composer_bin is None:
        sys.stderr.write('Cannot find composer.phar\n')
        return -1

    _, variant = loader.setup_project_env(None, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})

    for project, prj_config in config.items():
        loader.setup_shell_env(prj_config.get('shell_env', {}))

        work_dir = prj_config.get('work_dir', project)
        work_dir = loader.expand_path(work_dir)

        binargs = [composer_bin, 'install']

        json_path = os.path.join(work_dir, 'composer.json')
        json_var_path = os.path.join(work_dir, 'composer-%s.json' % variant)
        if os.path.exists(json_var_path):
            loader.force_symlink(json_var_path, json_path)

        if not os.path.exists(json_path):
            continue

        os.chdir(work_dir)
        check_call(binargs)

    return 0
