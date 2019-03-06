from subprocess import Popen, PIPE
import re
import configparser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

conf = configparser.ConfigParser()
conf.read('config.ini')


def run(cmd):
    cmd = cmd.split()
    sudo_cmd = ['sudo', '-S'] + cmd
    p = Popen(sudo_cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE,
              universal_newlines=True)
    prompt = p.communicate('  ' + '\n')
    return {'stdout': prompt[0],
            'stderr': prompt[1],
            'pid': p.pid}


def package_installed(package_name):  # TODO: namedtuple
    out = None
    std = run('dpkg -l')['stdout']
    lines = std.split('\n')
    pattern = r'ii\s*([^ \n]*)\s*([^ \n]*)\s*([^ \n]*)\s*([\w\s]*)\s'
    for line in lines:
        pkg = re.match(pattern, line)
        if pkg:
            if package_name and any([package_name == pkg.groups()[0],
                                     package_name in pkg.groups()[3]]):
                out = pkg.groups()
    return out
