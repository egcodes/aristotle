import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from aristotle import query
from aristotle.db import DB
from aristotle.parser import Parser


class News:
    def __init__(self, props, sources, categories):
        self.db = DB(props)
        self.props = props
        self.sources = sources
        self.categories = categories
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
            news = {}
            for category in self.sources:
                if category not in self.categories:
                    continue

                sources = self.sources.get(category)
                for domain in sources:
                    if domain.get("active"):
                        self.log.info("Link: %s",  domain.get("link"))
                        news.update(self.getNewsLinkFromSource(present, category, domain.get("domain"),  domain.get("link")))
                        self.insertToDatabase(category, domain.get("domain"), news)
                        news.clear()

            self.log.info("End: " + "[" + str(datetime.now())[:19] + "]")

        except Exception as ex:
            self.log.warning("run: ", ex)

    def getNewsLinkFromSource(self, present, category, domain, link):
        def isLinkCached(checkLink):
            for cachedData in cachedLinks:
                if cachedData[0] == checkLink:
                    return True
            return False

        try:
            htmlSource = requests.get(link, headers={'User-Agent': self.props.get("userAgent")}, timeout=5).text
        except Exception as ex:
            self.log.exception(ex)

        for src in self.sources.get(category):
            if src.get("domain") == domain:
                sourceProps = src

        fetchedLinks = {}
        if htmlSource != -1:
            linkList = self.getFilteredLinks(htmlSource, category, domain)
            linkList = self.fixBrokenLinks(linkList, domain, link)

            linkList = list(set(linkList))
            self.log.info("Total links: %d", len(linkList))
            self.log.info("Browsing links...")

            try:
                cachedLinks = self.db.executeQuery(query.findCachedLinksByDomain % domain)
            except:
                self.createTables()
                cachedLinks = []

            for link in linkList:
                if isLinkCached(link):
                    continue

                getParser = Parser(link, self.props, self.sources)
                getParser.run()
                if getParser.getParsedHtml() == -1:
                    self.db.executeQuery(query.insertCacheLink % link)
                    continue

                self.db.executeQuery(query.insertCacheLink % (domain, link))

                publishDate = getParser.getPublishDate()
                presentDate = str(present.strftime(sourceProps["tagForMetadata"]["publishDateFormat"]))
                if presentDate in publishDate:
                    fetchedLinks[link] = (getParser.getTitle(), getParser.getDescription(), getParser.getImage())

            self.log.info("Filtered links: %d", len(fetchedLinks))

        return fetchedLinks

    def insertToDatabase(self, category, domain, newsLinkDict):
        insertedCount = 0

        for link in newsLinkDict:
            try:
                info = newsLinkDict[link]
                title = info[0]
                description = info[1]
                image = info[2]

                insertQuery = query.insertLink % (self.yearMonth, category, domain, link, title, description, image)
                insertedCount += 1
                try:
                    self.db.executeQuery(insertQuery)
                except Exception as ex:
                    self.log.warning("SQL Error: %s: %s", insertQuery, ex)

            except Exception as ex:
                self.log.exception(ex)

        self.log.info("Added links: %d", insertedCount)

    def getFilteredLinks(self, htmlSource, category, domain):
        linkList = []
        soup = BeautifulSoup(htmlSource, 'html.parser')
        for propCategory in self.sources:
            if category == propCategory:
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

    def createTables(self):
        self.db.executeQuery(query.createTableIfNotExistsForLinkCache)
        self.db.executeQuery(query.addPrimaryKeyToTable % "link_cache")
        self.db.executeQuery(query.addAutoIncrementToTable % "link_cache")
        self.db.executeQuery(query.createTableIfNotExists % self.yearMonth)
        self.db.executeQuery(query.addPrimaryKeyToTable % ("links_" + self.yearMonth))
        self.db.executeQuery(query.addAutoIncrementToTable % ("links_" + self.yearMonth))