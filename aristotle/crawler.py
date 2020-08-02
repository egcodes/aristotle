import requests
import logging
from bs4 import BeautifulSoup

import meta_parser
import properties_parser
from settings import *
from util import *


class Crawler:
    def __init__(self, category, domain, link):
        self.log = logging.getLogger(__name__)

        self.category = category
        self.domain = domain
        self.link = link

        self.htmlSource = ""
        self.soup = ""

        self.title = ""
        self.description = ""
        self.image = ""
        self.publishDate = ""

    def run(self):
        try:
            requestProps = getProps("request")
            r = requests.get(self.link, headers={'User-Agent': requestProps["userAgent"]}, timeout=requestProps["timeout"])
            r.encoding = requestProps["encoding"]
            self.htmlSource = r.text

            self.soup = BeautifulSoup(self.htmlSource, 'html.parser')
            self.setFromProperties()
            self.setFromMetadata()
            self.fixStr()

        except Exception as ex:
            self.log.warning("%s, %s", ex, self.link)
            self.soup = -1
            self.htmlSource = -1

    def setFromProperties(self):
        domainProps = getDomainProps(self.category, self.domain, "tagForMetadata")
        if domainProps.get("title"):
            self.setTitle(properties_parser.getTitle(domainProps, self.soup))
        if domainProps.get("description"):
            self.setDescription(properties_parser.getDescription(domainProps, self.soup))
        if domainProps.get("image"):
            self.setImage(properties_parser.getImage(domainProps, self.soup))
        if domainProps.get("publishDate"):
            self.setPublishDate(properties_parser.getPublishDate(domainProps, self.soup))

    def setFromMetadata(self):
        metas = self.soup.find_all('meta')
        if not self.title:
            self.setTitle(meta_parser.getTitle(metas))
        if not self.description:
            self.setDescription(meta_parser.getDescription(metas))
        if not self.image:
            self.setImage(meta_parser.getImage(metas))
        if not self.publishDate:
            self.setPublishDate(meta_parser.getPublishDate(metas))

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image

    def getPublishDate(self):
        return self.publishDate

    def setPublishDate(self, publishDate):
        self.publishDate = publishDate

    def getHtmlSource(self):
        return self.htmlSource

    def getParsedHtml(self):
        return self.soup

    def fixStr(self):
        parserProps = getProps("parser")
        if self.title:
            self.title = self.title.replace("'", "''")
            self.title = self.title.strip()
            self.title = self.title.replace("\n", " ")
            if parserProps["titleCharLimit"]:
                self.title = trim_str(self.title, parserProps["titleCharLimit"])
        if self.description:
            self.description = self.description.replace("'", "''")
            self.description = self.description.strip()
            self.description = self.description.replace("\n", " ")
            if parserProps["descriptionCharLimit"]:
                self.description = trim_str(self.description, parserProps["descriptionCharLimit"])
        if self.image:
            self.image = self.image.replace("\n", " ")
            self.image = self.image.strip().replace("\n", " ")
        if self.publishDate:
            self.publishDate = self.publishDate.replace("\n", " ")
            self.publishDate = self.publishDate.strip()
