""" Odoo Test module.

Odoo is an OpenERP framework.
A copy of odoo.py with added features that eases testing.

Website: http://www.odoo.com
"""
import os
# set server timezone in UTC before time module imported
os.environ['TZ'] = 'UTC'

from distutils.util import strtobool
import logging
import subprocess
import sys

SHELL_TIMEOUT = None
SHELL_ENV_CLEANDB = 'RUNNER_SUBPROCESS_ARG_CLEANDB'

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def odoo_test(loader, project=None, variant='testing', reset='n', *args):
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
    os.environ[SHELL_ENV_CLEANDB] = reset
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'server'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_shell(loader, project=None, variant='testing', *args):
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


def odoo_test_install(loader, project=None, variant='testing', reset='n',
        *args):
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
    os.environ[SHELL_ENV_CLEANDB] = reset
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__, 'install'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_test_uninstall(loader, project=None, variant='testing', *args):
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


def odoo_test_upgrade(loader, project=None, variant='testing', *args):
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


def odoo_test_list_installed(loader, project=None, variant='testing', *args):
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
    binargs = [python_bin, __file__, 'list-installed'] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo_test, odoo_test_install, odoo_test_uninstall,
        odoo_test_upgrade, odoo_test_shell, odoo_test_list_installed)


def _run_server():
    import odoo
    odoo.cli.main()


def _run_silent_server():
    import odoo

    # Odoo config
    odoo_args = ['--no-xmlrpc']
    module_names = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            odoo_args.append(arg)
    config = odoo.tools.config
    config.parse_config(odoo_args)

    odoo.cli.server.report_configuration()
    odoo.service.server.start(preload=[], stop=True)


def _execute(*callbacks):
    import odoo

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
                except Exception as e:
                    _logger.exception(e)
                    cr.rollback()

            cr.rollback()


def _reset_database():
    import odoo
    import psycopg2

    # Odoo config
    odoo_args = []
    module_names = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            odoo_args.append(arg)
    config = odoo.tools.config
    config.parse_config(odoo_args)

    dsn = 'postgresql://%s:%s@%s:%s/%s' % (config['db_user'],
            config['db_password'], config['db_host'] or 'localhost',
            config['db_port'] or 5432, config['db_name'])
    with psycopg2.connect(dsn) as db:
        with db.cursor() as cur:
            cur.execute('DROP OWNED BY CURRENT_USER')
        db.commit()


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
    sys.path.remove(os.path.dirname(__file__))
    cmd = sys.argv.pop(1)

    if strtobool(os.environ.get(SHELL_ENV_CLEANDB, 'n')):
        _reset_database()

    if cmd == 'server':
        sys.argv.append('--test-enable')
        _run_server()

    elif cmd == 'install':
        sys.argv.append('--test-enable')
        _run_silent_server()
        _execute(_install)

    elif cmd == 'uninstall':
        _run_silent_server()
        _execute(_uninstall)

    elif cmd == 'list-installed':
        _run_silent_server()
        _execute(_list_installed)


if __name__ == '__main__':
    main()
