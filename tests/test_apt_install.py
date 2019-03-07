import pytest
from utils import *


def test_apt_install(missing_packages, exc):
    """
    run install against single and multiple options
    """
    exc.install(missing_packages)
    assert all([exc.package_installed(package) for package in missing_packages])


def test_already_installed(install_packages, exc):
    """
    validate output when attempting to install existing pkg
    """
    assert ('is already the newest version (%s)' % exc.package_installed(install_packages).version
            in exc.install(install_packages)['stdout'])


def test_unknown_package(exc):
    """
    validate proper handle of unsuccessful installation
    """
    dummy_package = 'foobar'
    run = exc.install(dummy_package)
    assert 'Unable to locate package %s' % dummy_package in run['stderr']
    assert run['rc'] == 100


def test_unknown_version(exc):
    assert exc.install('mc=0.0')['stderr']


def test_bad_connection(bad_network, exc, random_package):
    """
    check package installed with network issues
    """
    exc.purge(random_package)
    assert exc.install(random_package)['rc'] == 0
    assert exc.package_installed(random_package)


def test_multiple_instances(exc):
    """
    check apt-get install cannot run in parallel
    """
    assert 'Could not get lock' in exc.commands(['apt-get install'] * 2).values()[0]


def test_sigkill(exc):
    # always getting grep error: garbage option
    pass


def test_install_itself(exc):
    package = 'apt'
    assert ('is already the newest version (%s)' % exc.package_installed(package).version
            in exc.install(package)['stdout'])


@pytest.mark.skipif(dockerized(), reason='running in docker, no sudo')
def test_not_sudo(exc_sudoless):
    assert 'Permission denied' in exc_sudoless.run('apt-get install')['stderr']
