""" Helper functions """

import os
from collections.abc import Mapping
from json import load as json_load


def flatten_dict(prefix, data, exceptions=None):
    # see http://stackoverflow.com/a/6036037
    if exceptions is None:
        exceptions = []

    for key in data:
        item = data[key]
        new_prefix = '.'.join([prefix, key])

        if isinstance(item, Mapping) and new_prefix not in exceptions:
            for child_item in flatten_dict(new_prefix, item):
                yield child_item
        else:
            yield (new_prefix, item)


def generic_adapter(prefix, new, setter):
    exceptions = []
    setter.update(flatten_dict(prefix, new, exceptions))


def load_configuration_files(files, setter, config_key=None, adapter=None):

    def _load(filename, loader):
        with open(filename, 'r', encoding='utf-8') as filehandle:
            config = loader(filehandle)

        if config_key is not None:
            config = config.get(config_key, {})

        if adapter:
            # let adapter updates settings
            name, _ = os.path.splitext(os.path.basename(filename))
            adapter(name, config, setter)

        elif isinstance(setter, Mapping):
            setter.update(config)

        else:
            # update settings ourself
            for key in config:
                # simple security measure, don't override magic attributes
                if key.startswith('__'):
                    continue

                setter(key, config[key])

    yaml_files = []

    for filename in files:
        # ignore non existing files
        if not os.path.exists(filename):
            continue

        _, ext = os.path.splitext(filename)
        if ext == '.json':
            _load(filename, json_load)

        elif ext in ('.yml', '.yaml'):
            yaml_files.append(filename)

    if yaml_files:
        from yaml import load as yaml_load #pylint:disable=import-outside-toplevel
        for filename in yaml_files:
            _load(filename, yaml_load)


def load_files_from_shell(setter, adapter=generic_adapter):
    """
    The shell passed us filenames in either yaml or json, which contains
    configuration data.

    Shell variables used are:
     * CONFIG_FILENAMES (comma deliminated filenames)
     * CONFIG_KEY       (after the file loaded as object, pick this field)
    """
    root_dir = os.environ.get('ROOT_DIR', '')
    files = os.environ.get('CONFIG_FILENAMES', '').split(os.pathsep)
    if not files:
        return

    files = [os.path.join(root_dir, fname.strip()) for fname in files]
    load_configuration_files(files, setter, os.environ.get('CONFIG_KEY'),
            adapter)
