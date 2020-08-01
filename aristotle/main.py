__title__ = 'aristotle'
__author__ = 'Erdi Gurbuz'
__license__ = 'GNU3'
__copyright__ = 'Copyright 2013, Erdi Gurbuz'

import argparse

from news import News

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Usage aristotle")
    parser.add_argument("-c", "--categories", type=str, help="Which categories will be fetch (separate by commas)")
    args = parser.parse_args()

    News(args.categories).start()