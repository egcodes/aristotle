import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from aristotle import query
from aristotle.db import DB
from aristotle.parser import Parser
from aristotle.settings import *


class News:
    def __init__(self, categories):
        self.present = datetime.now()
        self.yearMonth = str(self.present.strftime('%Y%m'))

        self.db = DB(getProps("database"))
        self.createTablesIfNotExists()

        self.categories = categories
        self.log = logging.getLogger(__name__)

    def start(self):
        try:
            if self.present.hour == 0:
                self.db.executeQuery(query.truncateCache)

            self.log.info("Begin [%s]" % str(self.present)[:19])
            news = {}
            for category in sources:
                if category not in self.categories:
                    continue

                for domain in sources.get(category):
                    if domain.get("active"):
                        start = datetime.now()
                        self.log.info("Link: %s",  domain.get("link"))
                        news.update(self.fetchNews(category, domain.get("domain"),  domain.get("link")))
                        self.insertNews(category, domain.get("domain"), news)
                        news.clear()
                        self.log.info("Elapsed: %s" % str(datetime.now() - start)[:10])

            self.log.info("End: " + "[" + str(datetime.now())[:19] + "]")

        except Exception as ex:
            self.log.warning("run: ", ex)

    def fetchNews(self, category, domain, link):
        def isLinkCached(checkLink):
            for cachedData in cachedLinks:
                if cachedData[0] == checkLink:
                    return True
            return False

        try:
            htmlSource = requests.get(link, headers={'User-Agent': getProps("request", "userAgent")}, timeout=5).text
        except Exception as ex:
            self.log.exception(ex)
            return {}

        domainProps = getDomainProps(category, domain)
        fetchedLinks = {}
        if htmlSource != -1:
            linkList = self.getFilteredLinks(htmlSource, category, domain)
            linkList = self.fixBrokenLinks(linkList, domain, link)

            linkList = list(set(linkList))
            self.log.info("Total links: %d", len(linkList))
            self.log.info("Browsing links...")

            cachedLinks = self.db.executeQuery(query.findCachedLinksByDomain % domain)
            for link in linkList:
                if isLinkCached(link):
                    continue

                getParser = Parser(category, domain, link)
                getParser.run()
                if getParser.getParsedHtml() == -1:
                    self.db.executeQuery(query.insertCacheLink % (domain, link))
                    continue

                self.db.executeQuery(query.insertCacheLink % (domain, link))

                publishDate = getParser.getPublishDate()
                presentDate = str(self.present.strftime(domainProps["tagForMetadata"]["publishDateFormat"]))
                if presentDate in publishDate:
                    fetchedLinks[link] = (getParser.getTitle(), getParser.getDescription(), getParser.getImage())

            self.log.info("Filtered links: %d", len(fetchedLinks))

        return fetchedLinks

    def insertNews(self, category, domain, newsLinkDict):
        insertedCount = 0

        for link in newsLinkDict:
            try:
                info = newsLinkDict[link]
                title = info[0]
                description = info[1]
                image = info[2]

                insertQuery = query.insertLink % (self.yearMonth, category, domain, link, title, description, image, self.yearMonth, domain, link)
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
        filterLinkProps = getDomainProps(category, domain, "filterForLink")

        def isContainMandatoryKeywords():
            if filterLinkProps["mandatoryWords"]:
                for word in filterLinkProps["mandatoryWords"]:
                    if word not in href:
                        return False
            return True

        def isAllowed():
            if filterLinkProps["permissibleWords"]:
                for word in filterLinkProps["permissibleWords"]:
                    if word in href:
                        return True
                return False
            return True

        def isForbidden():
            if filterLinkProps["impermissibleWords"]:
                for word in filterLinkProps["impermissibleWords"]:
                    if word in href:
                        return True
            return False

        for link in soup.findAll('a'):
            try:
                href = link.attrs['href']
            except KeyError:
                continue

            if isContainMandatoryKeywords() and isAllowed() and not isForbidden():
                linkList.append(href)

        return linkList

    def fixBrokenLinks(self, linkList, domain, link):
        for index, href in enumerate(linkList):
            if domain not in href and ":" not in href:
                linkList[index] = link + href

        return linkList

    def createTablesIfNotExists(self):
        try:
            self.db.executeQuery(query.checkTableIsExists % ("links_" + self.yearMonth))
        except:
            self.db.executeQuery(query.createTableIfNotExists % self.yearMonth)
            self.db.executeQuery(query.addPrimaryKeyToTable % ("links_" + self.yearMonth))
            self.db.executeQuery(query.addAutoIncrementToTable % ("links_" + self.yearMonth))
        try:
            self.db.executeQuery(query.checkTableIsExists % "link_cache" )
        except:
            self.db.executeQuery(query.createTableIfNotExistsForLinkCache)
            self.db.executeQuery(query.addPrimaryKeyToTable % "link_cache")
            self.db.executeQuery(query.addAutoIncrementToTable % "link_cache")