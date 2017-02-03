# Fireh Runner

Manage console programs of multiple sub-projects.

See demo project: https://github.com/dozymoe/fireh_runner_demo


## Installation

`git clone` into a directory under your main project, then create a symlink of
"fireh_runner.py", for example: `ln -s fireh_runner/fireh_runner.py runner`.

Then create "etc/runner.json" with the content like this:

```
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
```
