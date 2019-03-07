import configparser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

conf = configparser.ConfigParser()
# conf.read('apt-get-install-tests/config.ini')
conf.read('config.ini')
