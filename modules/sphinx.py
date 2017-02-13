""" Sphinx module.

Sphinx is a tool that makes it easy to create intelligent and beautiful
documentation, written by Georg Brandl and licensed under the BSD license.

It was originally created for the Python documentation, and it has excellent
facilities for the documentation of software projects in a range of languages. 

Website: http://www.sphinx-doc.org
"""
import os
import shlex

def sphinx_quickstart(loader, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    binargs = ['sphinx-quickstart'] + list(args)
    os.execvp(binargs[0], binargs)


commands = (sphinx_quickstart,)
