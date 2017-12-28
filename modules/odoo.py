""" Odoo module.

Odoo is an OpenERP framework.

Website: http://www.odoo.com
"""
import os


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
    binargs = [python_bin, __file__]
    if config_file:
        binargs.append('--config=' + config_file)
    binargs += list(args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def odoo_setup(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    work_dir = os.path.join(loader.config['work_dir'], 'lib', 'odoo')

    binargs = [python_bin, 'setup.py', 'install', '--user']
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo, odoo_setup)


def main():
    # set server timezone in UTC before time module imported
    __import__('os').environ['TZ'] = 'UTC'
    __import__('pkg_resources').declare_namespace('odoo.addons')
    import odoo
    odoo.cli.main()


if __name__ == '__main__':
    main()
