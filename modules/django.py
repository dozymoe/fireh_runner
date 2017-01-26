"""Django module.

Django is a python CMS framework.

Website: http://www.djangoproject.com
"""
import os
import shlex

def django_admin(loader, project=None, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    binargs = ['django-admin'] + list(args)
    os.execvp(binargs[0], binargs)


def django_manage(loader, project=None, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    binargs = ['python', 'manage.py'] + list(args)
    os.chdir(os.path.join(loader.config['work_dir'], project))
    os.execvp(binargs[0], binargs)


def django_script(loader, project=None, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    binargs = ['python'] + list(args)
    os.chdir(os.path.join(loader.config['work_dir'], project))
    os.execvp(binargs[0], binargs)


commands = (django_admin, django_manage, django_script)
