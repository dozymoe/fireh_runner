#!/usr/bin/env python

from argparse import ArgumentParser
from collections import Mapping, Sequence
from copy import copy
import ctypes
from distutils.spawn import find_executable
import errno
from importlib import import_module
from json import load as json_loadf
import inspect
import os
from subprocess import check_output
import sys

try:
    input = raw_input
except NameError:
    pass


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

        if not hasattr(os, 'symlink') and os.name == 'nt':
            os.symlink = self._win_symlink


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
        ## python path

        if self.config.get('system_site_packages'):
            environ_key = 'PYTHON%s_PYTHONPATH' % self.config['python_version']
            python_path = os.environ.get(environ_key)
            if python_path is None:
                python_path = check_output([
                    self.get_python_bin(),
                    '-c',
                    'import os, site; ' +\
                        'print(os.pathsep.join(site.getsitepackages()))'
                ]).rstrip()
                os.environ[environ_key] = python_path
        else:
            python_path = ''

        venv_packages = self.get_virtualenv_sitepackages()
        site_path = [p for p in python_path.split(os.pathsep) if p]
        if len(site_path) == 0 or site_path[0] != venv_packages:
            site_path.insert(0, venv_packages)

        os.environ['PYTHONPATH'] = os.pathsep.join(site_path)

        ## bin path

        bin_path = self.get_virtualenv_bin()
        paths = os.environ['PATH'].split(os.pathsep)
        if paths[0] != bin_path:
            paths.insert(0, bin_path)
            os.environ['PATH'] = os.pathsep.join(paths)


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


    def get_python_bin(self):
        python_bin = getattr(self, '_python_bin')
        if python_bin is not None:
            return python_bin

        python_bin = 'python' + self.config['python_version']
        if find_executable(python_bin) is None:
            shellenv_key = python_bin.upper() + '_BIN'
            if shellenv_key in os.environ:
                python_bin = os.environ[shellenv_key]
            else:
                python_bin = input(python_bin + ' executable location: ')

        self._python_bin = python_bin
        return python_bin


    def get_virtualenv_bin(self):
        work_dir = self.config['work_dir']
        venv_dir = os.path.realpath(os.path.join(work_dir,
                self.config['virtualenv_dir']))

        bin_dir = os.path.join(venv_dir, 'bin')
        if os.path.isdir(bin_dir):
            return bin_dir

        # windows
        bin_dir = os.path.join(venv_dir, 'Scripts')
        if os.path.isdir(bin_dir):
            return bin_dir

        sys.stderr.write("Unable to find virtualenv's binary directory.\n")
        exit(-1)


    def get_virtualenv_sitepackages(self):
        work_dir = self.config['work_dir']
        venv_dir = os.path.realpath(os.path.join(work_dir,
                self.config['virtualenv_dir']))

        packages_dir = os.path.join(venv_dir, 'lib',
                'python' + self.config['python_version', 'site-packages')

        if os.path.isdir(packages_dir):
            return packages_dir

        # windows
        packages_dir = os.path.join(venv_dir, 'Lib', 'site-packages')
        if os.path.isdir(packages_dir):
            return packages_dir

        sys.stderr.write("Unable to find virtualenv's site-packages.\n")
        exit(-1)


    def _win_symlink(self, target, link_name):
        # see http://stackoverflow.com/a/8464306
        if not hasattr(self, '_CSL'):
            csl = ctypes.windll.kernel32.CreateSymbolicLinkW
            csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
            csl.restype = ctypes.c_ubyte
            self._CSL = csl

        if target is not None and os.path.isdir(target):
            flags = 1
        else:
            flags = 0

        if self._CSL(link_name, target, flags) == 0:
            raise ctypes.WinError()


work_dir = os.environ.get('ROOT_DIR', os.path.dirname(
        os.path.abspath(__file__)))

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
