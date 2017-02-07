# Fireh Runner

Manage console programs of multiple sub-projects.

See demo project: https://github.com/dozymoe/fireh_runner_demo


## Installation

`git clone` into a directory under your main project, then create a symlink of
"fireh_runner.py", for example: `ln -s fireh_runner/fireh_runner.py runner`.

Then create "etc/runner.json" with the content like this:

    {
        "modules": [
            "fireh_runner.django",
            "fireh_runner.pip",
            "fireh_runner.uwsgi_django",
            "fireh_runner.waf"
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
        "system_site_packages": false,
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

Then in the directory of your main project, run:

    mklink runner fireh_runner\fireh_runner.py

Create the following runner.bat:

    SET PYTHON3.5_BIN=C:\Python35\python.exe

    C:\Python27\python.exe runner %*

Or without the runner symlink, with this runner.bat:

    SET ROOT_DIR=C:\Users\USERNAME\Documents\MYPROJECT
    SET PYTHON3.5_BIN=C:\Python35\python.exe

    C:\Python27\python.exe %ROOT_DIR%\fireh_runner\fireh_runner.py %*

You could then run `runner.bat setup` or `runner.bat pip-install django`

If you have error like "no module named win32api", run
`runner.bat pip-install pypiwin32`.
