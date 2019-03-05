from utils import *
from utils.execute import Execute
import pytest


packages = conf.get('install', 'packages').split(', ')


@pytest.fixture
def exc():
    exc = Execute(sudo=conf.get('install', 'sudo').strip('"'))
    yield exc


@pytest.fixture(params=[[packages[0]], packages])
def missing_packages(exc, request):
    exc.purge(request.param)
    assert not all(package_installed(package) for package in request.param)
    yield request.param


@pytest.fixture(params=[packages[0]])
def install_packages(exc, request):
    exc.install(request.param)
    assert all(package_installed(package) for package in request.param)
    yield request.param


@pytest.fixture
def remove_lock_files(exc):
    exc.run('mv /etc/apt/sources.list sources.list.bck')
    yield
    exc.run('mv sources.list.bck /etc/apt/sources.list')
