import signal
import sys
import logging
import logging.config
from datetime import datetime

from LinkHandler import LinkHandler
from DbHandler import DbHandler
import Queries as query

from bs4 import BeautifulSoup
import requests
import yaml


class Parser:
    def __init__(self):
        with open(r'config/sources.yaml') as file:
            self.sources = yaml.load(file, Loader=yaml.FullLoader)

        with open(r'config/properties.yaml') as file:
            self.props = yaml.load(file, Loader=yaml.FullLoader)

        logging.config.dictConfig(yaml.load(open('config/logging.yaml', 'r'), Loader=yaml.FullLoader))
        self.log = logging.getLogger("Parser")

        self.dbHandler = DbHandler(self.props)

        self.yearMonth = ""

        if len(sys.argv) == 2:
            category = sys.argv[1]
            self.run(category)
        elif len(sys.argv) == 3:
            category = sys.argv[1]
            source = sys.argv[2]
            self.run(category, source)
        else:
            self.run()

    def run(self, category="", source=""):
        try:
            initCategory = ""
            initSource = ""
            if category:
                initCategory = category
                initSource = source

            present = datetime.now()
            self.yearMonth = str(present.strftime('%Y%m'))

            if present.hour == 0:
                self.dbHandler.executeQuery("TRUNCATE `link_cache`")

            self.log.info("Begin [%s]" % str(present)[:19])

            newsLinkDict = {}

            for category in self.sources:
                sources = self.sources.get(category)

                for source in sources:
                    startSource = datetime.now()
                    if initSource and source.get("domain") != initSource:
                        continue

                    link = source.get("link")
                    self.log.info("Link: %s", link)
                    try:
                        newsLinkDict.update(self.getNewsLinkFromSource(present, category, source.get("domain"), link))
                    except Exception as ex:
                        self.log.exception(ex)

                    self.log.info("Time: %s", str(datetime.now() - startSource)[:7])
                    self.insertToDatabase(newsLinkDict)
                    newsLinkDict.clear()

            self.log.info("End: " + str(datetime.now()) + " - " + str(datetime.now() - present)[:19])
        except Exception as ex:
            self.log.warning("run: ", ex)

    def getNewsLinkFromSource(self, present, category, domain, link):
        try:
            htmlSource = requests.get(link, headers={'User-Agent': self.props.get("userAgent")}, timeout=5).text
        except Exception as ex:
            self.log.exception(ex)

        if htmlSource != -1:
            linkList = self.getFilteredLinks(htmlSource, domain)
            linkList = self.fixBrokenLinks(linkList, domain, link)

            storedDataInDB = ""
            try:
                storedDataInDB = self.dbHandler.executeQuery(query.findLinkFromLinksByCategoryAndDomainAndDate %
                                                             (self.yearMonth, category, domain,
                                                              str(present.strftime('%Y-%m-%d'))))
            except:
                self.dbHandler.executeQuery(query.createTableIfNotExists % self.yearMonth)
                self.dbHandler.executeQuery(query.addPrimaryKeyToTable % ("links_" + self.yearMonth))
                self.dbHandler.executeQuery(query.addAutoIncrementToTable % ("links_" + self.yearMonth))

            for link in storedDataInDB:
                linkList.append(link[0])

            linkList = list(set(linkList))

            returnLinkDict = {}
            countDatabase = 0
            countHtmlSource = 0
            self.log.info("Total number of links to get: %d", len(linkList))
            self.log.info("Browsing links...")
            for link in linkList:
                try:
                    linkDate = self.dbHandler.executeQuery(query.findDateFromLinkCacheByLink % link)
                except:
                    self.dbHandler.executeQuery(query.createTableIfNotExistsForLinkCache)
                    self.dbHandler.executeQuery(query.addPrimaryKeyToTable % "link_cache")
                    self.dbHandler.executeQuery(query.addAutoIncrementToTable % "link_cache")
                    linkDate = self.dbHandler.executeQuery(query.findDateFromLinkCacheByLink % link)

                if linkDate:
                    if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
                        continue

                try:
                    linkData = self.dbHandler.executeQuery(query.findFromImgLinkByLink % (self.yearMonth, link))
                except Exception as ex:
                    self.log.warning("getNewsLinkFromSource: %s", ex)
                    continue

                if linkData:
                    if str(linkData[0][0]) == str(present.strftime('%Y-%m-%d')):
                        countDatabase += 1
                        linkData = linkData[0]
                        returnLinkDict[link] = (linkData[1], linkData[2], linkData[3])
                        continue
                else:
                    countHtmlSource += 1

                    getLinkHandler = LinkHandler(link, self.props, self.sources)
                    getLinkHandler.run()
                    if getLinkHandler.getParsedHtml() == -1:
                        self.dbHandler.executeQuery(query.insertTempLink % link)
                        continue

                    self.dbHandler.executeQuery(query.insertTempLink % link)

                    publishDate = getLinkHandler.getPublishDate()
                    year = str(present.strftime('%Y'))
                    month = str(present.strftime('%m'))
                    day = str(present.strftime('%d'))

                    if year in str(publishDate) and month in str(publishDate) and day in str(publishDate):
                        self.dbHandler.executeQuery(query.updateTempLink % link)
                        returnLinkDict[link] = (
                            getLinkHandler.getTitle(), getLinkHandler.getDescription(), getLinkHandler.getImage()
                        )

            returnLinkList = list(set(returnLinkDict))

            self.log.info("Link info location (Database / Source) - ( %d / %d)", countDatabase, countHtmlSource)
            self.log.info("Filtered links : %d", len(returnLinkList))

            linkCountDict = {}
            for src in returnLinkList:
                title = returnLinkDict[src][0]
                description = returnLinkDict[src][1]
                image = returnLinkDict[src][2]
                linkCountDict[src] = (category, domain, title, description, image)

        return linkCountDict

    def insertToDatabase(self, newsLinkDict):
        insertedCount = 0
        existsCount = 0
        for link in newsLinkDict:
            try:
                info = newsLinkDict[link]
                category = info[0]
                domain = info[1]
                title = info[2]
                description = info[3]
                image = info[4]

                if self.dbHandler.executeQuery(query.countFromLinksByLink % (self.yearMonth, link))[0][0] == 0:
                    self.dbHandler.executeQuery(
                        query.insertLink % (self.yearMonth, category, domain, link, title, description, image))
                    insertedCount += 1
                else:
                    existsCount += 1

            except Exception as ex:
                self.log.exception(ex)

        self.log.info("DB (new/exists) -> %d / %d", insertedCount, existsCount)

    def getFilteredLinks(self, htmlSource, domain):
        linkList = []
        soup = BeautifulSoup(htmlSource, 'html.parser')
        for category in self.sources:
            for source in self.sources.get(category):
                if domain == source.get("domain"):
                    sourceProps = source

        def isAllowed():
            for word in sourceProps["filterForLink"].get("permissibleWords"):
                if word in href:
                    return True
            return False

        def isForbidden():
            for word in sourceProps["filterForLink"].get("impermissibleWords"):
                if word in href:
                    return True
            return False

        for link in soup.findAll('a'):
            try:
                href = link.attrs['href']
            except KeyError:
                continue

            if isAllowed() and not isForbidden():
                linkList.append(href)

        return linkList

    def fixBrokenLinks(self, linkList, domain, link):
        for index, href in enumerate(linkList):
            if domain not in href and "." not in href:
                linkList[index] = link + href

        return linkList

    def closeProcess(self, arg1, signal):
        self.dbHandler.closeConnection()
        sys.exit(1)


if __name__ == '__main__':
    parser = Parser()
    signal.signal(signal.SIGINT, parser.closeProcess)
