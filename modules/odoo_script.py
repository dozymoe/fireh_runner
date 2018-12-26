""" odoo_script module.

Because of the main() function, this module is kept separately from the main
odoo module.
"""
from importlib import import_module
import os
import sys


def odoo_script(loader, project=None, variant=None, *args):
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
    # bugfix, command like `odoo.py shell`, the word 'shell'  must be mentioned
    # before we define --config, weird
    binargs = [python_bin, __file__] + list(args)
    if config_file:
        binargs.append('--config=' + config_file)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (odoo_script,)


def main():
    odoo_args = ['--no-xmlrpc']
    module_names = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            odoo_args.append(arg)
        else:
            module_names.append(arg)

    # Odoo config
    sys.path.remove(os.path.dirname(__file__))
    import odoo
    config = odoo.tools.config
    config.parse_config(odoo_args)
    odoo.cli.server.report_configuration()
    odoo.service.server.start(preload=[], stop=True)

    # Odoo
    local_vars = {
        'openerp': odoo,
        'odoo': odoo,
    }
    with odoo.api.Environment.manage():
        registry = odoo.registry(config['db_name'])
        with registry.cursor() as cr:
            uid = odoo.SUPERUSER_ID
            ctx = odoo.api.Environment(cr, uid, {})['res.users'].context_get()
            env = odoo.api.Environment(cr, uid, ctx)
            local_vars['env'] = env
            local_vars['self'] = env.user

            # Run modules
            for module_name in module_names:
                try:
                    mod = import_module(module_name)
                except ImportError:
                    sys.stderr.write('Unable to load the module: %s.\n' %\
                            module_name)
                mod.execute(**local_vars)

            cr.rollback()


if __name__ == '__main__':
    main()
