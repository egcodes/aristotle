from bs4 import BeautifulSoup
import requests
import logging

from aristotle.util import trim_str


class Parser:
    def __init__(self, link, props, sources):
        self.log = logging.getLogger(__name__)

        self.link = link
        self.props = props
        self.sources = sources

        self.htmlSource = ""
        self.soup = ""

        self.title = ""
        self.description = ""
        self.image = ""
        self.publishDate = ""

    def run(self):
        try:
            r = requests.get(self.link, headers={'User-Agent': self.props["request"]["userAgent"]},
                             timeout=self.props["request"]["timeout"])
            r.encoding = self.props["request"]["encoding"]
            self.htmlSource = r.text

            self.soup = BeautifulSoup(self.htmlSource, 'html.parser')
            self.setFromMetadata()
            self.setFromProperties()
            self.fixStr()

        except Exception as ex:
            self.log.warning("Parser: %s, %s", self.link, ex)
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
            for category in self.sources:
                for source in self.sources.get(category):
                    if self.link.find(source.get("domain")) != -1:
                        if not self.title:
                            title = self.soup.find(source["tagForMetadata"]["title"])
                            self.setTitle(title)

                        if not self.description:
                            description = self.soup.find(source["tagForMetadata"]["description"])
                            self.setDescription(description)

                        if not self.image:
                            image = self.soup.find(source["tagForMetadata"]["image"])
                            self.setImage(image)

                        if not self.publishDate:
                            tags = source["tagForMetadata"]["publishDate"].split(",")
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
        if self.title:
            self.title = self.title.replace("'", "''")
            self.title = trim_str(self.title, self.props["parser"]["titleCharLimit"])
        if self.description:
            self.description = self.description.replace("'", "''")
            self.description = trim_str(self.description, self.props["parser"]["descriptionCharLimit"])

