import logging
import requests
from datetime import datetime

from db import DB
from crawler import Crawler
from link_parser import *
from query import *
from settings import *
from util import *


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
                self.db.executeQuery(truncateCache)

            start = datetime.now()
            self.log.info("Begin [%s]" % str(start)[:19])
            news = {}
            for category in sources:
                if category not in self.categories:
                    continue

                for domain in sources.get(category):
                    if domain.get("active"):
                        self.log.info("MainPage: %s",  domain.get("link"))
                        news.update(self.fetchNews(category, domain.get("domain"),  domain.get("link")))
                        self.insertNews(category, domain.get("domain"), news)
                        news.clear()

            self.log.info("End: [%s] [%s]", str(datetime.now())[:19], str(datetime.now() - start)[:10])

        except Exception as ex:
            self.log.warning("run: ", ex)

    def fetchNews(self, category, domain, link):
        def isLinkCached(checkLink):
            for cachedData in cachedLinks:
                if cachedData[0] == checkLink:
                    return True
            return False

        attempts = 1
        while True:
            try:
                htmlSource = requests.get(link, headers={'User-Agent': getProps("request", "userAgent")},
                                          timeout=getProps("request")["timeout"]).text
                break
            except Exception as ex:
                attempts += 1
                self.log.warning("Request: %s", ex)
                if attempts > 3:
                    return {}

        domainProps = getDomainProps(category, domain)
        fetchedLinks = {}
        if htmlSource != -1:
            linkCount, linkList = get_filtered_links(htmlSource, category, domain)
            self.log.info("Links count (page): %d", linkCount)
            linkList = fix_broken_links(linkList, domain, link)
            self.log.info("Links count (filtered): %d", len(linkList))
            linkList = list(set(linkList))
            self.log.info("Links count (unduplicate): %d", len(linkList))
            self.log.info("Browsing links...")

            cachedLinks = self.db.executeQuery(findCachedLinksByDomain % domain)
            for link in linkList:
                if isLinkCached(link):
                    self.log.debug("Cached link: %s", link)
                    continue

                crawler = Crawler(category, domain, link)
                crawler.run()
                if crawler.getParsedHtml() == -1:
                    self.db.executeQuery(insertCacheLink % (domain, link))
                    self.log.debug("Link cannot be parsed: %s", link)
                    continue

                self.db.executeQuery(insertCacheLink % (domain, link))

                publishDate = crawler.getPublishDate()
                presentDate = non_zero_date(self.present.strftime(domainProps["tagForMetadata"]["publishDateFormat"]))
                if publishDate and presentDate in publishDate:
                    fetchedLinks[link] = (crawler.getTitle(), crawler.getDescription(), crawler.getImage())
                    self.log.debug("News published today: %s", link)
                else:
                    if not publishDate:
                        self.log.debug("No publishing date: %s", link)
                    else:
                        self.log.debug("News not published today: %s <-> %s, %s", publishDate, presentDate, link)

            self.log.info("Links count (to be stored): %d", len(fetchedLinks))

        return fetchedLinks

    def insertNews(self, category, domain, newsLinkDict):
        insertedCount = 0

        for link in newsLinkDict:
            try:
                info = newsLinkDict[link]
                title = info[0]
                description = info[1]
                image = info[2]

                insertQuery = insertLink % (self.yearMonth, category, domain, link, title, description, image, self.yearMonth, domain, link)
                insertedCount += 1
                self.log.debug("Links stored: %s", link)
                try:
                    self.db.executeQuery(insertQuery)
                except Exception as ex:
                    self.log.warning("SQL Error: %s: %s", insertQuery, ex)

            except Exception as ex:
                self.log.exception(ex)

        self.log.info("Stored links: %d", insertedCount)

    def createTablesIfNotExists(self):
        try:
            self.db.executeQuery(checkTableIsExists % ("links_" + self.yearMonth))
        except:
            self.db.executeQuery(createTableIfNotExists % self.yearMonth)
            self.db.executeQuery(addPrimaryKeyToTable % ("links_" + self.yearMonth))
            self.db.executeQuery(addAutoIncrementToTable % ("links_" + self.yearMonth))
        try:
            self.db.executeQuery(checkTableIsExists % "link_cache" )
        except:
            self.db.executeQuery(createTableIfNotExistsForLinkCache)
            self.db.executeQuery(addPrimaryKeyToTable % "link_cache")
            self.db.executeQuery(addAutoIncrementToTable % "link_cache")