""" Alembic module.

Alembic is a database migration tool for SQLAlchemy.

Website: http://alembic.zzzcomputing.com
"""
import os

def alembic(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Apply database migration.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = loader.get_binargs('alembic')

    config_file = config.get('alembic.config_file')
    if config_file is not None:
        binargs.append('-c')
        binargs.append(loader.expand_path(config_file))

    envs = config.get('alembic.custom_env', {})
    for key, value in envs.items():
        binargs.append('-x')
        binargs.append('%s=%s' % (key, value))

    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (alembic,)
