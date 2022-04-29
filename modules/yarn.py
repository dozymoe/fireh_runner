""" Yarn module.
"""
import os

def yarn(loader, project=None, variant=None, *args):
    """Install or uninstall nodejs packages."""
    project_selected = project is not None
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_shell_env()

    if project_selected:
        config = loader.get_project_config()
        work_dir = config.get('work_dir', project)
        work_dir = loader.expand_path(work_dir)
    else:
        work_dir = loader.config['current_dir']
    os.chdir(work_dir)

    binargs = ['yarnpkg'] + list(args)
    os.execvp(binargs[0], binargs)


commands = (yarn,)
