""" Odoo real module.

Odoo is an OpenERP framework.

Website: http://www.odoo.com
"""
from distutils.util import strtobool
from functools import partial
from importlib import import_module
import logging
import os
import sys
#-
import psycopg2 # pylint:disable=import-error

sys.path[0] = os.path.abspath(os.curdir)
import odoo

SHELL_ENV_QUIET = 'RUNNER_SUBPROCESS_ARG_QUIET'
SHELL_ENV_WITH_SERVER = 'RUNNER_SUBPROCESS_ARGS_WITH_SERVER'

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def _run_server():
    odoo.cli.main()


def _run_light(arg):
    version = odoo.release.version_info[0]
    sys.argv.insert(1, arg)
    sys.argv.insert(1, '--no-xmlrpc' if version <= 10 else '--no-http')
    sys.argv.insert(1, '--workers=0')
    sys.argv.insert(1, '--max-cron-threads=0')
    odoo.cli.main()


def _load_config(odoo_args):
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            odoo_args.append(arg)
    odoo.tools.config.parse_config(odoo_args)
    return odoo.tools.config


def _run_silent_server(quiet=False):
    version = odoo.release.version_info[0]
    _load_config([
            '--no-xmlrpc' if version <= 10 else '--no-http',
            '--workers=0',
            '--max-cron-threads=0'])
    if not quiet:
        odoo.cli.server.report_configuration()
    odoo.service.server.start(preload=[], stop=True)


def _execute(*callbacks):
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
    config = _load_config([])
    dsn = 'postgresql://%s:%s@%s:%s/%s' % (config['db_user'],
            config['db_password'], config['db_host'] or 'localhost',
            config['db_port'] or 5432, config['db_name'])
    with psycopg2.connect(dsn) as db:
        with db.cursor() as cur:
            cur.execute('DROP OWNED BY CURRENT_USER')
        db.commit()


def _run_script(quiet=False):
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

    elif cmd == 'shell':
        _run_light('shell')

    elif cmd == 'upgrade':
        _run_light('-u')

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
