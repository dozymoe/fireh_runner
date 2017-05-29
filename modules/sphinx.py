""" Sphinx module.

Sphinx is a tool that makes it easy to create intelligent and beautiful
documentation, written by Georg Brandl and licensed under the BSD license.

It was originally created for the Python documentation, and it has excellent
facilities for the documentation of software projects in a range of languages.

Website: http://www.sphinx-doc.org
"""
import os

def sphinx_apidoc(loader, *args):
    """ Create templates from module docs in python files.
    """
    loader.setup_virtualenv()

    binargs = loader.get_binargs('sphinx-apidoc', *args)
    os.execvp(binargs[0], binargs)


def sphinx_build(loader, *args):
    """ Create documentation pages from templates.
    """
    loader.setup_virtualenv()

    binargs = loader.get_binargs('sphinx-build', *args)
    os.execvp(binargs[0], binargs)


def sphinx_quickstart(loader, *args):
    """ Setup Sphinx configuration.
    """
    loader.setup_virtualenv()

    binargs = loader.get_binargs('sphinx-quickstart', *args)
    os.execvp(binargs[0], binargs)


commands = (sphinx_apidoc, sphinx_build, sphinx_quickstart)
