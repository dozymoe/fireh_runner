"""Waf module.

Website: http://waf.io
"""
import os

def waf(loader, *args):
    """Build project."""
    loader.setup_virtualenv()

    binargs = ['waf'] + list(args)
    os.execvp(binargs[0], binargs)


commands = (waf,)
