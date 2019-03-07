import configparser
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

conf = configparser.ConfigParser()
print(os.getcwd())
conf.read('apt-get-install-tests/config.ini')
