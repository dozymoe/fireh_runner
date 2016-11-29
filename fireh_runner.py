#!/usr/bin/env python3

import os
from argh import dispatch
from argparse import ArgumentParser
from collections import Mapping, Sequence

# see http://stackoverflow.com/a/67692
from importlib.machinery import SourceFileLoader

from json import load as json_loadf

def load_module(name, runner_dir):
    return SourceFileLoader('runner.' + name, os.path.join(runner_dir,
            'modules', name + '.py')).load_module()


class Helper(object):

    config = None

    def __init__(self, config):
        self.config = config


    def setup_project_env(self, project=None, variant=None):
        project = self.config['project'] = project or\
                os.environ.get('PROJECT_NAME',
                self.config.get('default_project'))

        variant = self.config['variant'] = variant or\
                os.environ.get('PROJECT_VARIANT',
                self.config.get('default_variant'))

        os.environ['PROJECT_NAME'] = project
        os.environ['PROJECT_VARIANT'] = variant
        return project, variant


    def setup_shell_env(self, data):
        for key, value in self._flatten_dict('', data):
            os.environ[key] = value


    def setup_virtualenv(self):
        os.environ['PATH'] = ':'.join([
            os.path.join(
                self.config['work_dir'],
                self.config.get('virtualenv_dir', '.virtualenv'),
                'bin'),
            os.environ['PATH']])

        os.environ['PYTHONPATH'] = os.path.join(
            self.config['work_dir'],
            self.config.get('virtualenv_dir', '.virtualenv'),
            'lib',
            'python' + self.config.get('python_version', '3.4'),
            'site-packages')


    @staticmethod
    def _flatten_dict(prefix, data):
        # see http://stackoverflow.com/a/6036037
        for key in data:
            item = data[key]
            if prefix:
                new_prefix = prefix + '_' + key.upper()
            else:
                new_prefix = key.upper()

            if isinstance(item, Mapping):
                for child_item in Helper._flatten_dict(new_prefix, item):
                    yield child_item
            elif isinstance(item, Sequence):
                yield (new_prefix, ';'.join(item))
            else:
                yield (new_prefix, item)


work_dir = os.path.dirname((os.path.abspath(__file__)))
runner_dir = os.path.dirname((os.path.realpath(__file__)))

with open(os.path.join(work_dir, 'etc', 'runner.json')) as f:
    runner_config = json_loadf(f)

runner_config['work_dir'] = work_dir
os.environ['PACKAGE_ROOT_DIR'] = work_dir

argparser = ArgumentParser()
helper = Helper(runner_config)

for name in runner_config.get('modules', []):
    mod = load_module(name, runner_dir)
    mod.initialize(runner_config, argparser, helper)

dispatch(argparser)
