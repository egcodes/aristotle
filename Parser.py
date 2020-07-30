import random
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
                self.dbHandler.executeQuery("TRUNCATE `tempLinks`")

            self.log.info("Starting [%s]" % str(present)[:19])

            newsLinkDict = {}

            for category in self.sources:
                sources = self.sources.get(category)

                for source in sources:
                    startSource = datetime.now()
                    if initSource and source.get("domain") != initSource:
                        continue

                    link = source.get("link")
                    permissibleWords = source.get("permissibleWords")
                    impermissibleWords = source.get("impermissibleWords")

                    self.log.info("Domain: %s", link)

                    try:
                        newsLinkDict.update(
                            self.getNewsLinkFromSource(present, category, source.get("domain"), link, permissibleWords,
                                                       impermissibleWords)
                        )
                        return
                    except Exception as ex:
                        self.log.exception(ex)

                    self.log.info("Time: %s", str(datetime.now() - startSource)[:7])
                    self.insertToDatabase(category, newsLinkDict, 5)
                    newsLinkDict.clear()

            self.log.info(str(datetime.now()) + ": Finished [%s]\n" % str(datetime.now() - present)[:19])
        except:
            self.log.warning("run")

    def getNewsLinkFromSource(self, present, category, domain, link, permissibleWords, impermissibleWords):
        class BreakIt(Exception):
            pass

        try:
            htmlSource = requests.get(link, headers={'User-Agent': self.props.get("userAgent")}, timeout=5).text
        except Exception as ex:
            self.log.exception(ex)

        if htmlSource != -1:
            linkList = self.getFilteredLinks(htmlSource, domain)
            linkList = self.fixBrokenLinks(linkList, domain, link)

            storedDataInDB = ""
            try:
                storedDataInDB = self.dbHandler.executeQuery(query.findLinkFromLinksByCategoryAndSourceAndDate %
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
            self.log.info("Total Link Count: %d", len(linkList))
            for link in linkList:
                try:
                    linkDate = self.dbHandler.executeQuery(query.findDateFromTempLinksByLink % link)
                except:
                    self.dbHandler.executeQuery(query.createTableIfNotExistsForTempLinks)
                    self.dbHandler.executeQuery(query.addPrimaryKeyToTable % "tempLinks")
                    self.dbHandler.executeQuery(query.addAutoIncrementToTable % "tempLinks")
                    linkDate = self.dbHandler.executeQuery(query.findDateFromTempLinksByLink % link)

                if linkDate:
                    if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
                        continue

                try:
                    linkData = self.dbHandler.executeQuery(query.findFromImgLinkByLink % (self.yearMonth, link))
                except:
                    self.log.warning("getNewsLinkFromSource")
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
                    soup = getLinkHandler.soup
                    if soup == -1:
                        self.dbHandler.executeQuery(query.insertTempLink % link)
                        continue

                    self.dbHandler.executeQuery(query.insertTempLink % link)

                    publishDate = getLinkHandler.publishDate
                    if "dateToday" in str(publishDate):
                        self.dbHandler.executeQuery(query.updateTempLink % link)
                        returnLinkDict[link] = (
                            getLinkHandler.title, getLinkHandler.description, getLinkHandler.imageLink)

            returnLinkList = list(set(returnLinkDict))

            self.log.info("Locate for link info (Database / Source) - ( %d / %d)", countDatabase, countHtmlSource)
            self.log.info("Eliminated links : %d", len(returnLinkList))

            linkCountDict = {}
            for src in returnLinkList:
                linkTitle = returnLinkDict[src][0]
                linkDesc = returnLinkDict[src][1]
                linkImage = returnLinkDict[src][2]
                linkCountDict[link] = (0, 0, 0, 0, category, domain, linkTitle, linkDesc, linkImage)

            choiceList = {}
            for i in range(0, len(linkCountDict)):
                try:
                    maxCountLink = random.choice(list(linkCountDict))
                    choiceList[maxCountLink] = linkCountDict[maxCountLink]
                    del linkCountDict[maxCountLink]
                except:
                    self.log.warning('getNewsLinkFromSource', "Hic sayfa gelmedi: %s" % link)
                    break

        return choiceList

    def isAscii(self, s):
        return all(ord(c) < 128 for c in s)

    def insertToDatabase(self, category, newsLinkDict, limit):
        insertedCount = 0
        existsCount = 0
        newsResult = ""
        try:
            index = 1
            for i in newsLinkDict:
                try:
                    maxCountLink = i

                    linkTitle = newsLinkDict[maxCountLink][6]
                    linkDesc = newsLinkDict[maxCountLink][7]
                    linkImage = newsLinkDict[maxCountLink][8]

                    # Description limit
                    try:
                        chIndex = 350
                        if len(linkDesc) >= 351:
                            count = 10
                            while count:
                                try:
                                    if self.isAscii(linkDesc[chIndex]):
                                        linkDesc = linkDesc[:chIndex] + '...'
                                        break
                                    count -= 1
                                    chIndex += 1
                                except:
                                    count -= 1
                                    chIndex = 340
                                    continue
                    except:
                        self.log.warning("generateHtmlFormat: %s" % maxCountLink)

                    imageId = linkImage[linkImage.rfind('/') + 1:]
                    if not (imageId and linkTitle):
                        continue

                    maxCountLinkInj = maxCountLink.replace("'", "''")

                    linkTitle = linkTitle.replace("'", "''")
                    linkTitle = linkTitle.replace("\\", "")
                    linkDesc = linkDesc.replace("'", "''")
                    linkDesc = linkDesc.replace("\\", "")
                    linkImage = linkImage.replace("'", "''")

                    if \
                            self.dbHandler.executeQuery(
                                query.countFromLinksByLink % (self.yearMonth, maxCountLinkInj))[0][
                                0] == 0:
                        self.dbHandler.executeQuery(query.insertLink %
                                                        (
                                                            self.yearMonth, newsLinkDict[maxCountLink][4],
                                                            newsLinkDict[maxCountLink][5],
                                                            maxCountLinkInj, newsLinkDict[maxCountLink][0],
                                                            newsLinkDict[maxCountLink][2],
                                                            newsLinkDict[maxCountLink][3], linkTitle, linkDesc,
                                                            linkImage
                                                        )
                                                        )
                        insertedCount += 1
                        index += 1
                    else:
                        existsCount += 1

                except:
                    index -= 1
                    self.log.warning("insertToDatabase", "Link html format hatasi: %s")

            self.log.info("DB (new/exists) -> %d / %d", insertedCount, existsCount)

            return str(newsResult)
        except Exception as ex:
            self.log.exception(ex)

    def getFilteredLinks(self, htmlSource, domain, label=None):
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
            if domain not in href:
                linkList[index] = link + domain

        return linkList

    def closeProcess(self, arg1, signal):
        self.dbHandler.closeConnection()
        sys.exit(1)


if __name__ == '__main__':
    parser = Parser()
    signal.signal(signal.SIGINT, parser.closeProcess)
