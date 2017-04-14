"""Setup virtualenv and project."""
import os

def setup(loader, variant=None):
    """Setup virtualenv and project."""

    if variant is None:
        variant = os.environ.get('PROJECT_VARIANT',
                loader.config['default_variant'])

    for module_name in loader.config.get('setup_modules', []):
        os.chdir(loader.config['work_dir'])
        mod = loader.load_module(module_name)
        try:
            func = getattr(mod, 'setup')
        except AttributeError:
            continue

        func(loader, variant)


commands = (setup,)
