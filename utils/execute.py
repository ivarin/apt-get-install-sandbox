from multiprocessing import Process, Manager
from time import sleep
from subprocess import Popen, PIPE
from utils import *
from collections import namedtuple


class Execute:
    def __init__(self, *args, **kwargs):
        self.sudo = kwargs.get('sudo') or kwargs.get('root')
        self.proc = None
        # self.stdout = None
        # self.stderr = None
        # self.rc = None

    def run(self, cmd, buff=None, sudo=True):
        logger.info('running %s' % cmd)
        cmd = cmd.split()
        sudo_cmd = ['sudo', '-S'] + cmd
        self.proc = Popen(sudo_cmd if sudo else cmd,
                          stderr=PIPE, stdout=PIPE, stdin=PIPE,
                          universal_newlines=True)

        # stderr = self.proc.stderr.read()

        prompt = self.proc.communicate(self.sudo + '\n')
        stdout = prompt[0]
        rc = self.proc.returncode
        if buff and stderr:
            buff.update({' '.join(cmd): stdout})
        return {
            'stdout': stdout,
            # 'stderr': stderr,
            'rc': rc
        }

    def commands(self, cmds: list):
        jobs = []
        manager = Manager()
        buff = manager.dict()
        for cmd in cmds:
            buff.update({cmd: ''})
            p = Process(target=self.run, args=(cmd, buff))
            jobs.append(p)
            sleep(0.5)
            p.start()

        for proc in jobs:
            proc.join(timeout=5)

        return buff

    def install(self, packages):
        packages = [packages] if type(packages) == str else packages
        cmd = 'apt-get install %s -y' % ' '.join(packages)
        return self.run(cmd)

    def purge(self, packages):
        cmd = 'apt-get purge %s -y' % ' '.join(packages)
        return self.run(cmd)

    def package_installed(self, package_name):
        out = None
        inst_pckg = namedtuple('installed_package', 'name version platform description')
        std = self.run('dpkg -l')['stdout']
        lines = std.split('\n')
        pattern = r'ii\s*([^ \n]*)\s*([^ \n]*)\s*([^ \n]*)\s*([\w\s]*)\s'
        for line in lines:
            pkg = re.match(pattern, line)
            if pkg:
                if package_name and any([package_name == pkg.groups()[0],
                                         package_name in pkg.groups()[3]]):
                    out = inst_pckg(*pkg.groups())
        return out

