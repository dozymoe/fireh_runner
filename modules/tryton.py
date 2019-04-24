""" Tryton module.

Tryton is a three-tier high-level general purpose application platform under
the license GPL-3 written in Python and using PostgreSQL as database engine.

It is the core base of a complete business solution providing modularity,
scalability and security.

Website: http://www.tryton.org
"""
import os

SHELL_TIMEOUT = None


def trytond(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    database_name = config.get('tryton.database.name', project)
    config_file = config.get('tryton.config_file')
    if config_file:
        config_file = os.path.join(loader.config['work_dir'],
                config_file)

    logging_config_file = config.get('tryton.logging.config_file')
    if logging_config_file:
        logging_config_file = os.path.join(loader.config['work_dir'],
                logging_config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    bindir = config.get('trytond.bin_dir')
    if bindir:
        python_bin = loader.get_python_bin()
        binargs = [python_bin, os.path.join(loader.config['work_dir'], bindir,
                'trytond')]
    else:
        binargs = loader.get_binargs('trytond')
    if config_file:
        binargs += ['--config', config_file]
    if database_name:
        binargs += ['--database', database_name]
    if logging_config_file:
        binargs += ['--logconf', logging_config_file]
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def trytond_admin(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    database_name = config.get('tryton.database.name', project)
    config_file = config.get('tryton.config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    bindir = config.get('trytond.bin_dir')
    if bindir:
        python_bin = loader.get_python_bin()
        binargs = [python_bin, os.path.join(loader.config['work_dir'], bindir,
                'trytond-admin')]
    else:
        binargs = loader.get_binargs('trytond-admin')
    if config_file:
        binargs += ['--config', config_file]
    if database_name:
        binargs += ['--database', database_name]
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def trytond_cron(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    database_name = config.get('tryton.database.name', project)
    config_file = config.get('tryton.config_file')
    if config_file:
        config_file = os.path.join(loader.config['work_dir'],
                config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    bindir = config.get('trytond.bin_dir')
    if bindir:
        python_bin = loader.get_python_bin()
        binargs = [python_bin, os.path.join(loader.config['work_dir'], bindir,
                'trytond-cron')]
    else:
        binargs = loader.get_binargs('trytond-cron')
    if config_file:
        binargs += ['--config', config_file]
    if database_name:
        binargs += ['--database', database_name]
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def trytond_worker(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    database_name = config.get('tryton.database.name', project)
    config_file = config.get('tryton.config_file')
    if config_file:
        config_file = os.path.join(loader.config['work_dir'],
                config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    bindir = config.get('trytond.bin_dir')
    if bindir:
        python_bin = loader.get_python_bin()
        binargs = [python_bin, os.path.join(loader.config['work_dir'], bindir,
                'trytond-worker')]
    else:
        binargs = loader.get_binargs('trytond-worker')
    if config_file:
        binargs += ['--config', config_file]
    if database_name:
        binargs += ['--database', database_name]
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def tryton(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    database_name = config.get('tryton.database.name', project)
    config_file = config.get('tryton.config_file')
    if config_file:
        config_file = os.path.join(loader.config['work_dir'],
                config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    bindir = config.get('tryton.bin_dir')
    if bindir:
        python_bin = loader.get_python_bin()
        binargs = [python_bin, os.path.join(loader.config['work_dir'], bindir,
                'tryton')]
    else:
        binargs = loader.get_binargs('tryton')
    if config_file:
        binargs += ['--config', config_file]
    if database_name:
        binargs += ['--database', database_name]
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (trytond, trytond_admin, trytond_cron, trytond_worker, tryton)
