# -*- coding: utf-8 -*-

from LogHandler import LogHandler
from ServerDatabaseHandler import ServerDatabaseHandler
from datetime import datetime
from SourceList import createNewsSource
import sys


class Main:
    def __init__(self):
        self.logHandler = LogHandler("FaultySources")
        self.serverHandler = ServerDatabaseHandler()
        self.run()

    def run(self):
        present = datetime.now()
        print("[%s] Starting" % str(datetime.now())[:19])
        sys.stdout.flush()

        for data in createNewsSource(present).iteritems():
            category = data[0]
            sources = data[1]

            for sourceList in sources:
                source = sourceList[0]
                if not self.serverHandler.executeQuery(
                        "SELECT id FROM `links_%s` WHERE date >= now() - interval 3 day and category='%s' and source='%s'"%
                        (str(present.strftime('%Y%m')), category, source)):
                    print(category, " -> ", source)

        self.serverHandler.closeConnection()
        sys.stdout.flush()


if __name__ == "__main__":
    main = Main()
