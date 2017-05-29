import os
from subprocess import check_call

def setup(loader, variant=None):
    loader.setup_virtualenv()

    _, variant = loader.setup_project_env(None, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})

    for project, prj_config in config.items():
        target = prj_config.get('alembic.setup_do_upgrade')
        if target is None:
            continue
        elif target is True:
            target = 'head'

        loader.setup_shell_env(prj_config.get('shell_env', {}))

        work_dir = prj_config.get('work_dir', project)
        work_dir = loader.expand_path(work_dir)

        binargs = loader.get_binargs('alembic')

        config_file = prj_config.get('alembic.config_file')
        if config_file is not None:
            pass
        elif os.path.exists(os.path.join(work_dir, 'alembic.ini')):
            config_file = os.path.join(work_dir, 'alembic.ini')
        else:
            continue

        binargs.append('-c')
        binargs.append(loader.expand_path(config_file))

        envs = prj_config.get('alembic.custom_env', {})
        for key, value in envs.items():
            binargs.append('-x')
            binargs.append('%s=%s' % (key, value))

        binargs.append('upgrade')
        binargs.append(target)

        os.chdir(work_dir)
        check_call(binargs)
