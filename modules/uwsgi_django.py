import os
import shlex
from argh import add_commands

class Plugin(object):

    config = None
    helper = None

    def __init__(self, config, helper):
        self.config = config
        self.helper = helper


    def uwsgi(self, *args):
        if len(args) == 1:
            args = shlex.split(args[0])

        self.helper.setup_virtualenv()

        binargs = ['uwsgi'] + list(args)
        os.execvp(binargs[0], binargs)


    def uwsgi_run(self, project=None, variant=None, *args):
        if len(args) == 1:
            args = shlex.split(args[0])

        self.helper.setup_virtualenv()

        project, variant = self.helper.setup_project_env(project, variant)

        config = self.config.get('configuration', {})
        config = config.get(variant, {})
        config = config.get(project, {})

        self.helper.setup_shell_env(config.get('shell_env', {}))

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


def initialize(config, argparser, helper):
    mod = Plugin(config, helper)
    add_commands(
        argparser,
        [
            mod.uwsgi,
            mod.uwsgi_run,
        ])
