__title__ = 'aristotle'
__author__ = 'Erdi Gurbuz'
__license__ = 'GNU3'
__copyright__ = 'Copyright 2013, Erdi Gurbuz'

import logging.config
import sys
import yaml

from aristotle.news import News


def closeProcess(self):
    self.dbHandler.closeConnection()
    sys.exit(1)


with open(r'config/sources.yaml') as file:
    sources = yaml.load(file, Loader=yaml.FullLoader)

with open(r'config/properties.yaml') as file:
    props = yaml.load(file, Loader=yaml.FullLoader)

logging.config.dictConfig(yaml.load(open('config/logging.yaml', 'r'), Loader=yaml.FullLoader))

news = News("article", "haberturk.com", props, sources)
