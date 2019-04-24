""" Odoo module.

Odoo is an OpenERP framework.

Website: http://www.odoo.com
"""
import os
from distutils.util import strtobool
from functools import partial
import logging
import subprocess
import sys
# set server timezone in UTC before time module imported
os.environ['TZ'] = 'UTC'

SHELL_TIMEOUT = None
SHELL_ENV_QUIET = 'RUNNER_SUBPROCESS_ARG_QUIET'
SHELL_ENV_WITH_SERVER = 'RUNNER_SUBPROCESS_ARGS_WITH_SERVER'

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def odoo(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'server'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_cleardb(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'cleardb'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_shell(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'server']
    binargs.append('shell')
    binargs.append('--no-xmlrpc')
    binargs += list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_install(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'install'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_uninstall(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'uninstall'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_upgrade(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'server']
    binargs.append('--no-xmlrpc')
    binargs.append('--stop-after-init')
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
        ret = subprocess.call(binargs + ['-u', mod])
        if ret:
            exit(ret)
    exit(0)


def odoo_script(loader, project=None, variant=None, quiet='y', with_server='y',
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
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    os.environ[SHELL_ENV_QUIET] = quiet
    os.environ[SHELL_ENV_WITH_SERVER] = with_server
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'script'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_setup(loader, project=None, variant=None, *args):
    venv_type = loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    odoo_dir = os.path.join(loader.config['work_dir'],
            config.get('odoo_dir', 'lib/odoo'))

    binargs = [python_bin, 'setup.py', 'install']
    if venv_type == 'python':
        binargs.append('--user')

    os.chdir(odoo_dir)
    os.execvp(binargs[0], binargs)


def odoo_list_installed(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    config_file = config.get('config_file')
    config_file = os.path.join(loader.config['work_dir'],
            config_file)

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    python_bin = loader.get_python_bin()
    os.environ[SHELL_ENV_QUIET] = 'y'
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'list-installed'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo, odoo_cleardb, odoo_setup, odoo_shell, odoo_install,
        odoo_uninstall, odoo_upgrade, odoo_script, odoo_list_installed)


def _run_server():
    import odoo #pylint:disable=redefined-outer-name
    odoo.cli.main()


def _load_config(odoo_args):
    import odoo #pylint:disable=redefined-outer-name
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            odoo_args.append(arg)
    odoo.tools.config.parse_config(odoo_args)
    return odoo.tools.config


def _run_silent_server(quiet=False):
    import odoo #pylint:disable=redefined-outer-name
    _load_config(['--no-xmlrpc', '--workers=0', '--max-cron-threads=0'])
    if not quiet:
        odoo.cli.server.report_configuration()
    odoo.service.server.start(preload=[], stop=True)


def _execute(*callbacks):
    import odoo #pylint:disable=redefined-outer-name
    local_vars = {
        'openerp': odoo,
        'odoo': odoo,
    }
    with odoo.api.Environment.manage():
        registry = odoo.registry(odoo.tools.config['db_name'])
        with registry.cursor() as cr:
            uid = odoo.SUPERUSER_ID
            ctx = odoo.api.Environment(cr, uid, {})['res.users'].context_get()
            env = odoo.api.Environment(cr, uid, ctx)
            local_vars['env'] = env
            local_vars['self'] = env.user
            for callback in callbacks:
                try:
                    callback(**local_vars)
                except Exception as e: #pylint:disable=broad-except
                    _logger.exception(e)
                    cr.rollback()

            cr.rollback()


def _simple_execute(*callbacks):
    for callback in callbacks:
        try:
            callback()
        except Exception as e: #pylint:disable=broad-except
            _logger.exception(e)


def _reset_database():
    import psycopg2
    config = _load_config([])
    dsn = 'postgresql://%s:%s@%s:%s/%s' % (config['db_user'],
            config['db_password'], config['db_host'] or 'localhost',
            config['db_port'] or 5432, config['db_name'])
    with psycopg2.connect(dsn) as db:
        with db.cursor() as cur:
            cur.execute('DROP OWNED BY CURRENT_USER')
        db.commit()


def _run_script(quiet=False):
    from importlib import import_module
    with_server = strtobool(os.environ.get(SHELL_ENV_WITH_SERVER, 'y'))
    if with_server:
        _run_silent_server(quiet)
    else:
        _load_config([])

    module_name = sys.argv[1]
    callback_args = []
    # Remove shell arguments started with '-'
    for arg in sys.argv[2:]:
        if not arg.startswith('-'):
            callback_args.append(arg)
    try:
        mod = import_module(module_name)
        if with_server:
            _execute(partial(mod.execute, args=callback_args))
        else:
            _simple_execute(partial(mod.simple_execute, args=callback_args))
    except ImportError:
        _logger.error("Unable to load module '%s'.", module_name)


def _install(env, **kwargs):
    IrModule = env['ir.module.module']
    for name in sys.argv[1:]:
        if name.startswith('-'):
            continue
        _logger.info("Installing module '%s'.", name)
        mod = IrModule.search([('name', '=', name)]).exists()
        if not mod:
            IrModule.update_list()
        if not mod:
            mod = IrModule.search([('name', '=', name)]).exists()
        if not mod:
            _logger.error("Module '%s' not found!", name)
            break
        if mod.state not in ('installed', 'to upgrade'):
            mod.button_immediate_install()
            env.cr.commit()


def _uninstall(env, **kwargs):
    IrModule = env['ir.module.module']
    for name in sys.argv[1:]:
        if name.startswith('-'):
            continue
        _logger.info("Uninstalling module '%s'.", name)
        mod = IrModule.search([('name', '=', name)]).exists()
        if not mod:
            continue
        if mod.state != 'uninstalled':
            mod.button_immediate_uninstall()
            env.cr.commit()


def _list_installed(env, **kwargs):
    IrModule = env['ir.module.module']
    print("Installed modules:")
    for mod in IrModule.search([('state', '=', 'installed')], order='name'):
        print(mod.name)


def main():
    __import__('pkg_resources').declare_namespace('odoo.addons')
    try:
        sys.path.remove(os.path.dirname(__file__))
    except: #pylint:disable=bare-except
        pass
    try:
        sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
    except: #pylint:disable=bare-except
        pass

    quiet = strtobool(os.environ.get(SHELL_ENV_QUIET, 'n'))

    cmd = sys.argv.pop(1)
    if cmd == 'server':
        _run_server()

    elif cmd == 'install':
        _run_silent_server(quiet)
        _execute(_install)

    elif cmd == 'uninstall':
        _run_silent_server(quiet)
        _execute(_uninstall)

    elif cmd == 'script':
        _run_script(quiet)

    elif cmd == 'list-installed':
        _run_silent_server(quiet)
        _execute(_list_installed)

    elif cmd == 'cleardb':
        _reset_database()

    else:
        sys.argv.insert(1, cmd)
        _run_server()


if __name__ == '__main__':
    main()
