"""uwsgi-for-Django module.

Website: https://uwsgi-docs.readthedocs.io/en/latest/
"""
import os

def uwsgi(loader, *args):
    loader.setup_virtualenv()
    venv_dir = loader.get_virtualenv_dir()
    binargs = [os.path.join(venv_dir, 'bin', 'uwsgi')] + list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_run(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    socket_path = config.get('socket_path', '/tmp/%s-%s-%s.sock' %\
            (loader.config['package_name'], project, variant))

    venv_dir = loader.get_virtualenv_dir()
    binargs = [
        os.path.join(venv_dir, 'bin', 'uwsgi'),
        '--module=%s.wsgi:application' % project,
        '--socket=' + os.path.realpath(socket_path),
        '--chmod-socket',
        '--max-requests=%i' % config.get('max_requests', 5000),
        '--workers=%i' % config.get('worker_count', 1),
        '--master',
        '--die-on-term',
    ]
    if not loader.is_production():
        binargs.append('--honour-stdin')

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs += list(args)
    os.execvp(binargs[0], binargs)


commands = (uwsgi, uwsgi_run)
