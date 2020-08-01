__title__ = 'aristotle'
__author__ = 'Erdi Gurbuz'
__license__ = 'GNU3'
__copyright__ = 'Copyright 2013, Erdi Gurbuz'

import argparse
import logging.config
import yaml
import locale

from aristotle.news import News

with open(r'config/properties.yaml') as file:
    props = yaml.load(file, Loader=yaml.FullLoader)

loc = props.get("locale")

with open(r'config/sources-%s.yaml'%loc) as file:
    sources = yaml.load(file, Loader=yaml.FullLoader)

locale.setlocale(locale.LC_ALL, loc)

logging.config.dictConfig(yaml.load(open('config/logging.yaml', 'r'), Loader=yaml.FullLoader))

parser = argparse.ArgumentParser(description = "Usage aristotle")
parser.add_argument("-c", "--categories", type=str, help="Which categories will be fetch (separate by commas)")
args = parser.parse_args()

news = News(props, sources, args.categories)
