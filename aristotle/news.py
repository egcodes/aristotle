import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from aristotle import query
from aristotle.db import DB
from aristotle.parser import Parser


class News:
    def __init__(self, category, domain, props, sources):
        self.db = DB(props)
        self.category = category
        self.domain = domain
        self.props = props
        self.sources = sources
        self.yearMonth = ""
        self.log = logging.getLogger(__name__)

        self.run()

    def run(self):
        try:
            present = datetime.now()
            self.yearMonth = str(present.strftime('%Y%m'))

            if present.hour == 0:
                self.db.executeQuery(query.truncateCache)

            self.log.info("Begin [%s]" % str(present)[:19])

            newsLinkDict = {}

            for category in self.sources:
                sources = self.sources.get(category)

                for source in sources:
                    startSource = datetime.now()

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
                storedDataInDB = self.db.executeQuery(query.findLinkFromLinksByCategoryAndDomainAndDate %
                                                      (self.yearMonth, category, domain,
                                                       str(present.strftime('%Y-%m-%d'))))
            except:
                self.db.executeQuery(query.createTableIfNotExists % self.yearMonth)
                self.db.executeQuery(query.addPrimaryKeyToTable % ("links_" + self.yearMonth))
                self.db.executeQuery(query.addAutoIncrementToTable % ("links_" + self.yearMonth))

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
                    linkDate = self.db.executeQuery(query.findDateFromLinkCacheByLink % link)
                except:
                    self.db.executeQuery(query.createTableIfNotExistsForLinkCache)
                    self.db.executeQuery(query.addPrimaryKeyToTable % "link_cache")
                    self.db.executeQuery(query.addAutoIncrementToTable % "link_cache")
                    linkDate = self.db.executeQuery(query.findDateFromLinkCacheByLink % link)

                if linkDate:
                    if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
                        continue

                try:
                    linkData = self.db.executeQuery(query.findFromImgLinkByLink % (self.yearMonth, link))
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

                    getParser = Parser(link, self.props, self.sources)
                    getParser.run()
                    if getParser.getParsedHtml() == -1:
                        self.db.executeQuery(query.insertTempLink % link)
                        continue

                    self.db.executeQuery(query.insertTempLink % link)

                    publishDate = getParser.getPublishDate()
                    year = str(present.strftime('%Y'))
                    month = str(present.strftime('%m'))
                    day = str(present.strftime('%d'))

                    if year in str(publishDate) and month in str(publishDate) and day in str(publishDate):
                        self.db.executeQuery(query.updateTempLink % link)
                        returnLinkDict[link] = (
                            getParser.getTitle(), getParser.getDescription(), getParser.getImage()
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

                if self.db.executeQuery(query.countFromLinksByLink % (self.yearMonth, link))[0][0] == 0:
                    self.db.executeQuery(
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
