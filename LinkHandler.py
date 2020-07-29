#! -*- coding:utf-8 -*-
import yaml
from bs4 import BeautifulSoup
from LogHandler import LogHandler
import requests


class LinkHandler:
    def __init__(self, link, props, sources, timeout=3):
        self.logHandler = LogHandler("LinkHandler")

        self.link = link
        self.props = props
        self.sources = sources
        self.timeout = timeout

        self.htmlSource = ""
        self.soup = ""

        self.title = ""
        self.description = ""
        self.imageLink = ""
        self.publishDate = ""

    def run(self):
        try:
            try:
                r = requests.get(self.link, headers={'User-Agent': self.props.get("userAgent")}, timeout=self.timeout)
                r.encoding = 'utf-8'
                self.htmlSource = r.text
            except Exception as error:
                print("\t\t\t LinkHandler: %s: %s" % (error, self.link))
                self.soup = -1
                self.htmlSource = -1
                return

            self.soup = BeautifulSoup(self.htmlSource, 'html.parser')

            metas = self.soup.find_all('meta')
            for meta in metas:
                if 'name' in meta.attrs:
                    metaName = meta.attrs['name']
                    if metaName in self.props.get("descriptionKeys"):
                        self.setDescription(meta.attrs['content'])

                elif 'property' in meta.attrs:
                    metaProperty = meta.attrs['property']
                    if metaProperty in self.props.get("titleKeys"):
                        self.setTitle(meta.attrs['content'])
                    elif metaProperty in self.props.get("descriptionKeys"):
                        self.setDescription(meta.attrs['content'])
                    elif metaProperty in self.props.get("imageLinkKeys"):
                        self.setImageLink(meta.attrs['content'])
                    elif metaProperty in self.props.get("publishDateKeys"):
                        self.setPublishDate(meta.attrs['content'])

                elif 'itemprop' in meta.attrs:
                    metaItemprop = meta.attrs['itemprop']
                    if metaItemprop in self.props.get("publishDateKeys"):
                        self.setPublishDate(meta.attrs['content'])

                if self.isMetadataComplete():
                    break

            if not self.isMetadataComplete():
                for category in self.sources:
                    for source in self.sources.get(category):
                        if self.link.find(source.get("domain")) != -1:
                            dateContent = self.soup.findAll(source.get("dateElement"))
                            self.setPublishDate(dateContent)
                            break


        except Exception as ex:
            self.soup = -1
            self.htmlSource = -1
            self.logHandler.logger("run", self.link, ex)
            return

    def setTitle(self, title):
        if not self.title: self.title = title

    def setDescription(self, description):
        if not self.description: self.description = description

    def setImageLink(self, imageLink):
        if not self.imageLink: self.imageLink = imageLink

    def setPublishDate(self, publishDate):
        if not self.publishDate: self.publishDate = publishDate

    def isMetadataComplete(self):
        return self.title and self.description and self.imageLink and self.publishDate