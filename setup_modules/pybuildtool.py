import os
from subprocess import check_call
import sys

if sys.version_info[0] < 3:
    class urllib:
        parse = __import__("urllib")
        request = __import__("urllib2")
else:
    import urllib.request
    import urllib.parse


def setup(loader, variant):
    work_dir = loader.config['work_dir']
    venv_dir = os.path.realpath(os.path.join(work_dir,
            loader.config['virtualenv_dir']))

    waf_path = os.path.join(venv_dir, 'bin', 'waf')
    waf_ver_path = os.path.join(venv_dir, 'bin',
            'waf-' + loader.config['waf_version'])

    if not os.path.exists(waf_ver_path):
        print('Downloading waf...')
        resp = urllib.request.urlopen('http://waf.io/waf-' +\
                loader.config['waf_version'], timeout=30).read()

        with open(waf_ver_path, 'wb') as f:
            f.write(resp)

        os.chmod(waf_ver_path, int('755', 8))
    loader.force_symlink(waf_ver_path, waf_path)

    build_path = os.path.join(work_dir, 'build.yml')
    build_var_path = os.path.join(work_dir, 'build-%s.yml' % variant)
    if os.path.exists(build_var_path):
        loader.force_symlink(build_var_path, build_path)

    wscript_path = os.path.join(work_dir, 'wscript')
    wscript_var_path = os.path.join(work_dir, 'wscript-' + variant)
    if os.path.exists(wscript_var_path):
        loader.force_symlink(wscript_var_path, wscript_path)

    if os.path.exists(wscript_path):
        loader.setup_virtualenv()
        check_call(['waf', 'configure'])
        check_call(['waf', 'clean', 'build'])
