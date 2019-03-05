# from utils import package_installed


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


def test_older_version():
    pass


def test_unknown_package(exc):
    """
    validate proper handle of unsuccessful installation
    """
    dummy_package = 'foobar'
    run = exc.install(dummy_package)
    assert 'Unable to locate package %s' % dummy_package in run['stderr']
    assert run['rc'] == 100


def test_unknown_version():
    pass


def test_no_connection():
    pass


def test_multiple_instances(exc):
    """
    check apt-get install cannot run in parallel
    """
    cmd = 'apt-get install'
    run = exc.commands([cmd] * 2)
    assert 'Could not get lock' in run[cmd]
    assert 'Unable to acquire the dpkg frontend lock' in run[cmd]


def test_sigkill(exc):
    pass


def test_missing_lock_files(remove_lock_files, exc):
    print(exc.run('apt-get install'))


def test_install_itself(exc):
    package = 'apt'
    assert ('is already the newest version (%s)' % exc.package_installed(package).version
            in exc.install(package)['stdout'])
