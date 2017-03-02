"""Doxygen module.

Create project's documentation.

Website: http://www.doxygen.org
"""
import os

def doxygen(loader, variant=None, *args):
    if variant is None:
        variant = os.environ.get('PROJECT_VARIANT',
                loader.config.get('default_variant'))

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})

    binargs = ['doxygen', config['doxygen']['config_file']] + list(args)
    os.execvp(binargs[0], binargs)


commands = (doxygen,)
