""" Odoo module.

Odoo is an OpenERP framework.

Website: http://www.odoo.com
"""
import os
import subprocess
import sys
from time import sleep

SHELL_TIMEOUT = None


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
    binargs = [python_bin, __file__] + list(args)
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
    binargs = [python_bin, __file__]
    binargs.append('shell')
    binargs.append('--no-xmlrpc')
    binargs += list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_install(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()
    import pexpect

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
    binargs = [python_bin, __file__]
    binargs.append('shell')
    binargs.append('--no-xmlrpc')
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)

    environ = os.environ.copy()
    environ['IPY_TEST_SIMPLE_PROMPT'] = '1'
    spawn_args = {
        'echo': False,
        'env': environ,
        'logfile': sys.stdout,
        'timeout': SHELL_TIMEOUT,
    }
    if sys.version_info[0] > 2:
        spawn_args['encoding'] = 'utf-8'
    prc = pexpect.spawn(' '.join(binargs), **spawn_args)
    prc.expect(r'In \[\d+\]:')
    prc.sendline("IrModule = env['ir.module.module']")
    for mod in args:
        prc.expect(r'In \[\d+\]:')
        prc.sendline("mod = IrModule.search([('name', '=', '%s')]).exists()"\
                % mod)

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod: IrModule.update_list()")

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod: mod = IrModule.search([('name', '=', " +\
                "'%s')]).exists()" % mod)

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod:")
        prc.expect(r'\s+\.+:')
        prc.sendline("    print('Module \"%s\" not found!')" % mod)
        prc.expect(r'\s+\.+:')
        prc.sendline("    quit()")
        prc.expect(r'\s+\.+:')
        prc.sendline("")

        exp = prc.expect([pexpect.EOF, r'In \[\d+\]:'])
        if exp == 0:
            break
        else:
            prc.sendline("if mod and mod.state not in ('installed', " +\
                    "'to upgrade'): mod.button_immediate_install()")

    else:
        prc.expect(r'In \[\d+\]:')
        prc.sendline('quit')


def odoo_uninstall(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()
    import pexpect

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
    binargs = [python_bin, __file__]
    binargs.append('shell')
    binargs.append('--no-xmlrpc')
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)

    environ = os.environ.copy()
    environ['IPY_TEST_SIMPLE_PROMPT'] = '1'
    spawn_args = {
        'echo': False,
        'env': environ,
        'logfile': sys.stdout,
        'timeout': SHELL_TIMEOUT,
    }
    if sys.version_info[0] > 2:
        spawn_args['encoding'] = 'utf-8'
    prc = pexpect.spawn(' '.join(binargs), **spawn_args)
    prc.expect(r'In \[\d+\]:')
    prc.sendline("IrModule = env['ir.module.module']")
    for mod in args:
        prc.expect(r'In \[\d+\]:')
        prc.sendline("mod = IrModule.search([('name', '=', '%s')]).exists()"\
                % mod)

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod: IrModule.update_list()")

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod: mod = IrModule.search([('name', '=', " +\
                "'%s')]).exists()" % mod)

        prc.expect(r'In \[\d+\]:')
        prc.sendline("if not mod:")
        prc.expect(r'\s+\.+:')
        prc.sendline("    print('Module \"%s\" not found!')" % mod)
        prc.expect(r'\s+\.+:')
        prc.sendline("    quit()")
        prc.expect(r'\s+\.+:')
        prc.sendline("")

        exp = prc.expect([pexpect.EOF, r'In \[\d+\]:'])
        if exp == 0:
            break
        else:
            prc.sendline("if mod.state != 'uninstalled': " +\
                    "mod.button_immediate_uninstall()")

    prc.expect(r'In \[\d+\]:')
    prc.sendline('quit')


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
    binargs = [python_bin, __file__]
    binargs.append('--no-xmlrpc')
    binargs.append('--stop-after-init')
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    for mod in args:
        ret = subprocess.call(binargs + ['-u', mod])
        if ret:
            exit(ret)
    exit(0)


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


commands = (odoo, odoo_setup, odoo_shell, odoo_install, odoo_uninstall,
        odoo_upgrade)


def main():
    # set server timezone in UTC before time module imported
    __import__('os').environ['TZ'] = 'UTC'
    __import__('pkg_resources').declare_namespace('odoo.addons')
    import odoo
    odoo.cli.main()


if __name__ == '__main__':
    main()
