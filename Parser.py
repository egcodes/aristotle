# -*- coding: utf-8 -*-

import random
import signal
import sys
import time
from datetime import datetime

from LinkHandler import LinkHandler
from LogHandler import LogHandler
from ServerDatabaseHandler import ServerDatabaseHandler
from SourceList import createNewsSource
import Properties as prop
import Queries as query

from bs4 import BeautifulSoup
import requests


class Main:
    def __init__(self):
        self.logHandler = LogHandler("Parser")
        self.serverHandler = ServerDatabaseHandler()

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

            # tempLinks truncate
            if present.hour == 0:
                self.serverHandler.executeQuery("TRUNCATE `tempLinks`")

            self.logHandler.printMsg("Starting [%s]" % str(present)[:19])

            # ===========================================================
            # Kaynaklar olusturuluyor
            # ===========================================================
            self.newsSources = createNewsSource(present)

            # ===========================================================================
            # Source sayimi icin count olusturuluyor sadece print'e lazim
            # ===========================================================================
            totalSource = 0
            gundemTotalSource = 0
            otherCategoryTotalSource = 0
            for sourceCategory, sources in self.newsSources.items():
                for sourceList in sources:
                    if sourceCategory == "gundem":
                        gundemTotalSource += 1
                    else:
                        otherCategoryTotalSource += 1
            if category == "gundem":
                totalSource = gundemTotalSource
            else:
                totalSource = otherCategoryTotalSource

            # ===========================================================
            # Her bir kategor ve her onun her bir source'i icin tek tek islem yapiliyor
            # ===========================================================
            count = 1
            newsLinkDict = {}

            for data in self.newsSources.items():
                category = data[0]
                sources = data[1]

                random.shuffle(sources)

                # Kose yazilari 18'den once ve 2 saaate bir kontrol edilsin
                if present.hour < 18 and present.hour % 2 != 0 and category == "koseyazilari":
                    continue

                if initCategory:
                    if initCategory.split('-')[0] != 'non' and initCategory != category:
                        continue

                    if initCategory.split('-')[0] == 'non' and initCategory.split('-')[1] == category:
                        continue

                for sourceList in sources:
                    startSource = datetime.now()
                    source = sourceList[0]
                    if initSource and source != initSource:
                        continue

                    newsSourceLink = sourceList[1]
                    newsSourceDiffWords = ()
                    newsSourceBlackWords = ()
                    if len(sourceList) > 2:
                        newsSourceDiffWords = sourceList[2]
                    if len(sourceList) > 3:
                        newsSourceBlackWords = sourceList[3]

                    self.logHandler.printMsg("Source: (%d / %d) %s" % (count, totalSource, newsSourceLink), 1)

                    try:
                        newsLinkDict.update(
                            self.getNewsLinkFromSource(present, category, source, newsSourceLink, newsSourceDiffWords,
                                                       newsSourceBlackWords)
                        )
                    except Exception as ex:
                        if str(ex).find("NoneType") == -1:
                            self.logHandler.logger("run: %s:%s" % (newsSourceLink, ex))
                    count += 1

                    self.logHandler.printMsg("Time: %s" % (str(datetime.now() - startSource)[:7]), 1)
                    self.insertToDatabase(category, newsLinkDict, 5)
                    newsLinkDict.clear()

            self.logHandler.printMsg(str(datetime.now()) + ": Finished [%s]\n" % str(datetime.now() - present)[:19])
        except:
            self.logHandler.logger("run")

    def getNewsLinkFromSource(self, present, category, sourceTitle, newsSourceLink, newsSourceDiffWords,
                              newsSourceBlackWords):
        """
			Verilen link icin kategoriye uygun haber linklerini cikarip en cok paylasim sayisina 
			ve bugunun tarine sahip olanlari liste olarak geri doner
		"""

        class BreakIt(Exception):
            pass

        try:
            htmlSource = requests.get(newsSourceLink, headers={'User-Agent': prop.userAgent}, timeout=5).text
        except:
            time.sleep(10)
            try:
                htmlSource = requests.get(newsSourceLink, headers={'User-Agent': prop.userAgent}, timeout=5).text
            except Exception as error:
                return []

        if htmlSource != -1:
            linkList = self.getLinks(htmlSource)
            linkList = self.fixLinks(linkList)

            storedDataInDB = ""
            try:
                storedDataInDB = self.serverHandler.executeQuery(query.findLinkFromLinksByCategoryAndSourceAndDate %
                                                            (self.yearMonth, category, sourceTitle,
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
                linkData = []

                # Ana source link duzenleme
                sourceLink = newsSourceLink
                if newsSourceLink.find("http://") != -1 and newsSourceLink[len('http://'):].find('/') != -1:
                    sourceLink = sourceLink[:sourceLink[len('http://'):].find('/') + len('http://')]
                else:
                    if newsSourceLink[len('https://'):].find('/') != -1:
                        sourceLink = sourceLink[:sourceLink[len('https://'):].find('/') + len('https://')]

                # Eger link icinde sourceTitle yok ise ve alttaki keyword'lardan biri var ise alakasi bir link gec
                if link.find(sourceTitle) == -1 and (
                        link.find('http://') != -1 or link.find('www.') != -1 or link.find('https://') != -1):
                    continue
                if link.count('http://') > 1 or (
                        link.count('http://') > 0 and link.count('https://') > 0) or link.count('www.') > 1:
                    continue

                # Eger link'de hostname yok ise ekle, link'i duzenle
                if link.find(sourceTitle) == -1:
                    if link[0] == '/':
                        link = sourceLink + link
                    else:
                        link = sourceLink + '/' + link
                else:
                    if link[0] != 'w' and link[0] != 'h':
                        link = 'http://' + link[2:]

                # Black word'ler varsa linkde gec
                if newsSourceBlackWords:
                    flag = False
                    for word in newsSourceBlackWords:
                        if link.find(word) != -1:
                            flag = True
                            break
                    if flag:
                        continue

                # Linkleri ayiraca gore ayikla, uygun olmayanlari alma
                if newsSourceDiffWords:
                    flag = True
                    for word in newsSourceDiffWords:
                        if link.find(word) != -1:
                            flag = False
                            break
                    if flag:
                        continue

                # Injection onleme
                linkInj = link.replace("'", "''")

                # ===========================================================================================
                # Eger link temp tabloda var ise tarihine bakilir bugun ise alinir yoksa gecilir sonraki linke
                # ===========================================================================================
                try:
                    linkDate = self.serverHandler.executeQuery(query.findDateFromTempLinksByLink % linkInj)
                except:
                    self.serverHandler.executeQuery(query.createTableIfNotExistsForTempLinks)
                    self.serverHandler.executeQuery(query.addPrimaryKeyToTable % "tempLinks")
                    self.serverHandler.executeQuery(query.addAutoIncrementToTable % "tempLinks")
                    linkDate = self.serverHandler.executeQuery(query.findDateFromTempLinksByLink % linkInj)

                if linkDate:
                    if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
                        continue

                try:
                    linkData = self.serverHandler.executeQuery(query.findFromImgLinkByLink % (self.yearMonth, linkInj))
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

                    getLinkHandler = LinkHandler(link)
                    getLinkHandler.run()
                    soup = getLinkHandler.soup
                    if soup == -1:
                        self.serverHandler.executeQuery(query.insertTempLink % linkInj)
                        continue

                    self.serverHandler.executeQuery(query.insertTempLink % linkInj)

                    try:
                        for categories in list(self.newsSources):
                            for source in categories:
                                if source[1] == newsSourceLink:
                                    title = getLinkHandler.title
                                    desc = getLinkHandler.description
                                    img = getLinkHandler.imageLink

                                    flagW = False
                                    for keyword in prop.blackListWords:
                                        if title.lower().find(keyword) != -1:
                                            flagW = True
                                            break
                                        if desc.lower().find(keyword) != -1:
                                            flagW = True
                                            break
                                    if flagW:
                                        continue

                                    if len(desc) < 5:
                                        desc = title

                                    try:
                                        if len(source) > 5:
                                            seperator = list(source[5])[0]
                                            seperatorCount = list(source[5])[0]
                                            if title.count(seperator) >= seperatorCount:
                                                for i in range(seperatorCount):
                                                    if title.rfind(seperator) > 20:
                                                        title = title[:title.rfind(seperator)].strip()
                                    except:
                                        self.logHandler.logger("getNewsLinkFromSource", "Title replace")

                                    try:
                                        if len(source) > 6:
                                            seperator = source[6]
                                            desc = desc.split(seperator)[0]
                                    except:
                                        self.logHandler.logger("getNewsLinkFromSource", "Desc replace")

                                    # link'de 2013/09/09 sekli icin, 0 ise direk al
                                    if source[4] == 0:
                                        returnLinkDict[link] = (title, desc, img)
                                    elif source[4] == 1:
                                        todayFormat = source[2][0]
                                        if link.find(todayFormat) != -1:
                                            returnLinkDict[link] = (title, desc, img)
                                    elif source[4] == 2:
                                        todayFormat = source[2][0]
                                        monthDay = todayFormat[4:]
                                        if link.find(monthDay) != -1:
                                            returnLinkDict[link] = (title, desc, img)
                                    else:
                                        for dateFormats in source[4]:
                                            dateKeyword = dateFormats
                                            dateClass = list(dateKeyword)[0]
                                            dateToday = list(dateKeyword)[0]

                                            soupDateDiv = soup.findAll("div", {"class": "%s" % dateClass})

                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("meta", {"itemprop": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("meta", {"property": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("div", {"id": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("span", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("span", {"style": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("time", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("div", {"style": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("span", {"id": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("p", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("div", {"itemprop": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("span", {"itemprop": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("li", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("p", {"itemprop": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("a", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("h1", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("time", {"itemprop": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("time", {"datetime": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll("i", {"class": "%s" % dateClass})
                                            if not soupDateDiv:
                                                soupDateDiv = soup.findAll(dateClass)

                                            # Tarihin string olarak aliniyor
                                            findedDate = ""
                                            for item in soupDateDiv:
                                                findedDate = str(item.text)
                                                if not findedDate:
                                                    try:
                                                        findedDate = item['value']
                                                    except:
                                                        pass
                                                if not findedDate:
                                                    try:
                                                        findedDate = item['content']
                                                    except:
                                                        pass

                                                # direk zaman yerine 1 saat once seklinde ise burada ayristirilir
                                                if findedDate.find('önce') != -1 and findedDate.find("gün") == -1:
                                                    try:
                                                        findedDate = soupDateDiv[0]["title"]
                                                    except:
                                                        pass

                                                    for i in soupDateDiv:
                                                        try:
                                                            if i.getText("title").find("saat") != -1:
                                                                findedDate = str(present.strftime('%d.%m.%Y'))
                                                                break
                                                        except:
                                                            findedDate = ""

                                                # Bir tane keyword bulundu ama istenen degil tarih olup olmadigi kontrol edilir
                                                if len(findedDate) == 0:
                                                    continue

                                                findedDate = findedDate.replace('s&#x0131;', 'ı')
                                                findedDate = findedDate.replace('&#x131;', 'ı')
                                                if findedDate.find(str(datetime.now().year)) == -1:
                                                    continue
                                                else:
                                                    break

                                            if not findedDate:
                                                continue

                                            try:
                                                dateText = findedDate
                                                # Html ü karakteri
                                                dateText = dateText.replace('&#x00FC;', 'ü')
                                                dateText = dateText.replace('&amp;#305;', 'ı')
                                                dateText = dateText.replace('&#252;', 'ü')
                                                dateText = dateText.replace('&amp;#350;', 'Ş')

                                                # ===============================
                                                # Bazi tarihlerde guncelleme var onu almasin diye
                                                # ===============================
                                                if dateText[10:].find("Güncelleme") != -1:
                                                    firstIndex = dateText.find("Güncelleme")
                                                    endIndex = firstIndex + len('Güncelleme') + 10
                                                    dateText = dateText[:firstIndex] + dateText[endIndex:]

                                                if dateText.find(dateToday) != -1:
                                                    # Eger linkDate yoksa ekle
                                                    self.serverHandler.executeQuery(
                                                        "UPDATE `tempLinks` SET date=CURRENT_DATE() WHERE link='%s'" % linkInj)

                                                    returnLinkDict[link] = (title, desc, img)

                                                break
                                            except AttributeError as error:
                                                print(error)
                                                continue
                                    raise BreakIt
                    except BreakIt:
                        continue

            # Duplicate linkleri temizle
            returnLinkList = list(set(returnLinkDict))
            self.logHandler.printMsg("Locate for link info (Database / Source) - ( %d / %d)" % (countDatabase, countHtmlSource), 2)
            self.logHandler.printMsg("Eliminated links : %d" % len(returnLinkList), 2)

            linkCountDict = self.getSocialCount(category, sourceTitle, returnLinkList, returnLinkDict)

            choiceList = {}
            for i in range(0, len(linkCountDict)):
                try:
                    maxCountLink = random.choice(list(linkCountDict))
                    choiceList[maxCountLink] = linkCountDict[maxCountLink]
                    del linkCountDict[maxCountLink]
                except:
                    self.logHandler.logger('getNewsLinkFromSource', "Hic sayfa gelmedi: %s" % newsSourceLink)
                    break

        return choiceList

    def getSocialCount(self, category, sourceTitle, returnLinkList, returnLinkDict):
        linkCountDict = {}

        for link in returnLinkList:
            linkTitle = returnLinkDict[link][0]
            linkDesc = returnLinkDict[link][1]
            linkImage = returnLinkDict[link][2]
            countTwitter = 0
            countGoogle = 0
            countFacebook = 0

            linkCountDict[link] = (
                countTwitter + countFacebook + countGoogle, countTwitter, countFacebook, countGoogle, category,
                sourceTitle,
                linkTitle, linkDesc, linkImage
            )

            # LinkDatabase'de var ise count'lari update et
            # self.serverHandler.executeQuery(
            #    "UPDATE `links_%s` SET tweetCount=%d, facebookCount=%d, googleCount=%d  WHERE `link`='%s'" % (
            #        self.yearMonth, countTwitter, countFacebook, countGoogle, link))

        return linkCountDict

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
                    for keyword in prop.blackListWordsForLinks:
                        if href.find(keyword) != -1:
                            flagGet = False
                            break
                    if flagGet:
                        linkList.append(href)
            except:
                pass
        return linkList

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
