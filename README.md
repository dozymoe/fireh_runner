# Fireh Runner

Manage console programs of multiple sub-projects.

See video demo: https://www.youtube.com/watch?v=qEKoDQ-WB5M  
See demo project: https://github.com/dozymoe/fireh_runner_demo


## Installation

`git clone` into a directory under your main project, then create a symlink of
"fireh_runner.py", for example: `ln -s fireh_runner/fireh_runner.py runner`.

Then create "etc/runner.json" with the content like this:

    {
        "modules": [
            "fireh_runner.modules.setup",
            "fireh_runner.modules.pip",
            "fireh_runner.modules.django",
            "fireh_runner.modules.uwsgi_django",
            "fireh_runner.modules.waf"
        ],
        "setup_modules": [
            "fireh_runner.setup_modules.git",
            "fireh_runner.setup_modules.python",
            "fireh_runner.setup_modules.alembic",
            "fireh_runner.setup_modules.npm",
            "fireh_runner.setup_modules.bower",
            "fireh_runner.setup_modules.pybuildtool"
        ],
        "package_name": "my_blog",
        "default_project": "blog",
        "default_variant": "development",

        "python_version": "3.5",
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

Just run `./runner` to see what options you have, these commands were
provided by "modules" section in "etc/runner.json".

If you run something like `./runner pip install --upgrade MODULE`, this will
break with `error: unrecognized arguments: --upgrade MODULE`. Do it like this:
`./runner pip install MODULE -- --upgrade`, there is "--" before "--upgrade".

Run `./runner pip --help` and you'll see that the pip command only recognize
`args` as positional arguments and `--help` as optional arguments, it doesn't
recognize `--upgrade`.


## Windows users

If you wanted to use `runner setup` you need symlink support.

You need to be regular user (not administrators), and the Local Policies for
creating symbolic links needs to be tweaked, see:
http://stackoverflow.com/a/8464306

Instructions:

1. Run gpedit.msc

2. Browse to "Computer Configuration" - "Windows Settings" -
   "Security Settings" - "Local Policies" - "User Rights Assignment" -
   "Create symbolic links"

Create this runner.bat:

    SET ROOT_DIR=%~dp0
    SET PYTHON3.5_BIN=C:\Python35\python.exe

    %PYTHON3.5_BIN% %ROOT_DIR%\fireh_runner\fireh_runner.py %*

You could then run `runner.bat setup` or `runner.bat pip-install django`

If you have error like "no module named win32api", run
`runner.bat pip-install pypiwin32`.
