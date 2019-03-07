import configparser
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

conf = configparser.ConfigParser()
conf_file = 'apt-get-install-tests/config.ini'


def dockerized():
    with open('/proc/self/cgroup', 'r') as procfile:
        for line in procfile:
            fields = line.strip().split('/')
            if 'docker' in fields:
                return True
    return False


if dockerized():
    conf.read(conf_file)
else:
    conf.read(conf_file.split('/')[1])
