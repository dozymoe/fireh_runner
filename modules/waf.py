"""Waf module.

Website: http://waf.io
"""
import os
import shlex

def waf(loader, *args):
    """Build project."""
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    binargs = ['waf'] + list(args)
    os.execvp(binargs[0], binargs)


commands = (waf,)
