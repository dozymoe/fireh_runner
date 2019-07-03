""" Sphinx module.

Sphinx is a tool that makes it easy to create intelligent and beautiful
documentation, written by Georg Brandl and licensed under the BSD license.

It was originally created for the Python documentation, and it has excellent
facilities for the documentation of software projects in a range of languages.

Website: http://www.sphinx-doc.org
"""
import os

def sphinx_apidoc(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Create templates from module docs in python files.
    """
    loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    binargs = loader.get_binargs('sphinx-apidoc', *args)
    os.execvp(binargs[0], binargs)


def sphinx_build(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Create documentation pages from templates.
    """
    loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    binargs = loader.get_binargs('sphinx-build', *args)
    os.execvp(binargs[0], binargs)


def sphinx_quickstart(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Setup Sphinx configuration.
    """
    loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    binargs = loader.get_binargs('sphinx-quickstart', *args)
    os.execvp(binargs[0], binargs)


commands = (sphinx_apidoc, sphinx_build, sphinx_quickstart)
