""" Odoo Test module.

Odoo is an OpenERP framework.
A copy of odoo.py with added features that eases testing.

Website: http://www.odoo.com
"""
import logging
import os
import subprocess
import sys
# set server timezone in UTC before time module imported
os.environ['TZ'] = 'UTC'

SHELL_TIMEOUT = None
SHELL_ENV_QUIET = 'RUNNER_SUBPROCESS_ARG_QUIET'
SHELL_ENV_WITH_SERVER = 'RUNNER_SUBPROCESS_ARGS_WITH_SERVER'

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def _get_realfile():
    path = os.path.abspath(__file__)
    return os.path.splitext(path)[0] + '_.py'


def odoo_test(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile()] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_cleardb(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'cleardb'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_shell(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'shell'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_install(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'install'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_uninstall(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'uninstall'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_upgrade(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'upgrade']
    if config_file:
        binargs.append('--config=' + config_file)

    for arg in args:
        if arg.startswith('-'):
            binargs.append(arg)

    os.chdir(work_dir)
    for mod in args:
        if mod.startswith('-'):
            continue
        _logger.info("Upgrading module '%s'.", mod)
        ret = subprocess.call(binargs + [mod])
        if ret:
            sys.exit(ret)
    sys.exit(0)


def odoo_test_list_installed(loader, project=None, variant='testing', *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'list-installed'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo_test, odoo_test_cleardb, odoo_test_install,
        odoo_test_uninstall, odoo_test_upgrade, odoo_test_shell,
        odoo_test_list_installed)
