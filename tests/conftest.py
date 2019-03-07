from utils import *
from utils.execute import Execute
import pytest
from random import randint


packages = conf.get('install', 'packages').split(', ')


@pytest.fixture
def exc():
    exc = Execute(sudo=conf.get('install', 'sudo').strip('"'))
    yield exc


@pytest.fixture(params=[[packages[0]], packages])
def missing_packages(exc, request):
    exc.purge(request.param)
    assert not all(exc.package_installed(package) for package in request.param)
    yield request.param


@pytest.fixture(params=[packages[0]])
def install_packages(exc, request):
    exc.install(request.param)
    yield request.param


@pytest.fixture
def remove_lock_files(exc):
    exc.run('mv /etc/apt/sources.list sources.list.bck')
    yield
    exc.run('mv sources.list.bck /etc/apt/sources.list')


@pytest.fixture(params=['slow', 'loss'])
def bad_network(exc, request):
    if not exc.package_installed('tc'):
        exc.install('iproute2')
    cmd = {
        'slow': '/sbin/tc qdisc add dev enp0s3 root netem delay 1001ms',
        'loss': '/sbin/tc qdisc add dev enp0s3 root netem loss 25%'
    }
    exc.run(cmd[request.param])
    yield request.param
    exc.run('tc qdisc del dev enp0s3 root')


@pytest.fixture
def random_package():
    yield packages[randint(0, len(packages) - 1)]
