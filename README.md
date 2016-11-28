# Fireh Runner

Manage console programs of multiple sub-projects.


## Installation

`git clone` into a directory under your main project, then create a symlink of
"fireh_runner.py", for example: `ln -s fireh_runner/fireh_runner.py runner`.

Then create "etc/runner.json" with the content like this:

```
{
    "modules": [
        "django",
        "pip",
        "uwsgi_django",
        "waf"
    ],
    "package_name": "my_blog",
    "default_project": "blog",
    "default_variant": "development",

    "python_version": "3.4",
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


## Dependency

* python-argh
