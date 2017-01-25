"""uwsgi-for-Django module.

Website: https://uwsgi-docs.readthedocs.io/en/latest/
"""
import os
import shlex

def uwsgi(loader, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    binargs = ['uwsgi'] + list(args)
    os.execvp(binargs[0], binargs)


def uwsgi_run(loader, project=None, variant=None, *args):
    if len(args) == 1:
        args = shlex.split(args[0])

    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    socket_path = config.get('socket_path', '/tmp/%s-%s-%s.sock' %\
            (self.config['package_name'], project, variant))

    binargs = [
        'uwsgi',
        '--module=%s.wsgi:application' % project,
        '--socket=' + os.path.realpath(socket_path),
        '--chmod-socket',
        '--max-requests=%i' % config.get('max_requests', 5000),
        '--workers=%i' % config.get('worker_count', 1),
        '--master',
        '--die-on-term',
    ]
    if variant in ('dev', 'devel', 'development'):
        binargs.append('--honour-stdin')

    os.chdir(os.path.join(self.config['work_dir'], project))

    binargs += list(args)
    os.execvp(binargs[0], binargs)


commands = (uwsgi, uwsgi_run)
