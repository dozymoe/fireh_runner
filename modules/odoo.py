""" Odoo module.

Odoo is an OpenERP framework.

Website: http://www.odoo.com
"""
import glob
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


def odoo(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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


def odoo_cleardb(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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


def odoo_shell(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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
    binargs = [python_bin, _get_realfile(), 'shell'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_install(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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


def odoo_uninstall(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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


def odoo_upgrade(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
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


def odoo_script(loader, project=None, variant=None, quiet='y', with_server='y', #pylint:disable=keyword-arg-before-vararg
        *args):
    """
    Runs python scripts and provides odoo shell environment.

    Usage example: `./run odoo-script odoo.addons.my_module.scripts.my_script`

    Where my_script is a module name, and the related file is my_script.py.
    The python script must implements the function below:

    def execute(env, self, odoo, openerp):
        pass

    It is recommended not to run anything on the module's scope, because some
    scripts are run as
    `cat my_module/scripts/other_script.py | ./run odoo-shell` for educational
    purposes, that is to show how the script can be run inside odoo shell.

    When `with_server` is 'n', do not call `execute()`, call `simple_execute()`
    without arguments.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    os.environ[SHELL_ENV_QUIET] = quiet
    os.environ[SHELL_ENV_WITH_SERVER] = with_server
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'script'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_setup(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    _, variant = loader.setup_project_env(project, variant)
    venv_type = loader.setup_virtualenv()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()
    loader.setup_shell_env()

    odoo_dir = os.path.join(loader.config['work_dir'],
            config.get('odoo_dir', 'lib/odoo'))

    # Is directory writable?
    if os.access(odoo_dir, os.W_OK):
        binargs = [python_bin, 'setup.py', 'install']
        if venv_type == 'python':
            binargs.append('--user')

        os.chdir(odoo_dir)
        os.execvp(binargs[0], binargs)

    odoo_ver = config.get('odoo_version')
    if odoo_ver:
        # Check sdist of specific version.
        filename = os.path.join(odoo_dir, 'dist', 'odoo-%s.0.tar.gz' % odoo_ver)
        if not os.path.exists(filename):
            filename = None
    else:
        # Check any sdist.
        files = glob.glob(os.path.join(odoo_dir, 'dist', 'odoo-*.tar.gz'))
        if files:
            # Get latest version.
            files.sort(reverse=True)
            filename = files[0]
        else:
            filename = None

    if not filename:
        raise RuntimeError("Odoo directory is not writable for setup.py and "
                "source dist tarball not found.")

    binargs = [python_bin, '-m', 'pip', 'install', filename]
    if venv_type == 'python':
        binargs.append('--user')

    os.execvp(binargs[0], binargs)


def odoo_list_installed(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    config_file = os.environ['ODOO_CONFIG_FILE']
    config_file = os.path.join(loader.config['work_dir'], config_file)

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    os.environ[SHELL_ENV_QUIET] = 'y'
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, _get_realfile(), 'list-installed'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo, odoo_cleardb, odoo_setup, odoo_shell, odoo_install,
        odoo_uninstall, odoo_upgrade, odoo_script, odoo_list_installed)
