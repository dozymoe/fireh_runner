#!/usr/bin/env python

from argparse import ArgumentParser, RawDescriptionHelpFormatter
try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence
from copy import deepcopy
import ctypes
from distutils.spawn import find_executable # pylint:disable=no-name-in-module,import-error
import errno
from importlib import import_module
from json import load as json_loadf
import inspect
import os
import signal
from subprocess import Popen
import sys

try:
    input = raw_input # pylint:disable=redefined-builtin
except NameError:
    pass


def merge_dict(result, *dicts):
    for data in dicts:
        for k, v in data.items():
            if k in result:
                try:
                    is_str = isinstance(v, basestring)
                except NameError:
                    is_str = isinstance(v, str)

                if isinstance(v, Mapping):
                    # Will raise exception if result[k] is not a Mapping
                    merge_dict(result[k], v)
                elif isinstance(v, Sequence) and not is_str:
                    result[k].extend(deepcopy(v))
                else:
                    result[k] = deepcopy(v)
            else:
                result[k] = deepcopy(v)


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
            yield (new_prefix, os.pathsep.join(item))
        else:
            yield (new_prefix, item)


class Loader():

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
                self.config.get('default_variant', 'default'))

        if self.config.get('variant_is_production') or\
                variant in ['prod', 'production', 'staging', 'stage']:
            is_prod = '1'
        else:
            is_prod = '0'

        os.environ['PROJECT_NAME'] = project
        os.environ['PROJECT_VARIANT'] = variant
        os.environ['PROJECT_VARIANT_IS_PRODUCTION'] = is_prod
        return project, variant


    def setup_shell_env(self, data=None):
        config = self.get_project_config()
        env = config.get('shell_env', {})
        for key, value in (data or {}).items():
            env[key] = value

        # Expand PYTHONPATH relative to project directory
        for idx, value in enumerate(env.get('PYTHONPATH', [])):
            env['PYTHONPATH'][idx] = os.path.join(self.config['work_dir'],
                    value)
        for key, value in flatten_dict('', env):
            os.environ[key] = value


    def setup_virtualenv(self):
        venv_dir = self.get_virtualenv_dir()
        venv_bin_dir = os.path.join(venv_dir, 'bin')
        venv_type = self.config.get('virtualenv_type', 'python')

        self._python_bin = None

        if venv_type in ('venv', 'virtualenv'):
            os.environ['VIRTUAL_ENV'] = venv_dir
            if 'PYTHONHOME' in os.environ:
                del os.environ['PYTHONHOME']

        else:
            # PYTHONUSERBASE is the default
            os.environ['PYTHONUSERBASE'] = venv_dir
            if 'VIRTUAL_ENV' in os.environ:
                del os.environ['VIRTUAL_ENV']

        paths = os.environ['PATH'].split(os.pathsep)
        if paths[0] != venv_bin_dir:
            paths.insert(0, venv_bin_dir)
            os.environ['PATH'] = os.pathsep.join(paths)

        return venv_type


    def get_project_config(self):
        project = os.environ['PROJECT_NAME']
        variant = os.environ['PROJECT_VARIANT']

        config = self.config.get('configuration', {})
        config = config.get(variant, {})
        conf = {}
        # empty string is configuration key that applies to all projects
        merge_dict(conf, config.get('', {}), config.get(project, {}))
        return conf


    def is_production(self):
        return os.environ.get('PROJECT_VARIANT_IS_PRODUCTION') == '1'


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

            desc = inspect.getdoc(function)
            if desc:
                desc = desc.strip()
                head = desc.splitlines()[0]
            else:
                head = None
            command = argparser.add_parser(name, help=head, description=desc,
                    formatter_class=RawDescriptionHelpFormatter)

            params = list(self.get_function_signature(function))
            # First argument/params is always the Loader instance.
            params.pop(0)
            for param in params:
                if len(param) == 1:
                    command.add_argument(param[0], nargs='*')
                elif len(param) == 2:
                    name = param[0].replace('_', '-')
                    command.add_argument('--' + name, dest=param[0],
                            required=True, type=param[1])
                else:
                    name = param[0].replace('_', '-')
                    command.add_argument('--' + name, dest=param[0],
                            default=param[2], type=param[1])


    def execute(self, arguments):
        known, unknown = arguments
        for module in self._modules:
            for function in module.commands:
                name = function.__name__.replace('_', '-')

                if name != known._command_:
                    continue

                args = []
                kwargs = {}
                params = list(self.get_function_signature(function))
                # First argument/params is always the Loader instance.
                params.pop(0)
                for param in params:
                    if len(param) == 1:
                        args.extend(getattr(known, param[0], []))
                    elif param[0] in ('self', 'loader'):
                        args.append(self)
                    else:
                        try:
                            default = param[2]
                        except IndexError:
                            default = None
                        args.append(getattr(known, param[0], default))

                args.extend(unknown)
                return function(self, *args, **kwargs)


    @staticmethod
    def force_symlink(target, link_name):
        try:
            os.symlink(target, link_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(link_name)
                os.symlink(target, link_name)
            else:
                pass


    @staticmethod
    def load_module(module):
        """Load a python module by its name."""
        try:
            return import_module(module)
        except ImportError:
            sys.stderr.write('Unable to load the module: %s.\n' % module)
            sys.exit(-1)


    def get_virtualenv_dir(self):
        return os.path.join(self.config['work_dir'],
                self.config.get('virtualenv_dir', '.virtualenv'))


    def get_binargs(self, script, *args):
        venv_dir = self.get_virtualenv_dir()
        script_path = os.path.join(venv_dir, 'bin', script)
        if os.path.exists(script_path):
            python_bin = self.get_python_bin()
            executable = [python_bin, script_path]
        else:
            raise RuntimeError('Cannot find executable for ' + script)

        return executable + list(args)


    def get_python_bin(self, cache=True):
        if cache:
            python_bin = getattr(self, '_python_bin', None)
            if python_bin is not None:
                os.environ['PYTHON_BIN'] = python_bin
                return python_bin

        python_bin = 'python' + self.config['python_version']
        shellenv_key = python_bin.replace('.', '_').upper() + '_BIN'
        if shellenv_key in os.environ:
            self._python_bin = os.environ[shellenv_key]
        else:
            self._python_bin = find_executable(python_bin)
            if not self._python_bin and os.environ.get('VIRTUAL_ENV'):
                self._python_bin = os.path.join(os.environ['VIRTUAL_ENV'], 'bin',
                        'python')
        if self._python_bin is None:
            self._python_bin = input(python_bin + ' executable location: ')

        os.environ['PYTHON_BIN'] = self._python_bin
        return self._python_bin


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
        if sys.platform == 'cygwin':
            return os.path.join('/cygdrive',
                    fixed_path.replace(':', ''))

        return fixed_path


if __name__ == '__main__':
    current_dir = os.environ.get('CURRENT_DIR', os.getcwd())
    root_dir = os.environ.get('ROOT_DIR', os.path.dirname(
            os.path.abspath(__file__)))

    root_dir = Loader.fix_pathname(root_dir)

    runner_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path[0] = root_dir

    try:
        if 'RUNNER_CONFIG_FILE' in os.environ:
            runner_config_file = os.environ['RUNNER_CONFIG_FILE']
        else:
            runner_config_file = os.path.join(root_dir, 'etc', 'runner.json')
            os.environ['RUNNER_CONFIG_FILE'] = runner_config_file

        with open(runner_config_file) as f:
            runner_config = json_loadf(f)
    except Exception as e: # pylint:disable=broad-except
        sys.stderr.write('Unable read configuration file etc/runner.json:\n' +\
                repr(e) + '\n')

        sys.exit(-1)

    runner_config['work_dir'] = root_dir
    os.environ['ROOT_DIR'] = root_dir

    runner_config['current_dir'] = current_dir
    os.environ['CURRENT_DIR'] = current_dir

    argparse = ArgumentParser()
    subparsers = argparse.add_subparsers(dest='_command_')
    loader = Loader(runner_config)

    for module_name in runner_config.get('modules', []):
        mod = loader.load_module(module_name)
        loader.register(subparsers, mod)

    os.chdir(root_dir)
    sys.exit(loader.execute(argparse.parse_known_args()))
