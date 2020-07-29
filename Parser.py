# -*- coding: utf-8 -*-

import random
import signal
import sys
from datetime import datetime

from LinkHandler import LinkHandler
from LogHandler import LogHandler
from DbHandler import DbHandler
import Queries as query

from bs4 import BeautifulSoup
import requests
import yaml


class Main:
    def __init__(self):
        with open(r'config/sources.yaml') as file:
            self.sources = yaml.load(file, Loader=yaml.FullLoader)

        with open(r'config/properties.yaml') as file:
            self.props = yaml.load(file, Loader=yaml.FullLoader)

        self.logHandler = LogHandler("Parser")
        self.serverHandler = DbHandler(self.props)

        self.yearMonth = ""

        if len(sys.argv) == 2:
            category = sys.argv[1]
            self.run(category)
        elif len(sys.argv) == 3:
            category = sys.argv[1]
            source = sys.argv[2]
            self.run(category, source)
        else:
            self.run()

    def run(self, category="", source=""):
        try:
            initCategory = ""
            initSource = ""
            if category:
                initCategory = category
                initSource = source
                print(initCategory, initSource)

            present = datetime.now()
            self.yearMonth = str(present.strftime('%Y%m'))

            if present.hour == 0:
                self.serverHandler.executeQuery("TRUNCATE `tempLinks`")

            self.logHandler.printMsg("Starting [%s]" % str(present)[:19])

            gundemTotalSource = 0
            otherCategoryTotalSource = 0
            for domainCategory in self.sources:
                if domainCategory == "gundem":
                    gundemTotalSource = len(self.sources.get(domainCategory))
                else:
                    otherCategoryTotalSource += len(self.sources.get(domainCategory))

            if category == "gundem":
                domainCount = gundemTotalSource
            else:
                domainCount = otherCategoryTotalSource

            count = 1
            newsLinkDict = {}

            for category in self.sources:
                sources = self.sources.get(category)

                if present.hour < 18 and present.hour % 2 != 0 and category == "koseyazilari":
                    continue

                if initCategory:
                    if initCategory.split('-')[0] != 'non' and initCategory != category:
                        continue

                    if initCategory.split('-')[0] == 'non' and initCategory.split('-')[1] == category:
                        continue

                for source in sources:
                    startSource = datetime.now()
                    if initSource and source.get("domain") != initSource:
                        continue

                    link = source.get("link")
                    whiteWords = source.get("whiteWords")
                    blackWords = source.get("blackWords")

                    self.logHandler.printMsg("Source: (%d / %d) %s" % (count, domainCount, link), 1)

                    try:
                        newsLinkDict.update(
                            self.getNewsLinkFromSource(present, category, source.get("domain"), link, whiteWords, blackWords)
                       )
                        return
                    except Exception as ex:
                        if str(ex).find("NoneType") == -1:
                            self.logHandler.logger("run: %s:%s" % (link, ex))
                    count += 1

                    self.logHandler.printMsg("Time: %s" % (str(datetime.now() - startSource)[:7]), 1)
                    self.insertToDatabase(category, newsLinkDict, 5)
                    newsLinkDict.clear()

            self.logHandler.printMsg(str(datetime.now()) + ": Finished [%s]\n" % str(datetime.now() - present)[:19])
        except:
            self.logHandler.logger("run")

    def getNewsLinkFromSource(self, present, category, domain, link, whiteWords, blackWords):
        class BreakIt(Exception):
            pass

        try:
            htmlSource = requests.get(link, headers={'User-Agent': self.props.get("userAgent")}, timeout=5).text
        except:
            try:
                htmlSource = requests.get(link, headers={'User-Agent': self.props.get("userAgent")}, timeout=5).text
            except Exception as error:
                self.logHandler.printMsg(error)

        if htmlSource != -1:
            linkList = self.getLinks(htmlSource)
            linkList = self.fixLinks(linkList)

            storedDataInDB = ""
            try:
                storedDataInDB = self.serverHandler.executeQuery(query.findLinkFromLinksByCategoryAndSourceAndDate %
                                                            (self.yearMonth, category, domain,
                                                             str(present.strftime('%Y-%m-%d'))))
            except:
                self.serverHandler.executeQuery(query.createTableIfNotExists % self.yearMonth)
                self.serverHandler.executeQuery(query.addPrimaryKeyToTable % ("links_" + self.yearMonth))
                self.serverHandler.executeQuery(query.addAutoIncrementToTable % ("links_" + self.yearMonth))

            for link in storedDataInDB:
                linkList.append(link[0])

            # Duplicate linkleri temizle
            linkList = list(set(linkList))

            # Kaynaktaki tum alinan linklere bakilir
            returnLinkDict = {}
            countDatabase = 0
            countHtmlSource = 0
            self.logHandler.printMsg("Total Link Count: %d" % len(linkList), 2)
            for link in linkList:
                link = self.fixUrl(link, domain, whiteWords, blackWords)
                if not link:
                    continue

                # ===========================================================================================
                # Eger link temp tabloda var ise tarihine bakilir bugun ise alinir yoksa gecilir sonraki linke
                # ===========================================================================================
                try:
                    linkDate = self.serverHandler.executeQuery(query.findDateFromTempLinksByLink % link)
                except:
                    self.serverHandler.executeQuery(query.createTableIfNotExistsForTempLinks)
                    self.serverHandler.executeQuery(query.addPrimaryKeyToTable % "tempLinks")
                    self.serverHandler.executeQuery(query.addAutoIncrementToTable % "tempLinks")
                    linkDate = self.serverHandler.executeQuery(query.findDateFromTempLinksByLink % link)

                if linkDate:
                    if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
                        continue

                try:
                    linkData = self.serverHandler.executeQuery(query.findFromImgLinkByLink % (self.yearMonth, link))
                except:
                    self.logHandler.logger("getNewsLinkFromSource")
                    continue

                if linkData:
                    # Link tarihi database'de olan bugun ise database'den bilgileri al
                    if str(linkData[0][0]) == str(present.strftime('%Y-%m-%d')):
                        countDatabase += 1
                        linkData = linkData[0]
                        returnLinkDict[link] = (linkData[1], linkData[2], linkData[3])
                        continue
                else:
                    countHtmlSource += 1

                    getLinkHandler = LinkHandler(link, self.props, self.sources)
                    getLinkHandler.run()
                    soup = getLinkHandler.soup
                    if soup == -1:
                        self.serverHandler.executeQuery(query.insertTempLink % link)
                        continue

                    self.serverHandler.executeQuery(query.insertTempLink % link)

                    publishDate = getLinkHandler.publishDate
                    if str(publishDate).find("dateToday") != -1:
                        self.serverHandler.executeQuery(query.updateTempLink % link)
                        returnLinkDict[link] = (getLinkHandler.title, getLinkHandler.description, getLinkHandler.imageLink)

            # Duplicate linkleri temizle
            returnLinkList = list(set(returnLinkDict))

            self.logHandler.printMsg("Locate for link info (Database / Source) - ( %d / %d)" % (countDatabase, countHtmlSource), 2)
            self.logHandler.printMsg("Eliminated links : %d" % len(returnLinkList), 2)

            linkCountDict = {}
            for src in returnLinkList:
                linkTitle = returnLinkDict[src][0]
                linkDesc = returnLinkDict[src][1]
                linkImage = returnLinkDict[src][2]
                linkCountDict[link] = (0, 0, 0, 0, category, domain, linkTitle, linkDesc, linkImage)

            choiceList = {}
            for i in range(0, len(linkCountDict)):
                try:
                    maxCountLink = random.choice(list(linkCountDict))
                    choiceList[maxCountLink] = linkCountDict[maxCountLink]
                    del linkCountDict[maxCountLink]
                except:
                    self.logHandler.logger('getNewsLinkFromSource', "Hic sayfa gelmedi: %s" % link)
                    break

        return choiceList

    def isAscii(self, s):
        return all(ord(c) < 128 for c in s)

    def insertToDatabase(self, category, newsLinkDict, limit):
        """
			Verilen link listesindeki haber linklerini table icin uygun formatta geri dondurur
		"""

        insertedCount = 0
        existsCount = 0
        newsResult = ""
        try:
            index = 1
            for i in newsLinkDict:
                try:
                    maxCountLink = i

                    linkTitle = newsLinkDict[maxCountLink][6]
                    linkDesc = newsLinkDict[maxCountLink][7]
                    linkImage = newsLinkDict[maxCountLink][8]

                    # Description limit
                    try:
                        chIndex = 350
                        if len(linkDesc) >= 351:
                            count = 10
                            while count:
                                try:
                                    if self.isAscii(linkDesc[chIndex]):
                                        linkDesc = linkDesc[:chIndex] + '...'
                                        break
                                    count -= 1
                                    chIndex += 1
                                except:
                                    count -= 1
                                    chIndex = 340
                                    continue
                    except:
                        self.logHandler.logger("generateHtmlFormat: %s" % maxCountLink)

                    imageId = linkImage[linkImage.rfind('/') + 1:]
                    if not (imageId and linkTitle):
                        continue

                    maxCountLinkInj = maxCountLink.replace("'", "''")

                    # Linkler database kaydediliyor
                    # Var ise update yapiliyor
                    linkTitle = linkTitle.replace("'", "''")
                    linkTitle = linkTitle.replace("\\", "")
                    linkDesc = linkDesc.replace("'", "''")
                    linkDesc = linkDesc.replace("\\", "")
                    linkImage = linkImage.replace("'", "''")

                    if self.serverHandler.executeQuery(query.countFromLinksByLink % (self.yearMonth, maxCountLinkInj))[0][0] == 0:
                        self.serverHandler.executeQuery(query.insertLink %
                            (
                                self.yearMonth, newsLinkDict[maxCountLink][4], newsLinkDict[maxCountLink][5],
                                maxCountLinkInj, newsLinkDict[maxCountLink][0], newsLinkDict[maxCountLink][2],
                                newsLinkDict[maxCountLink][3], linkTitle, linkDesc, linkImage
                            )
                        )
                        insertedCount += 1
                        index += 1
                    else:
                        existsCount += 1

                except:
                    index -= 1
                    self.logHandler.logger("insertToDatabase", "Link html format hatasi: %s")

            self.logHandler.printMsg("DB (new/exists) -> %d / %d" % (insertedCount, existsCount), 1)
            self.logHandler.printMsg("---------------------", 1)

            return str(newsResult)
        except:
            self.logHandler.logger("insertToDatabase")

    def getLinks(self, htmlSource):
        linkList = []
        soup = BeautifulSoup(htmlSource, 'html.parser')
        for link in soup.findAll('a'):
            href = link.get('href')
            try:
                if len(href) > 8:
                    flagGet = True
                    for keyword in self.props.get("blackListWordsForLinks"):
                        if href.find(keyword) != -1:
                            flagGet = False
                            break
                    if flagGet:
                        linkList.append(href)
            except:
                pass
        return linkList

    def fixUrl(self, link, domain, whiteWords, blackWords):
        if link.find(domain) == -1:
            link = "https://" + domain + link

        if blackWords:
            flag = False
            for word in blackWords:
                if link.find(word) != -1:
                    flag = True
                    break
            if flag:
                return

        if whiteWords:
            flag = True
            for word in whiteWords:
                if link.find(word) != -1:
                    flag = False
                    break
            if flag:
                return

        link = link.replace("'", "''")

        return link

    def fixLinks(self, linkList):
        newLinkList = []
        for link in linkList:
            newLink = link.strip()

            if newLink[5:].find('#') != -1:
                newLink = newLink[:newLink.find('#')]
            if newLink[5:].find(';') != -1:
                newLink = newLink[:newLink.find(';')]

            newLinkList.append(newLink)
        return newLinkList

    def closeProcess(self, arg1, signal):
        self.serverHandler.closeConnection()
        sys.exit(1)


if __name__ == '__main__':
    main = Main()
    signal.signal(signal.SIGINT, main.closeProcess)
