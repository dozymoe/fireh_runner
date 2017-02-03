#!/usr/bin/env python

from argparse import ArgumentParser
from collections import Mapping, Sequence
import errno
from importlib import import_module
from json import load as json_loadf
import inspect
import os
import sys

def flatten_dict(prefix, data):
    # see http://stackoverflow.com/a/6036037
    for key in data:
        item = data[key]
        if prefix:
            new_prefix = prefix + '_' + key.upper()
        else:
            new_prefix = key.upper()

        try:
            is_str = isinstance(item, basestring)
        except NameError:
            is_str = isinstance(item, str)

        if isinstance(item, Mapping):
            for child_item in flatten_dict(new_prefix, item):
                yield child_item
        elif isinstance(item, Sequence) and not is_str:
            yield (new_prefix, ';'.join(item))
        else:
            yield (new_prefix, item)


class Loader(object):

    config = None

    _modules = None

    def __init__(self, config):
        self.config = config
        self._modules = []


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
        for key, value in flatten_dict('', data):
            os.environ[key] = value


    def setup_virtualenv(self):
        bin_path = os.path.join(
            self.config['work_dir'],
            self.config['virtualenv_dir'],
            'bin'
        )
        paths = os.environ['PATH'].split(os.pathsep)
        if paths[0] != bin_path:
            paths.insert(0, bin_path)
            os.environ['PATH'] = os.pathsep.join(paths)

        os.environ['PYTHONPATH'] = os.path.join(
            self.config['work_dir'],
            self.config['virtualenv_dir'],
            'lib',
            'python' + self.config['python_version'],
            'site-packages',
        )


    def register(self, argparser, module):
        self._modules.append(module)

        for function in module.commands:
            name = function.__name__.replace('_', '-')

            command = argparser.add_parser(name, help=inspect.getdoc(function))
            args, varargs, _, defaults = inspect.getargspec(function)
            if args[0] == 'self':
                args.pop(0)
            if args[0] == 'loader':
                args.pop(0)

            if defaults is not None:
                for arg in args[0:-len(defaults)]:
                    name = arg.replace('_', '-')
                    command.add_argument('--' + name, dest=arg, required=True)

                for index, default in enumerate(reversed(defaults)):
                    arg = args[-1 - index]
                    name = arg.replace('_', '-')
                    command.add_argument('--' + name, dest=arg, default=default)
            else:
                for arg in args:
                    name = arg.replace('_', '-')
                    command.add_argument('--' + name, dest=arg, required=True)

            if varargs is not None:
                command.add_argument(varargs, nargs='*')


    def execute(self, arguments):
        for module in self._modules:
            for function in module.commands:
                name = function.__name__.replace('_', '-')

                if name != arguments._command_:
                    continue

                args, varargs, _, _ = inspect.getargspec(function)
                if args[0] == 'self':
                    args.pop(0)
                if args[0] == 'loader':
                    args.pop(0)

                args = [getattr(arguments, arg) for arg in args]
                if varargs is not None:
                    args.extend(getattr(arguments, varargs))
                return function(self, *args)


    @staticmethod
    def force_symlink(target, link_name):
        try:
            os.symlink(target, link_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(link_name)
                os.symlink(target, link_name)
            else:
                raise e


    @staticmethod
    def load_module(module):
        """Load a python module by its name."""
        try:
            return import_module(module)
        except ImportError:
            sys.stderr.write('Unable to load the module: %s.\n' % module)
            exit(-1)


work_dir = os.path.dirname(os.path.abspath(__file__))
runner_dir = os.path.dirname(os.path.realpath(__file__))
sys.path[0] = work_dir

try:
    with open(os.path.join(work_dir, 'etc', 'runner.json')) as f:
        runner_config = json_loadf(f)
except Exception as e: # pylint:disable=broad-except
    sys.stderr.write('Unable read configuration file:\n' + repr(e) + '\n')
    exit(-1)

runner_config['work_dir'] = work_dir
os.environ['ROOT_DIR'] = work_dir

argparse = ArgumentParser()
subparsers = argparse.add_subparsers(dest='_command_')
loader = Loader(runner_config)

for module_name in runner_config.get('modules', []):
    mod = loader.load_module(module_name)
    loader.register(subparsers, mod)

exit(loader.execute(argparse.parse_args()))
