"""Django module.

Django is a python CMS framework.

Website: http://www.djangoproject.com
"""
import os

def django_admin(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    binargs = loader.get_binargs('django-admin', *args)

    os.execvp(binargs[0], binargs)


def django_manage(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = [python_bin, 'manage.py'] + list(args)
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def django_script(loader, project=None, variant=None, *args):
    loader.setup_virtualenv()
    python_bin = loader.get_python_bin()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = [python_bin] + list(args)
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (django_admin, django_manage, django_script)
