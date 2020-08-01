from bs4 import BeautifulSoup
import requests
import logging

from settings import *
from util import *


class Parser:
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
            self.setFromMetadata()
            self.setFromProperties()
            self.fixStr()

        except Exception as ex:
            self.log.warning("%s, %s", ex, self.link)
            self.soup = -1
            self.htmlSource = -1

    def setFromMetadata(self):
        metas = self.soup.find_all('meta')
        for meta in metas:
            if 'name' in meta.attrs:
                metaName = meta.attrs['name']
                if metaName in "title":
                    self.setTitle(meta.attrs['content'])
                if metaName in ["description", "og:description"]:
                    self.setDescription(meta.attrs['content'])

            elif 'property' in meta.attrs:
                metaProperty = meta.attrs['property']
                if metaProperty in "og:title":
                    self.setTitle(meta.attrs['content'])
                elif metaProperty in "og:description":
                    self.setDescription(meta.attrs['content'])
                elif metaProperty in "og:image":
                    self.setImage(meta.attrs['content'])
                elif metaProperty in ["datePublished", "og:article:published_time"]:
                    self.setPublishDate(meta.attrs['content'])

            elif 'itemprop' in meta.attrs:
                metaItemprop = meta.attrs['itemprop']
                if metaItemprop in "datePublished":
                    self.setPublishDate(meta.attrs['content'])

            if self.isMetadataComplete():
                break

    def setFromProperties(self):
        if not self.isMetadataComplete():
            domainProps = getDomainProps(self.category, self.domain, "tagForMetadata")

            if not self.title:
                title = self.soup.find(domainProps["title"])
                self.setTitle(title)

            if not self.description:
                description = self.soup.find(domainProps["description"])
                self.setDescription(description)

            if not self.image:
                image = self.soup.find(domainProps["image"])
                self.setImage(image)

            if not self.publishDate:
                if domainProps["publishDate"]:
                    tags = domainProps["publishDate"].split(",")
                    if len(tags) == 3:
                        publishDate = self.soup.find(tags[0], {tags[1]: tags[2]})
                        if publishDate:
                            publishDate = publishDate.text
                    else:
                        publishDate = self.soup.find(tags[0])[tags[1]]
                    self.setPublishDate(publishDate)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        if not self.title:
            if title:
                self.title = title.strip()

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        if not self.description:
            if description:
                self.description = description.strip()

    def getImage(self):
        return self.image

    def setImage(self, image):
        if not self.image:
            self.image = image.strip()

    def getPublishDate(self):
        return self.publishDate

    def setPublishDate(self, publishDate):
        if not self.publishDate:
            if publishDate:
                self.publishDate = publishDate.strip()

    def getHtmlSource(self):
        return self.htmlSource

    def getParsedHtml(self):
        return self.soup

    def isMetadataComplete(self):
        return self.title and self.description and self.image and self.publishDate

    def fixStr(self):
        parserProps = getProps("parser")
        if self.title:
            self.title = self.title.replace("'", "''")
            self.title = trim_str(self.title, parserProps["titleCharLimit"])
        if self.description:
            self.description = self.description.replace("'", "''")
            self.description = trim_str(self.description, parserProps["descriptionCharLimit"])
