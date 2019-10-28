import os
from shutil import copyfile, rmtree
from subprocess import call, check_call
import sys

if sys.version_info[0] < 3:
    class urllib:
        parse = __import__("urllib")
        request = __import__("urllib2")
    from urllib2 import URLError #pylint:disable=import-error
else:
    import urllib.request
    import urllib.parse
    from urllib.error import URLError


def setup(loader, variant):
    work_dir = loader.config['work_dir']
    venv_dir = loader.get_virtualenv_dir()
    venv_bin_dir = os.path.join(venv_dir, 'bin')

    waf_path = os.path.join(venv_bin_dir, 'waf')
    waf_ver_path = os.path.join(venv_bin_dir,
            'waf-' + loader.config['waf_version'])

    use_symlink = not loader.config.get('no_symlink_please', False)

    if use_symlink:
        link_fn = loader.force_symlink
    else:
        link_fn = copyfile

    if not os.path.exists(waf_ver_path):
        print('Downloading waf...')
        try:
            resp = urllib.request.urlopen('https://waf.io/waf-' +\
                    loader.config['waf_version'], timeout=30).read()
        except URLError:
            # mirror
            resp = urllib.request.urlopen(
                    'https://www.freehackers.org/~tnagy/release/waf-' +\
                    loader.config['waf_version'], timeout=30).read()

        with open(waf_ver_path, 'wb') as f:
            f.write(resp)

        os.chmod(waf_ver_path, int('755', 8))

    link_fn(waf_ver_path, waf_path)

    if os.name == 'nt':
        print('Downloading waf.bat...')
        resp = urllib.request.urlopen('https://raw.githubusercontent.com/' +\
                'waf-project/waf/master/utils/waf.bat', timeout=30).read()

        with open(os.path.join(venv_bin_dir, 'waf.bat'), 'wb') as f:
            f.write(resp)

    build_path = os.path.join(work_dir, 'build.yml')
    build_var_path = os.path.join(work_dir, 'build-%s.yml' % variant)
    if os.path.exists(build_var_path):
        link_fn(build_var_path, build_path)

    wscript_path = os.path.join(work_dir, 'wscript')
    wscript_var_path = os.path.join(work_dir, 'wscript-' + variant)
    if os.path.exists(wscript_var_path):
        link_fn(wscript_var_path, wscript_path)

    temp_build_path = os.path.join(work_dir, '.BUILD')
    if os.path.exists(temp_build_path):
        rmtree(temp_build_path)

    os.chdir(work_dir)

    if os.path.exists(wscript_path):
        loader.setup_virtualenv()
        check_call(loader.get_binargs('waf', 'configure'))
        call(loader.get_binargs('waf'))
