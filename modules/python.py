""" Python module.
"""
import os
import shlex

def python(loader, project=None, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    binargs = ['python'] + list(args)
    os.execvp(binargs[0], binargs)


commands = (python,)
