import logging
import requests
from datetime import datetime

from sqlalchemy import literal, exists

from connection import Database
from crawler import Crawler
from link_parser import *
from query import *
from settings import *
from util import *


class News:
    def __init__(self, categories):
        self.present = datetime.now()
        self.yearMonth = str(self.present.strftime('%Y%m'))

        self.db = Database()
        self.createTablesIfNotExists()
        self.link_cache_table = self.db.getMeta("link_cache")
        self.links_table = self.db.getMeta("links_%s" % self.yearMonth)

        self.categories = categories
        self.log = logging.getLogger(__name__)

    def start(self):
        try:
            if self.present.hour == 0:
                self.db.getConnection().execute(truncateCache)

            start = datetime.now()
            self.log.info("Begin [%s]" % str(start)[:19])
            news = {}
            for category in sources:
                if category not in self.categories:
                    continue

                for domain in sources.get(category):
                    if domain.get("active"):
                        self.log.info("MainPage: %s", domain.get("link"))
                        news.update(self.fetchNews(category, domain.get("domain"), domain.get("link")))
                        self.insertNews(category, domain.get("domain"), news)
                        news.clear()

            self.log.info("End: [%s] [%s]", str(datetime.now())[:19], str(datetime.now() - start)[:10])

        except Exception as ex:
            self.log.warning("run: ", ex)

        self.db.closeDB()

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

            query = self.db.getDB() \
                .select([self.link_cache_table.columns.link]) \
                .where(self.link_cache_table.columns.domain == domain)
            cachedLinks = self.db.getConnection().execute(query).fetchall()

            for link in linkList:
                if isLinkCached(link):
                    self.log.debug("Cached link: %s", link)
                    continue

                crawler = Crawler(category, domain, link)
                crawler.run()

                query = self.db.getDB().insert(self.link_cache_table).values(id=None, domain=domain, link=link)
                self.db.getConnection().execute(query)

                if crawler.getParsedHtml() == -1:
                    self.log.debug("Link cannot be parsed: %s", link)
                    continue

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
        existsCount = 0

        for link in newsLinkDict:
            try:
                info = newsLinkDict[link]
                title = info[0]
                description = info[1]
                image = info[2]

                currentDate = datetime.now()
                query = self.db.getDB() \
                    .select([literal(currentDate), literal(category),
                             literal(domain), literal(link), literal(title), literal(description),
                             literal(image), literal("0"), literal(currentDate)]) \
                    .where(~exists([self.links_table.c.link]).where(self.links_table.c.link == link))

                self.log.debug("Links stored: %s", link)
                try:
                    ins = self.links_table.insert().from_select(["date", "category", "domain", "link", "title",
                                                                 "description", "image", "clicked", "timestamp"], query)
                    result = self.db.getConnection().execute(ins)
                    if result.rowcount == 1:
                        insertedCount += 1
                    else:
                        existsCount += 1
                except Exception as ex:
                    self.log.warning("SQL Error: %s: %s", query, ex)

            except Exception as ex:
                self.log.exception(ex)

        self.log.info("Links stored/exists: %d/%d", insertedCount, existsCount)

    def createTablesIfNotExists(self):
        if not self.db.getEngine().dialect.has_table(self.db.getEngine(), "links_" + self.yearMonth):
            self.db.getConnection().execute(createTableIfNotExists % self.yearMonth)
            self.db.getConnection().execute(addPrimaryKeyToTable % ("links_" + self.yearMonth))
            self.db.getConnection().execute(addAutoIncrementToTable % ("links_" + self.yearMonth))

        if not self.db.getEngine().dialect.has_table(self.db.getEngine(), "link_cache"):
            self.db.getConnection().execute(createTableIfNotExistsForLinkCache)
            self.db.getConnection().execute(addPrimaryKeyToTable % "link_cache")
            self.db.getConnection().execute(addAutoIncrementToTable % "link_cache")
