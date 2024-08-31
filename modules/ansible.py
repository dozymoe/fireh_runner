""" Ansible module.

Ansible is an IT automation tool. It can configure systems, deploy software,
and orchestrate more advanced IT tasks such as continuous deployments or zero
downtime rolling updates.

Website: http://ansible.com
"""
import os

def ansible(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Server provisioning.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = loader.get_binargs('ansible')

    inventories = loader.ensure_list(config.get('ansible.inventory'))
    for inventory in inventories:
        binargs.append('-i')
        binargs.append(loader.expand_path(inventory))

    extra_vars = config.get('ansible.extra_vars')
    if extra_vars:
        for key, val in extra_vars.items():
            if ' ' in val:
                val = f"'{val}'"
            binargs.append(f'--extra-vars={key}={val}')

    binargs += list(args)

    os.chdir(work_dir)
    os.execv(binargs[0], binargs)


def ansible_doc(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Ansible modules documentation.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()

    binargs = loader.get_binargs('ansible-doc')
    binargs += list(args)
    os.execv(binargs[0], binargs)


def ansible_playbook(loader, project=None, variant=None, *args): #pylint:disable=keyword-arg-before-vararg
    """ Server provisioning.
    """
    project, variant = loader.setup_project_env(project, variant)
    loader.setup_virtualenv()
    loader.setup_shell_env()
    config = loader.get_project_config()

    work_dir = config.get('work_dir', project)
    work_dir = loader.expand_path(work_dir)

    binargs = loader.get_binargs('ansible-playbook')

    inventories = loader.ensure_list(config.get('ansible.inventory'))
    for inventory in inventories:
        binargs.append('-i')
        binargs.append(loader.expand_path(inventory))

    extra_vars = config.get('ansible.extra_vars')
    if extra_vars:
        for key, val in extra_vars.items():
            if ' ' in val:
                val = f"'{val}'"
            binargs.append(f'--extra-vars={key}={val}')

    playbook = config.get('ansible.playbook')
    if playbook:
        binargs.append(loader.expand_path(playbook))

    binargs += list(args)

    os.chdir(work_dir)
    os.execv(binargs[0], binargs)


commands = (ansible, ansible_doc, ansible_playbook)
