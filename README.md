# Fireh Runner

Manage console programs of multiple sub-projects.

See video demo: https://www.youtube.com/watch?v=qEKoDQ-WB5M  
See demo project: https://github.com/dozymoe/fireh\_runner\_demo


## Installation

`git clone` into a directory under your main project, usually under "lib", for
example: `git submodule add https://github.com/dozymoe/fireh_runner lib/fireh_runner`

Then create a symlink of "fireh\_runner.py", for example:
`ln -s lib/fireh_runner/fireh_runner.py run`.

Then create "etc/runner.json" with the content like this:

    {
        "modules": [
            "lib.fireh_runner.modules.setup",
            "lib.fireh_runner.modules.pip",
            "lib.fireh_runner.modules.django",
            "lib.fireh_runner.modules.uwsgi_django",
            "lib.fireh_runner.modules.waf"
        ],
        "setup_modules": [
            "lib.fireh_runner.setup_modules.git",
            "lib.fireh_runner.setup_modules.python",
            "lib.fireh_runner.setup_modules.alembic",
            "lib.fireh_runner.setup_modules.npm",
            "lib.fireh_runner.setup_modules.pybuildtool"
        ],

        "package_name": "my_blog",
        "default_project": "blog",
        "default_variant": "development",
        "variant_is_production": false,

        "python_version": "3.5",
        "virtualenv_type": "python",
        "virtualenv_dir": ".virtualenv",
        "no_symlink_please": false,
        "pip_install_args": [
            "--only-binary", ":all:"
        ],

        "configuration": {
            "development": {
                "blog": {
                    "worker_count": 1,
                    "max_requests": 5000,
                    "socket_path": "./tmp/sockets/blog.sock"
                }
            }
        }
    }



## Using

Just run `./run --help` to see what options you have, these commands were
provided by "modules" section in "etc/runner.json".

If you run something like `./run pip install --upgrade MODULE`, this will
break with `error: unrecognized arguments: --upgrade MODULE`. Do it like this:
`./run pip install MODULE -- --upgrade`, there is "--" before "--upgrade".

Run `./run pip --help` and you'll see that the pip command only recognize
`args` as positional arguments and `--help` as optional arguments, it doesn't
recognize `--upgrade`.

By default fireh\_runner uses PYTHONUSERBASE, you can set `virtualenv_type`
to "virtualenv" to use python-virtualenv instead.


## Windows users

If you wanted to use `run setup` you need symlink support, or you can set
`no_symlink_please` to `true` then files will be copied instead.

For enabling symlink support you need to be regular user (not administrators),
and the Local Policies for creating symbolic links needs to be tweaked, see:
http://stackoverflow.com/a/8464306

Instructions:

1. Run gpedit.msc

2. Browse to "Computer Configuration" - "Windows Settings" -
   "Security Settings" - "Local Policies" - "User Rights Assignment" -
   "Create symbolic links"

Create this run.bat:

    SET ROOT_DIR=%~dp0
    SET PYTHON3_7_BIN=C:\Python37\python.exe

    %PYTHON3_7_BIN% %ROOT_DIR%\lib\fireh_runner\fireh_runner.py %*

You could then run `run.bat setup` or `run.bat pip install django`

If you have error like "no module named win32api", run
`run.bat pip install pypiwin32`.
