"""Doxygen module.

Create project's documentation.

Website: http://www.doxygen.org
"""
import os
import shlex

def doxygen(loader, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    if variant is None:
        variant = os.environ.get('PROJECT_VARIANT',
                loader.config.get('default_variant'))

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})

    binargs = ['doxygen', config['doxygen']['config_file']]
    os.execvp(binargs[0], binargs)


commands = (doxygen,)
