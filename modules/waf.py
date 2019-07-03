"""Waf module.

Website: http://waf.io
"""
import os

def waf(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """Build project.

    Checkout pybuildtool (shameless plug) for a python version of web project
    resources compiler.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()

    binargs = loader.get_binargs('waf', *args)
    os.execvp(binargs[0], binargs)


commands = (waf,)
