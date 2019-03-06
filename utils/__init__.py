import configparser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

conf = configparser.ConfigParser()
conf.read('config.ini')
