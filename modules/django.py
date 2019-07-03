"""Django module.

Django is a python CMS framework.

Website: http://www.djangoproject.com
"""
import os

def django_admin(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()

    binargs = loader.get_binargs('django-admin', *args)
    os.execvp(binargs[0], binargs)


def django_manage(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = [python_bin, 'manage.py'] + list(args)
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def django_script(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()
    python_bin = loader.get_python_bin()

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = [python_bin] + list(args)
    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


commands = (django_admin, django_manage, django_script)
