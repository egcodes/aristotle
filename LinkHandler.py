#! -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from LogHandler import LogHandler
import requests
import Properties as prop


class LinkHandler:
    def __init__(self, link, timeout=3):
        self.logHandler = LogHandler("LinkHandler")

        self.htmlSource = ""
        self.soup = ""
        self.title = ""
        self.description = ""
        self.imageLink = ""

        self.link = link
        self.timeout = timeout

    def run(self):
        try:
            try:
                self.htmlSource = requests.get(self.link, headers={'User-Agent': prop.userAgent}, timeout=self.timeout).text
            except Exception as error:
                print("\t\t\t LinkHandler: %s: %s" % (error, self.link))
                self.soup = -1
                self.htmlSource = -1
                return

            self.soup = BeautifulSoup(self.htmlSource, 'html.parser')

            self.title = self.getTitle(self.soup)
            self.description = self.getDescription(self.soup)
            self.imageLink = self.getImageLink(self.soup)

        except ValueError as error:
            if str(error).find('unichr() arg not in range(0x10000) (narrow Python build)') == -1:
                self.logHandler.logger("run", self.link)
            self.soup = -1
            self.htmlSource = -1
            return
        except TypeError as error:
            if str(error).find("cannot concatenate 'str' and 'NoneType' objects") == -1:
                self.logHandler.logger("run", self.link)
            self.soup = -1
            self.htmlSource = -1
            return
        except:
            self.soup = -1
            self.htmlSource = -1
            self.logHandler.logger("run", self.link)
            self.logHandler.logger("run")
            return

    def getTitle(self, soup):
        title = soup.findAll(attrs={"property": "og:title"})
        if not title:
            title = soup.findAll(attrs={"name": "title"})
        if not title:
            title = soup.findAll(attrs={"name": "twitter:title"})
        if not title:
            title = soup.findAll(attrs={"name": "Search.Title"})
        if not title:
            title = soup.findAll(attrs={"name": "Title"})
        if not title:
            title = soup.findAll(attrs={"name": "TITLE"})
        if not title:
            try:
                title = soup.html.head.title
            except:
                pass

        if title:
            if str(title)[0] == '<':
                title = title.text
            else:
                try:
                    title = title[0]['content']
                except:
                    try:
                        title = title[0]['value']
                    except:
                        pass
        return title

    def getDescription(self, soup):
        description = soup.findAll(attrs={"name": "description"})
        if not description:
            description = soup.findAll(attrs={"property": "og:description"})
        if not description:
            description = soup.findAll(attrs={"name": "twitter:description"})
        if not description:
            description = soup.findAll(attrs={"name": "Search.Description"})
        if not description:
            description = soup.findAll(attrs={"name": "Description"})
        if not description:
            description = soup.findAll(attrs={"name": "DESCRIPTION"})

        if description:
            try:
                description = description[0]['content']
            except Exception as error:
                try:
                    description = description[0]['value']
                except:
                    pass

        return description

    def getImageLink(self, soup):
        imageLink = ""
        if not imageLink:
            imageLink = soup.findAll(attrs={"property": "og:image"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"name": "image"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"name": "twitter:image"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"name": "Search.Image"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"name": "Image"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"name": "IMAGE"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"id": "NewsImagePath"})
        if not imageLink:
            imageLink = soup.findAll(attrs={"class": "yenihaberresmi"})
        if not imageLink:
            imageLink = soup.find("link", {"rel": "image_src"})

        if imageLink:
            try:
                imageLink = imageLink[0]['src']
            except:
                try:
                    imageLink = imageLink[0]['content']
                except:
                    try:
                        imageLink = imageLink[0]['value']
                    except:
                        try:
                            imageLink = imageLink[0]['href']
                        except:
                            try:
                                imageLink = dict(imageLink.attrs)['href']
                            except:
                                imageLink = str(imageLink)

            if imageLink.count('http://') > 1:
                imageLink = imageLink[imageLink[5:].find('http://') + 5:]
            if imageLink.find('https://') != -1:
                imageLink = imageLink.replace('https://', 'http://')
            if imageLink.startswith("//"):
                imageLink = "http://" + imageLink[2:]

            imageLink = imageLink.replace('////', '//')
            if imageLink.find('mc.yandex.ru/watch') == -1:
                imageLink = imageLink
            if imageLink.find('http://iatkn.tmgrup.com.tr') != -1:
                imageLink = imageLink.replace("http://", "https://")
            try:
                imageLink = "http:" + imageLink.split("http:")[2]
            except:
                pass

        return imageLink

# ===============================================================================
# test = LinkHandler("https://webrazzi.com//2013/08/26/web-uyelik-kapatma-justdeleteme/")
# test.run()
# ===============================================================================
