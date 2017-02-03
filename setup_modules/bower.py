import os
from subprocess import check_call

def setup(loader, variant):
    work_dir = loader.config['work_dir']

    if os.path.exists(os.path.join(work_dir, 'bower.json')):
        check_call(['bower', 'install'])
