""" Redis module.
"""
import os


def redis(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = [config.get('redis.bin', '/usr/sbin/redis-server')] + list(args)
    os.execvp(binargs[0], binargs)


def redis_cli(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = [
        config.get('redis.cli.bin', '/usr/bin/redis-cli'),
        '-h', os.environ.get('REDIS_LISTEN', '127.0.0.1'),
        '-p', os.environ.get('REDIS_PORT', 6379),
    ]

    os.execvp(binargs[0], binargs + list(args))


def redis_run(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()
    config = loader.get_project_config()

    binargs = [
        config.get('redis.bin', '/usr/sbin/redis-server'),
        '--bind', os.environ.get('REDIS_LISTEN', '127.0.0.1'),
        '--port', os.environ.get('REDIS_PORT', 6379),
    ]

    filename = config.get('redis.filename')
    if filename:
        filename = os.path.join(os.environ['ROOT_DIR'], filename)
        binargs.append('--dir')
        binargs.append(os.path.dirname(filename))
        binargs.append('--dbfilename')
        binargs.append(os.path.basename(filename))

    max_memory = config.get('redis.max_memory')
    if max_memory:
        binargs.append('--maxmemory')
        binargs.append(max_memory)

    eviction_policy = config.get('redis.eviction_policy')
    if eviction_policy:
        binargs.append('--maxmemory-policy')
        binargs.append(eviction_policy)

    lazy_eviction = config.get('redis.lazy_eviction')
    if lazy_eviction:
        binargs.append('--lazyfree-lazy-eviction')
        binargs.append('yes')

    os.execvp(binargs[0], binargs + list(args))


commands = (redis, redis_cli, redis_run)
