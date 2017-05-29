"""Scrapy module.

An open source and collaborative framework for extracting the data you need
from websites. In a fast, simple, yet extensible way.
"""
import os

def scrapy(loader, project=None, variant=None, *args):
    """Extract data from websites."""
    loader.setup_virtualenv()

    project, variant = loader.setup_project_env(project, variant)

    config = loader.config.get('configuration', {})
    config = config.get(variant, {})
    config = config.get(project, {})

    loader.setup_shell_env(config.get('shell_env', {}))

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = loader.get_binargs('scrapy', *args)

    os.chdir(work_dir)
    os.execvp(binargs[0], binargs)


def scrapy_startproject(loader, *args):
    """Create new scrapy project."""
    loader.setup_virtualenv()

    binargs = loader.get_binargs('scrapy', 'startproject', *args)

    os.execvp(binargs[0], binargs)


commands = (scrapy, scrapy_startproject)
