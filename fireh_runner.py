#!/usr/bin/env python

from argparse import ArgumentParser
from collections import Mapping, Sequence
import ctypes
from distutils.spawn import find_executable # pylint:disable=no-name-in-module,import-error
import errno
from importlib import import_module
from json import load as json_loadf
import inspect
import os
import signal
from subprocess import check_output, Popen
import sys

try:
    input = raw_input # pylint:disable=redefined-builtin
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
    _python_bin = None
    _CSL = None

    def __init__(self, config):
        self.config = config
        self._modules = []

        if os.name == 'nt':
            os.execvp = self._win_execvp

            if not hasattr(os, 'symlink'):
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


    @staticmethod
    def fix_dir_separator(slash_delim_path):
        """ Text replace directory separator.

        Replace slash character (/) with the OS' directory separator.
        """
        return slash_delim_path.replace('/', os.path.sep)


    def expand_path(self, original_path):
        """ Get real path relative to project root dir.
        """
        path = self.fix_dir_separator(original_path)
        path = os.path.expanduser(path)
        return os.path.join(self.config['work_dir'], path)


    def register(self, argparser, module):
        self._modules.append(module)

        for function in module.commands:
            name = function.__name__.replace('_', '-')

            command = argparser.add_parser(name, help=inspect.getdoc(function))

            args = list(self.get_function_signature(function))
            if args[0][0] == 'self':
                args.pop(0)
            if args[0][0] == 'loader':
                args.pop(0)

            for arg in args:
                if len(arg) == 1:
                    command.add_argument(arg[0], nargs='*')
                elif len(arg) == 2:
                    name = arg[0].replace('_', '-')
                    command.add_argument('--' + name, dest=arg[0],
                            required=True, type=arg[1])
                else:
                    name = arg[0].replace('_', '-')
                    command.add_argument('--' + name, dest=arg[0],
                            default=arg[2], type=arg[1])


    def execute(self, arguments):
        for module in self._modules:
            for function in module.commands:
                name = function.__name__.replace('_', '-')

                if name != arguments._command_:
                    continue

                args = list(self.get_function_signature(function))
                if args[0][0] == 'self':
                    args.pop(0)
                if args[0][0] == 'loader':
                    args.pop(0)

                params = []
                for arg in args:
                    if len(arg) == 1:
                        params.extend(getattr(arguments, arg[0]))
                    else:
                        params.append(getattr(arguments, arg[0]))

                return function(self, *params)


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
        python_bin = getattr(self, '_python_bin', None)
        if python_bin is not None:
            return python_bin

        python_bin = 'python' + self.config['python_version']
        self._python_bin = find_executable(python_bin)
        if self._python_bin is None:
            shellenv_key = python_bin.upper() + '_BIN'
            if shellenv_key in os.environ:
                self._python_bin = os.environ[shellenv_key]
            else:
                self._python_bin = input(python_bin + ' executable location: ')

        return self._python_bin


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
                'python' + self.config['python_version'], 'site-packages')

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


    def _win_execvp(self, cmd, argv):
        # see:
        # https://github.com/jupyter/jupyter_core/pull/54
        # https://github.com/jupyter/jupyter_core/pull/88
        process = Popen([cmd] + argv[1:], shell=True)
        # Don't raise KeyboardInterrupt in the parent process.
        # Set  this after spawning, to avoid subprocess inheriting handler.
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        process.wait()
        sys.exit(process.returncode)


    @staticmethod
    def get_function_signature(func):
        try:
            signature = inspect.signature(func)
            for name, param in signature.parameters.items():
                if param.kind == param.VAR_POSITIONAL:
                    yield (name,)
                elif param.kind == param.VAR_KEYWORD:
                    continue
                else:

                    if param.annotation is param.empty:
                        type_ = None
                    else:
                        type_ = param.annotation

                    if param.default is param.empty:
                        yield (name, type_)
                    else:
                        yield (name, type_, param.default)

        except AttributeError:
            args, varargs, _, defaults = inspect.getargspec(func) # pylint:disable=deprecated-method

            if defaults is not None:
                n_non_default = len(args) - len(defaults)
                for arg in args[0:n_non_default]:
                    yield (arg, None)

                for index, arg in enumerate(args[n_non_default:]):
                    default = defaults[index + 1 - n_non_default]
                    yield (arg, None, default)

            else:
                for arg in args:
                    yield (arg, None)

            if varargs is not None:
                yield (varargs,)

    @staticmethod
    def fix_pathname(dos_path):
        fixed_path = dos_path.replace('\\', os.path.sep)
        fixed_path = fixed_path.replace('/', os.path.sep)

        if sys.platform == 'msys':
            return os.path.join('/', fixed_path.replace(':', ''))
        elif sys.platform == 'cygwin':
            return os.path.join('/cygdrive',
                    fixed_path.replace(':', ''))

        return fixed_path


root_dir = os.environ.get('ROOT_DIR', os.path.dirname(
        os.path.abspath(__file__)))

root_dir = Loader.fix_pathname(root_dir)

runner_dir = os.path.dirname(os.path.realpath(__file__))
sys.path[0] = root_dir

try:
    with open(os.path.join(root_dir, 'etc', 'runner.json')) as f:
        runner_config = json_loadf(f)
except Exception as e: # pylint:disable=broad-except
    sys.stderr.write('Unable read configuration file:\n' + repr(e) + '\n')
    exit(-1)

runner_config['work_dir'] = root_dir
os.environ['ROOT_DIR'] = root_dir

argparse = ArgumentParser()
subparsers = argparse.add_subparsers(dest='_command_')
loader = Loader(runner_config)

for module_name in runner_config.get('modules', []):
    mod = loader.load_module(module_name)
    loader.register(subparsers, mod)

os.chdir(root_dir)
exit(loader.execute(argparse.parse_args()))
