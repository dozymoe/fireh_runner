""" Memcached module.
"""
import os


def memcached(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = [config.get('memcached.bin', '/usr/bin/memcached')] + list(args)
    os.execvp(binargs[0], binargs)


def memcached_run(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = [
        config.get('memcached.bin', '/usr/bin/memcached'),
        '--listen=%s' % os.environ.get('MEMCACHED_LISTEN', '127.0.0.1'),
        '--port=%s' % os.environ.get('MEMCACHED_PORT', 11211),
    ]

    # in megabytes
    max_memory = config.get('memcached.max_memory')
    if max_memory:
        binargs.append('--memory-limit=%s' % max_memory)

    os.execvp(binargs[0], binargs + list(args))


commands = (memcached, memcached_run)
