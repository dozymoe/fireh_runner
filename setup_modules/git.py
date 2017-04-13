from subprocess import check_call
import os

def setup(loader, variant):
    work_dir = loader.config['work_dir']

    if os.path.exists(os.path.join(work_dir, '.git')):
        check_call(['git', 'pull'])
        check_call(['git', 'submodule', 'update', '--init', '--recursive'])
