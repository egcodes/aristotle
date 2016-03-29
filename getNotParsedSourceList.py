# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from LogHandler import LogHandler
from ServerDatabaseHandler import ServerDatabaseHandler
from datetime import datetime
from haberbusSources import createNewsSourceByPresent
import sys

class Main:
    def __init__(self):
	
        self.logHandler = LogHandler("Main")
        self.serverHandler = ServerDatabaseHandler()
        self.run()
	
    def run(self):
        present = datetime.now()
        self.yearMonth = str(present.strftime('%Y%m'))
        print "[%s] Starting" % str(datetime.now())[:19]
        sys.stdout.flush()
		
        #===========================================================
        # Kaynaklar olusturuluyor
        #===========================================================
        self.newsSources = createNewsSourceByPresent(present)
		
        for data in self.newsSources.iteritems():
            category = data[0]
            sources = data[1]
			
            for sourceList in sources:
                startSource = datetime.now()
                source = sourceList[0]
                if not self.serverHandler.executeQuery("SELECT id FROM `links_%s` WHERE date BETWEEN DATE_SUB(NOW(), INTERVAL 3 DAY) AND NOW() and category='%s' and source='%s'" % (self.yearMonth, category, source)):
                    print category, " -> ", source
				
        self.serverHandler.closeConnection()
        print "Finished\n"
        sys.stdout.flush()

if __name__ == "__main__":
    main = Main()
