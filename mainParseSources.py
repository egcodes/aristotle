# -*- coding: utf-8 -*-

import sys, os, ast, random
import urllib, urllib2, requests, json
import time
import simplejson
import signal
from sourceList import createNewsSourceByPresent
from datetime import datetime
from LinkHandler import LinkHandler
from LogHandler import LogHandler
from ServerDatabaseHandler import ServerDatabaseHandler
if os.name == "posix":
	from BeautifulSoup import BeautifulSoup
else:
	from bs4 import BeautifulSoup

import requests, urllib

class Main:
	def __init__(self):
		
		#=======================================================================
		# Configuration values
		#=======================================================================
		self.wwwPath = '/var/www/html/'
		#Resimler icin
		self.linkImagePath = self.wwwPath + 'imageslink/'
		# Url request'lerinde kullanilan agent
		self.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
		# Alinan ve islenen linkleri goster
		self.showLink = False
		#links database tablosu icin son ek
		self.yearMonth = ""
		#Turkce karakter
		self.turkishDict = {'ı': 'i', 'ü': 'u', 'ö':'o', 'ş':'s', 'ç':'c', 'ğ':'g'}
			
		#=======================================================================
		# Configuration For Requests
		#=======================================================================
		#Bazi sitelerin haber resimleri icin class ile alinir
		#birden fazla class girilebilir value kismina , karakteri ile bitisik yaz
		self.imageClassForSources = {
									'http://www.aksam.com.tr':'image', 
									'http://www.trthaber.com':'image', 
									'http://www.trthaber.com/haber/kultur-sanat/':'image',
									'http://amkspor.sozcu.com.tr':'in_image',
									'http://www.sosyalmedya.co':'attachment-large wp-post-image', 
									'http://www.teknolojioku.com':'newsImage', 
									'http://www.webrazzi.com': 'post-content',
									'http://www.taraf.com.tr/yazarlar/':'info',
									'http://www.donanimhaber.com':'entry',
									'http://www.gazetevatan.com/yazarlar/':'aimg',
									'http://www.cumhuriyet.com.tr/yazarlar':'author',
									'http://www.sabah.com.tr/Yazarlar':'iBox',
									'http://www.ensonhaber.com':'mansetresmi',
									'http://www.yenisafak.com.tr/yazarlar/':'picture',
									'http://www.haberler.com':'image',
									'http://www.internethaber.com':'item img active',
									'http://haber.sol.org.tr':'singlenews-image',
									'http://www.yeniakit.com.tr/yazarlar':'au-top-right',
									'http://www.takvim.com.tr':'haberImg',
									'http://www.haberturk.com':'image',
									'http://www.haber7.com':'image_src',
									'http://www.mynet.com':'twitter:image',
									}
		#Farkli meta etiketi icin tanim
		self.descMetaTypes = {
								'http://www.mynet.com/teknoloji':{"property":"og:description"}, 
								'http://www.mynet.com':{"property":"og:description"}, 
								'http://webtv.hurriyet.com.tr':{"property":"og:description"}, 
								'http://www.haber7.com':{"name":"twitter:description"},
							}

		#Desc'i alma title'i ata
		self.notGetDesc = []

		#Link'lerdeki ? karakteri icin
		self.containQuestionCharacter = [
										'http://www.posta.com.tr', 
										'http://www.odatv.com',
										]

		#Link sonundaki / karakteri silinmeyecek
		self.notDeletedBackslashCharacter = [
										'http://www.posta.com.tr', 
										'http://www.odatv.com',
										'http://www.taraf.com.tr',
										'http://www.taraf.com.tr/yazarlar/',
										'http://www.samanyoluhaber.com',
										'http://amkspor.sozcu.com.tr',
										'http://www.haberler.com',
										'http://www.diken.com.tr',
										'http://www.fizikist.com',
										]
		#Haberden alinan resim cok kucuk ise yada yanlis ise title baz alinarak google'dan resim cekilir
		#Google image limit'leri oldugundan surekli cekince yasaklandi
		self.getGoogleImageList = []

		#Link'in image link'inin icinde alindiktan sonra replace edilmesi gerek bir sey var ise
		self.replaceStringForLink = {
									'shiftdelete.net': ('/shiftdelete.net', '/s01.shiftdelete.net/img/general_b'), 
									}

		#Asagiya girilen keyword'lar link icinde geciyor ise o link alinmaz
		self.notGetLinkIfContainThisKeyword = ['javascript:', ]

		#Hotlink korumasi olanlar bunlarin resimleri link vermek yerine indiriliyor
		self.hotlinks = []
		
		#Eger karakterler bozuk geliyor ise farkli bir Request tpye deneniyor bu kaynaklar icin
		self.requestTypes = ['amkspor.sozcu.com.tr', 'yenisafak.com.tr']

		#Eger source'u encoding geliyor ise baska bir request yapilir
		self.encodePageSource = ['mynet.com', 'trthaber.com']

		#degeri 0 ise www eklenir , 1 ise www silinir, 2 ise http://www silinir
		self.getTweetCountFix = {'yenisafak.com.tr':0, 'bigumigu.com':1, 'webrazzi.com':2, 'odatv.com':2}
		
		#Eger title, desc karakterler bozuk geliyor temizlik icin
		self.contentTitleDescReplace = ['shiftdelete.net']
		
		#Gormek istemedigin linkleri gec #imageLink'i icinde bulunanlar sadece
		self.blackListLinkImage ={
								}
		

		#=======================================================================
		# Class import
		self.logHandler = LogHandler("Main")

		# Database baglantisi
		self.serverHandler = ServerDatabaseHandler()
		
		self.getLinkCountLimit = 2000

		if len(sys.argv) == 2:
			category = sys.argv[1]
			self.run(category)
		elif len(sys.argv) == 3:
			category = sys.argv[1]
			source = sys.argv[2]
			self.run(category, source)
		else:
			self.run()

	
	def getGoogleImage(self, searchTerm):
		searchTerm = self.multipleReplace(searchTerm, self.turkishDict)
		searchTerm = '%20'.join(searchTerm.split()[:4])
		
		# Set count to 0
		count= 0
		
		imageUrl = ""
		# Notice that the start changes for each iteration in order to request a new set of images for each loop
		try:
			url = 'https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm
			request = urllib2.Request(url, None, {'User-Agent' : self.userAgent})
			response = urllib2.urlopen(request, timeout=10)
			# Get results using JSON
			results = simplejson.load(response)
			data = results['responseData']
			dataInfo = data['results']
			
			# Iterate for each result and get unescaped url
			for myUrl in dataInfo:
				count = count + 1
				if int(myUrl['width']) >= 300 and int(myUrl['height']) >= 300:
					imageUrl =  myUrl['unescapedUrl']
				else:
					imageUrl = ""
				if imageUrl:
					break
		except:
			imageUrl = ""
			
		return imageUrl
			
	def multipleReplace(self, text, wordDict):
		for key in wordDict:
			text = text.replace(key, wordDict[key])
		return text
		
	def downloadImage(self, source, link, path):
		#Bu kaynaklar icin bot olmadigimizi anlatmak icin donen link'e istek yollanir
		if source == 'cumhuriyet.com.tr':
			try:
				ln = 'http://www.cumhuriyet.com.tr'
				req = urllib2.Request(ln, headers={'User-Agent' : self.userAgent})
				html = urllib2.urlopen(req, timeout=5).read()
				if len(html) < 250:
					firstIndex = html.find('url=')
					endIndex = html[firstIndex:].find('"') + firstIndex
					
					url = html[firstIndex + len('url='): endIndex]
					if url and url.find('http') != -1:
						req = urllib2.Request(url, headers={'User-Agent' : self.userAgent})
						html = urllib2.urlopen(req, timeout=5).read()
						print url
			except:
				self.logHandler.logger("run")

		#Bu kaynaklar icin bot olmadigimizi anlatmak icin donen link'e istek yollanir
		elif source == 'odatv.com':
			try:
				ln = 'http://www.odatv.com'
				req = urllib2.Request(ln, headers={'User-Agent' : self.userAgent})
				html = urllib2.urlopen(req, timeout=5).read()
				if len(html) < 300:
					firstIndex = html.find('url=')
					endIndex = html[firstIndex:].find('"') + firstIndex
					
					url = html[firstIndex + len('url='): endIndex]
					if url and url.find('http') != -1:
						req = urllib2.Request(url, headers={'User-Agent' : self.userAgent})
						html = urllib2.urlopen(req, timeout=5).read()
						print url
			except:
				self.logHandler.logger("run")
		
					
		req = urllib2.Request(link, headers={'User-Agent' : self.userAgent})
		try:
			imageId = "default.png"
			if source == 'cumhuriyet.com.tr':
				imageId = link[link[:link.rfind('/')].rfind('/') + 1:].replace('/', '')
			else:
				imageId = link[link.rfind('/') + 1:]
			if imageId.find('?') != -1:
				imageId = imageId[:imageId.find('?')]
			elif imageId.find('#') != -1:
				imageId = imageId[:imageId.find('#')]
				
			if not os.path.exists(path + imageId):
				htmlSource = urllib2.urlopen(req, timeout=5).read()
				with open(path + imageId, "wb") as f:
					f.write(htmlSource)
			return imageId
		except Exception, error:
			print error, link
			return 0
	
	def getNewsLinkFromSource(self, present, category, sourceTitle, newsSourceLink, newsSourceDiffWords, newsSourceBlackWords):
		"""
			Verilen link icin kategoriye uygun haber linklerini cikarip en cok paylasim sayisina 
			ve bugunun tarine sahip olanlari liste olarak geri doner
		"""
		class BreakIt(Exception): pass
		
		#=======================================================================
		# Link source aliniyor
		#=======================================================================
		try:
			self.encodePageSource.index(sourceTitle)
			try:
				htmlSource = requests.get(newsSourceLink, headers={'User-Agent' : self.userAgent}, timeout=10).text
			except:
				time.sleep(15)
				try:
					htmlSource = requests.get(newsSourceLink, headers={'User-Agent' : self.userAgent}, timeout=10).text
				except Exception, error:
					return []
		except:
			req = urllib2.Request(newsSourceLink, headers={'User-Agent' : self.userAgent})
			try:
				htmlSource = urllib2.urlopen(req, timeout=10).read()
			except:
				time.sleep(15)
				try:
					htmlSource = urllib2.urlopen(req, timeout=10).read()
				except Exception, error:
					return []
				
		#=======================================================================
		# Source alindiysa link analiz islemi basliyor
		#=======================================================================
		if htmlSource != -1: 
			#===================================================================
			# #Verilen kaynak link'den (anasayfa) tum linkler aliniyor
			#===================================================================
			linkList = []
			soup = BeautifulSoup(htmlSource)
			for link in soup.findAll('a'):
				href = link.get('href')
				try:
					if len(href) > 8:
						flagGet = True
						for keyword in self.notGetLinkIfContainThisKeyword:
							if href.find(keyword) != -1:	
								flagGet = False
								break
						if flagGet:
							linkList.append(href)
				except:
					pass
			

			#===================================================================
			# #Linklerin argumanlari atilip sade hale getiriliyor
			#===================================================================
			newLinkList = []
			for link in linkList:
				newLink = link.strip()
				if len(newLink) > 3:
					
					if newLink[5:].find('#') != -1:
						newLink = newLink[:newLink.find('#')]
					if newLink[5:].find(';') != -1:
						newLink = newLink[:newLink.find(';')]
						
					#Linklerin icin haberi belirleyen ?'den sonraki kisim ise bu islem yapilmaz
					try:
						self.containQuestionCharacter.index(newsSourceLink)
					except:
						if newLink[5:].find('?') != -1:
							newLink = newLink[:newLink.find('?')]
						
					#Asagidaki siteler'de sondaki / karakteri silinmez
					try:	
						self.notDeletedBackslashCharacter.index(newsSourceLink)
					except:
						if newLink[-1] ==  '/':
							newLink = newLink[:-1]

					#Link listeye alinir
					newLinkList.append(newLink)
						
						
			
			#===================================================================
			# Anasayfada olmayan ama database'de bugun yayimlanan linkleri ekle
			#===================================================================
			firstData = ""
			try:
				firstData = self.serverHandler.executeQuery("SELECT link FROM `links_%s` WHERE category='%s' AND source='%s' AND date='%s'"%(self.yearMonth, category, sourceTitle, str(present.strftime('%Y-%m-%d'))))
			except:
				self.serverHandler.executeQuery("""CREATE TABLE IF NOT EXISTS `links_%s` (
`id` int(11) NOT NULL,
  `date` date NOT NULL,
  `category` varchar(32) NOT NULL,
  `source` varchar(255) NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `tweetCount` int(11) NOT NULL,
  `facebookCount` int(11) NOT NULL,
  `googleCount` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `imgLink` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `clickedCount` int(11) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"""%(self.yearMonth))
				time.sleep(3)
				self.serverHandler.executeQuery("ALTER TABLE `links_%s` ADD PRIMARY KEY (`id`)"%self.yearMonth)
				time.sleep(3)
				self.serverHandler.executeQuery("ALTER TABLE `links_%s` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT"%self.yearMonth)

			#Database'deki bu kaynaga ait diger
			#datalar aliniyor
			for link in firstData:
				newLinkList.append(link[0])

			#Anasayfa olmayan ama database'de source icin kayitli diger link'lerle ilgili bilgi
			#Duplicate linkleri temizle	
			tmp = set(newLinkList)
			linkList = list(tmp)

			#En fazla limit link'e bak
			if len(linkList) > self.getLinkCountLimit:
				linkList = linkList[:self.getLinkCountLimit]
							
			#============================================
			#Kaynaktaki tum alinan linklere bakilir
			#============================================
			returnLinkDict = {}
			countDatabase = 0
			countHtmlSource = 0
			notGetLinkFlag = False
			self.logHandler.printMsg("Total Link Count: %d"%len(linkList), 2)
			for link in linkList:
				linkData = []
				
				#Link var ise
				if not link:
					continue
				
				#Turkce karakter temizle
				for key in self.turkishDict:
					link = link.replace(key, self.turkishDict[key])
				
				#Ana source link duzenleme
				sourceLink = newsSourceLink
				if newsSourceLink[len('http://'):].find('/') != -1:
					sourceLink = sourceLink[:sourceLink[len('http://'):].find('/') + len('http://')]

				#Eger link icinde sourceTitle yok ise ve alttaki keyword'lardan biri var ise alakasi bir link gec
				#Exm: https://itunes.apple.com.tr					
				if link.find(sourceTitle) == -1 and (link.find('http://') != -1 or link.find('www.') != -1 or link.find('https://') != -1):
					continue
				if link.count('http://') > 1 or (link.count('http://') > 0 and link.count('https://') > 0) or link.count('www.') > 1:
					continue
				
				#Eger link'de hostname yok ise ekle, link'i duzenle
				if link.find(sourceTitle) == -1:
					if link[0] == '/':
						link = sourceLink + link
					else:
						link = sourceLink + '/' + link
				else:
					if link[0] != 'w' and link[0] != 'h':
						link = 'http://' + link[2:]
				
				#Domain yok ise linki alma baska sitenin linkidir
				if link.find(sourceTitle) == -1:
					continue
				
				#Black word'ler varsa linkde gec
				if newsSourceBlackWords:
					flag = False
					for word in newsSourceBlackWords:
						if link.find(word) != -1:
							flag = True
							break
					if flag:
						continue
				
				#Linkleri ayiraca gore ayikla, uygun olmayanlari alma
				if newsSourceDiffWords:
					flag = True
					for word in newsSourceDiffWords:
						if link.find(word) != -1:
							flag = False
							break
					if flag:
						continue
				
				if self.showLink:
					self.logHandler.printMsg(link, 3)
				

					
				#===============================================================
				# Link links_* database'de var ise tekrar LinkHandlerr cagrilmaz, eger ana sayfada ise meta etiketleri kontrol icin cagrilir
				#===============================================================
				# Injection onleme
				linkInj = link.replace("'", "''")

				try:
					linkData = self.serverHandler.executeQuery("SELECT date, title, description, imgLink FROM `links_%s` WHERE `link`='%s'"%(self.yearMonth, linkInj))
				except:
					self.logHandler.logger("getNewsLinkFromSource")
					continue
				
				if linkData:
					#Link tarihi database'de olan bugun ise database'den bilgileri al
					if str(linkData[0][0]) == str(present.strftime('%Y-%m-%d')):
						countDatabase += 1
						linkData = linkData[0]
						#Eger link ana sayfada ise meta tag'ler kontrol edilir
						linksAllMainPage = []
						linksAllMainPage.extend(list(self.serverHandler.executeQuery("SELECT imgLink, title, link, tweetCount, facebookCount, googleCount, category, description, source, id FROM `links_%s` WHERE `date`='%s' AND category = 'gundem' AND tweetCount+facebookCount+googleCount > 5 ORDER BY id DESC LIMIT 0, 12"%(self.yearMonth, present))))
						limitMozaikCount = 25 
						linksAllMainPage.extend(list(self.serverHandler.executeQuery("SELECT imgLink, title, link, tweetCount, facebookCount, googleCount, category, description, source FROM (SELECT imgLink, title, link, tweetCount, facebookCount, googleCount, category, description, source FROM (SELECT imgLink, title, link, `tweetCount`, `facebookCount`, `googleCount`, category, description, source FROM `links_%s` WHERE `date`='%s' AND category = '%s') AS `NEWTABLE` WHERE category='gundem' ORDER BY `tweetCount`+`facebookCount`+`googleCount` DESC LIMIT 0, %d) AS NEWTABLE"%(self.yearMonth, present, category, limitMozaikCount))))
						limitCategoryCount = 8
						linksAllMainPage.extend(list(self.serverHandler.executeQuery("SELECT imgLink, title, link, tweetCount, facebookCount, googleCount, category, description, source FROM (SELECT imgLink, title, link, tweetCount, facebookCount, googleCount, category, description, source FROM (SELECT imgLink, title, link, `tweetCount`, `facebookCount`, `googleCount`, category, description, source FROM `links_%s` WHERE `date`='%s' AND category = '%s') AS `NEWTABLE` ORDER BY `tweetCount`+`facebookCount`+`googleCount` DESC LIMIT 0, %d) AS NEWTABLE"%(self.yearMonth, present, category, limitCategoryCount))))
						for data in linksAllMainPage:
							lnMainPage = data[2]
							if lnMainPage != link:
								returnLinkDict[link] = (linkData[1], linkData[2], linkData[3])
								continue

				#===========================================================================================
				#Eger link database'de var ise tarihine bakilir bugun ise alinir yoksa gecilir sonraki linke
				#===========================================================================================
				try:
					linkDate = self.serverHandler.executeQuery("SELECT date FROM `tempLinks` WHERE `link`='%s'" % linkInj)
				except:
					self.serverHandler.executeQuery("""
CREATE TABLE IF NOT EXISTS `tempLinks` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;""")

					time.sleep(3)
					self.serverHandler.executeQuery("ALTER TABLE `tempLinks` ADD PRIMARY KEY (`id`)")
					time.sleep(3)
					self.serverHandler.executeQuery("ALTER TABLE `tempLinks` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT")
					linkDate = self.serverHandler.executeQuery("SELECT date FROM `tempLinks` WHERE `link`='%s'" % linkInj)

					
				if linkDate:
					if str(linkDate[0][0]) != str(present.strftime('%Y-%m-%d')):
						continue

				#===========================================================
				# #Timeout olur diye 2 defa deneyecek
				#===========================================================
				count = 2
				countHtmlSource += 1
				flagContinue = False
				while count:
					getLinkHandler= ""
					
					#=======================================================
					# Link'ler icin ozel LinkHandlerr argumanlari
					#=======================================================
					imageClass = ""
					requestType = ""
					cleanBrokenCh = ""
					descMetaType = ""
					try:
						imageClass = self.imageClassForSources[newsSourceLink]
					except:
						pass
					try:
						self.requestTypes.index(sourceTitle)
						requestType = 1
					except:
						requestType = 0
					try:
						self.contentTitleDescReplace.index(sourceTitle)
						cleanBrokenCh = True
					except:
						cleanBrokenCh = False
					try:
						descMetaType = self.descMetaTypes[newsSourceLink]
					except:
						descMetaType = ""
						
					getLinkHandler = LinkHandler(link, requestType=requestType,  imageClass=imageClass, descMetaType=descMetaType, cleanBrokenCh=cleanBrokenCh)
					getLinkHandler.run()
					soup = getLinkHandler.soup

					#Source gelmez ise link'i gec
					if soup == -1:
						time.sleep(3)
						count -= 1
					else:
						break
					if count == 0:
						flagContinue = True
						break
				if flagContinue:
					continue
				
				#===========================================================
				# Bugunun tarihi arastiriliyor link htmlSource'unda
				# Varsa bugunun tarihi returnLinkList'e ekleniyor
				#===========================================================
				try:
					for categories in self.newsSources.values():
						for source in categories:
							if source[1] == newsSourceLink:
								# -'den oncenin alinmasi
								# Eger dashCount' kadari title'da var ise temizle
								title = getLinkHandler.titleContent
								desc = getLinkHandler.descContent
								img = getLinkHandler.imgContent
							

								#Tanim yok ise title atanir
								if len(desc) < 5:
									desc = title
								
								#Gormek istemedigin linkleri gec #imageLink'i icinde bulunanlar sadece
								for src, lnnk in self.blackListLinkImage.iteritems():
									if src == sourceTitle :
										for i in lnnk:
											if img.find(i) != -1:
												notGetLinkFlag = True
												break
								if notGetLinkFlag:
									notGetLinkFlag = False
									continue
								
								if title.find('&#039;') != -1:
									title = title.replace('&#039;', "'")
								if title.find('&quot;') != -1:
									title = title.replace('&quot;', '"')
								if desc.find('&#039;') != -1:
									desc = desc.replace('&#039;', "'")
								if desc.find('&quot;') != -1:
									desc = desc.replace('&quot;', "'")
								
								#Title silme islemleri
								try:
									if len(source) > 5:
										seperator = source[5].keys()[0]
										seperatorCount = source[5].values()[0]
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

								#link'de 2013/09/09 sekli icin, 0 ise direk al
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
										dateClass = dateKeyword.keys()[0]
										dateToday = dateKeyword.values()[0]
										
										
										if source[0] == "izlesene.com":
											soupDateDiv = soup.findAll("p", { "class" : "%s"%dateClass})
										else:
											soupDateDiv = soup.findAll("div", { "class" : "%s"%dateClass})
											
											if not soupDateDiv:
												soupDateDiv = soup.findAll("meta", { "itemprop" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("div", { "id" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("span", { "class" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("span", { "style" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("time", { "class" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("div", { "style" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("span", { "id" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("p", { "class" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("div", { "itemprop" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("span", { "itemprop" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("li", { "class" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("p", { "itemprop" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("a", { "class" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll("time", { "itemprop" : "%s"%dateClass})
											if not soupDateDiv:
												soupDateDiv = soup.findAll(dateClass)
										if self.showLink:
											print "\t",dateKeyword
											print "\t", soupDateDiv 
										
										#Tarihin string olarak aliniyor
										findedDate = ""
										for item in soupDateDiv:
											findedDate = str(item.text)
											if not findedDate:
												try:
													findedDate = item['value']
												except:
													pass
											if findedDate.find('önce') != -1:
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

											#Bir tane keyword bulundu ama istenen degil tarih olup olmadigi kontrol edilir
											if len(findedDate) == 0:
												continue

											findedDate = findedDate.replace('s&#x0131;', 'ı')
											if findedDate.find(str(datetime.now().year)) == -1:
												continue
											else:
												break

										if not findedDate:
											continue
										
										#Eger linkDate yoksa ekle 1 gun oncesi olarak 
										#Eger bugunun link'i ise asagida duzeltilir

										if not linkDate:
											self.serverHandler.executeQuery("INSERT INTO `tempLinks` VALUES(NULL, CURRENT_DATE()-1, '%s')"%linkInj)

										try:
											dateText = findedDate
											#Html ü karakteri
											dateText = dateText.replace('&#x00FC;', 'ü')
											dateText = dateText.replace('&amp;#305;', 'ı')
											dateText = dateText.replace('&#252;', 'ü')
											dateText = dateText.replace('&amp;#350;', 'Ş')

											#===============================
											# Bazi tarihlerde guncelleme var onu almasin diye
											#===============================
											if dateText[10:].find("Güncelleme") != -1:
												firstIndex = dateText.find("Güncelleme")
												endIndex = firstIndex + len('Güncelleme') + 10
												dateText = dateText[:firstIndex] + dateText[endIndex:]

											if dateText.find(dateToday) != -1:
												#Eger linkDate yoksa ekle
												self.serverHandler.executeQuery("UPDATE `tempLinks` SET date=CURRENT_DATE() WHERE link='%s'"%linkInj)
													
												returnLinkDict[link] = (title, desc, img)
											else:
												if self.showLink:
													print "Link bugunun degil: | %s | %s |"%(dateText, dateToday)
											break
										except AttributeError, error:
											print error
											continue
								raise BreakIt
				except BreakIt:
					continue
				
				
			#Duplicate linkleri temizle
			tmp = set(returnLinkDict)
			returnLinkList = list(tmp)

			#===================================================================
			# Twitter ve Facebook count'lari alinip gerekli tum seyler donduruluyor
			#===================================================================
			self.logHandler.printMsg("Link parse locate (Database / Source) - ( %d / %d)"%(countDatabase, countHtmlSource), 2)
			self.logHandler.printMsg("Got it links : %d"%len(returnLinkList), 2)
			
			linkCountDict = self.getSocialCount(category, sourceTitle, returnLinkList, returnLinkDict)
			
			choiceList = {}
			
			for i in range(0, len(linkCountDict)):
				try:
					#maxCountLink = max(linkCountDict, key=linkCountDict.get)
					maxCountLink = random.choice(linkCountDict.keys())
					choiceList[maxCountLink] = linkCountDict[maxCountLink]
					del linkCountDict[maxCountLink]
				except:
					self.logHandler.logger('getNewsLinkFromSource', "Hic sayfa gelmedi: %s"%newsSourceLink)
					break
					
		return choiceList
	
	
	def getSocialCount(self, category, sourceTitle, returnLinkList, returnLinkDict):
		linkCountDict = {}

		for link in returnLinkList:
			if self.showLink:
				self.logHandler.printMsg(link, 3)
				

			linkTitle = returnLinkDict[link][0]
			linkDesc = returnLinkDict[link][1]
			linkImage = returnLinkDict[link][2]
			countTwitter = 0
			countGoogle = 0	
			countFacebook = 0

			linkCountDict[link] = (countTwitter + countFacebook + countGoogle, countTwitter, countFacebook, countGoogle, category, sourceTitle, linkTitle, linkDesc, linkImage)
			#LinkDatabase'de var ise count'lari update et
			self.serverHandler.executeQuery("UPDATE `links_%s` SET tweetCount=%d, facebookCount=%d, googleCount=%d  WHERE `link`='%s'"%(self.yearMonth, countTwitter, countFacebook, countGoogle, link))
		
		return linkCountDict
	
	
	def isAscii(self, s):
		return all(ord(c) < 128 for c in s)

	def insertToDatabase(self, category, newsLinkDict, limit):
		"""
			Verilen link listesindeki haber linklerini table icin uygun formatta geri dondurur
		"""
		
		self.logHandler.printMsg("Insert To Database (%d)"%len(newsLinkDict.keys()), 1)
		self.logHandler.printMsg("---------------------", 1)
		

		newsResult = ""
		try:
			index = 1
			for i in newsLinkDict:
				if index > 3:
					break
				try:
					maxCountLink = random.choice(newsLinkDict.keys())
					
					linkTitle = newsLinkDict[maxCountLink][6]
					linkDesc = newsLinkDict[maxCountLink][7]
					linkImage = newsLinkDict[maxCountLink][8]

					#Eger kaynak icin getGoogleImage'de tanimli ise resim site yerine
					#Google'dan alinir, link database'de var ise tekrar aranmaz google api limit'i
					#asmamak icin
					for sourceHttp in self.getGoogleImageList:
						if maxCountLink.find(sourceHttp) != -1:
							try:
								self.serverHandler.executeQuery("SELECT imgLink FROM `links_%s` WHERE link='%s'"%(self.yearMonth, maxCountLink.replace("'", "''")))[0][0]
							except:
								imageName = self.multipleReplace(linkTitle, self.turkishDict)
								imageName = '%20'.join(linkTitle.split()[:4])
								imgLinkGoogle  = self.getGoogleImage(linkTitle)
								if imgLinkGoogle:
									linkImage = imgLinkGoogle



					source = newsLinkDict[maxCountLink][5]
					
					#Description limit
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
						self.logHandler.logger("generateHtmlFormat: %s"%maxCountLink)
										
												
					#===========================================================
					# #Image dogrulama
					#===========================================================
					imageId = linkImage[linkImage.rfind('/') + 1:]
					if self.showLink:
						self.logHandler.printMsg(maxCountLink, 3)
						self.logHandler.printMsg("Image: " + imageId, 3)
					if imageId:
						#Title var ise al
						if linkTitle:
							maxCountLinkInj = maxCountLink.replace("'", "''")
							try:
								searchLink = maxCountLinkInj.replace('http://', '')
								searchLink = searchLink.replace('www.', '')
							except:
								self.logHandler.logger("insertToDatabase")
								index -= 1
								continue
								
							imgSrc = ""
							if linkImage.find('imageslink/') == -1:
								#Hotlink ise yani indirilecek
								try:
									self.hotlinks.index(source)
									#DownloadImage var ise tekrar indirmez
									imageId = self.downloadImage(source, linkImage, self.linkImagePath)
									if imageId == 0:
										#Hotimage link indirlememisse google'da ara yok ise default kullan
										imgLinkGoogle  = self.getGoogleImage(linkTitle)
										if imgLinkGoogle:
											imgSrc = imgLinkGoogle
										else:
											imgSrc = 'imageslink/default.png'
									else:
										imgSrc = self.linkImagePath.split('/')[-2] + '/' + imageId
								except:
									if linkImage.find('.gif') != -1:
										#Hotimage link indirlememisse google'da ara yok ise default kullan
										imgLinkGoogle  = self.getGoogleImage(linkTitle)
										if imgLinkGoogle:
											imgSrc = imgLinkGoogle
										else:
											imgSrc = linkImage
									else:
										imgSrc = linkImage
							else:
								imgSrc = linkImage

							#===============================================
							# Ozel link degisiklikleri
							#===============================================
							for srcLink, replaceTuple in self.replaceStringForLink.iteritems():
								if srcLink == source:
									imgSrc = imgSrc.replace(replaceTuple[0], replaceTuple[1])

							#Linkler database kaydediliyor
							#Var ise update yapiliyor
							
							linkTitle = linkTitle.replace("'", "''")
							linkTitle = linkTitle.replace("\\", "")
							linkDesc = linkDesc.replace("'", "''")
							linkDesc = linkDesc.replace("\\", "")
							#Desc bozuk ise desc'e title'i ata
							try:
								self.notGetDesc.index(source)
								linkDesc = linkTitle
							except:
								pass
							imgSrc = imgSrc.replace("'", "''")
							
							if self.serverHandler.executeQuery("SELECT COUNT(*) FROM `links_%s` WHERE link='%s'"%(self.yearMonth, maxCountLinkInj))[0][0] == 0:
								self.serverHandler.executeQuery("INSERT INTO `links_%s` VALUES(NULL, CURRENT_DATE(), '%s', '%s', '%s', %d, %d, %d, '%s', '%s', '%s',0, NULL)"%(self.yearMonth, newsLinkDict[maxCountLink][4], newsLinkDict[maxCountLink][5], maxCountLinkInj, newsLinkDict[maxCountLink][0], newsLinkDict[maxCountLink][2], newsLinkDict[maxCountLink][3], linkTitle, linkDesc, imgSrc))
							if self.showLink:
								self.logHandler.printMsg(maxCountLink, 3)
							
					index += 1
				except:
					index -= 1
					self.logHandler.logger("insertToDatabase1", "Link html format hatasi: %s")
						
			return str(newsResult)
		except:
			self.logHandler.logger("insertToDatabase3")



	def run(self, category="", source=""):
		try:
			self.initCategory = ""
			self.initSource = ""
			if category:
				self.initCategory = category
				self.initSource = source
				print self.initCategory, self.initSource
			
					
			present = datetime.now()
			self.yearMonth = str(present.strftime('%Y%m'))
		
			
			#tempLinks truncate
			if present.hour == 1:
				self.serverHandler.executeQuery("TRUNCATE `tempLinks`")
			
			
			self.logHandler.printMsg("Starting [%s]"%str(present)[:19])
			
			#===========================================================
			# Kaynaklar olusturuluyor
			#===========================================================
			self.newsSources = createNewsSourceByPresent(present)
			
			#===========================================================================
			# Source sayimi icin count olusturuluyor sadece print'e lazim
			#===========================================================================
			totalSource = 0
			gundemTotalSource = 0
			otherCategoryTotalSource = 0
			for sourceCategory, sources in self.newsSources.iteritems():
				for sourceList in sources:
					if sourceCategory == "gundem":
						gundemTotalSource += 1
					else:
						otherCategoryTotalSource += 1
			if category == "gundem":
					totalSource = gundemTotalSource
			else:
				totalSource = otherCategoryTotalSource
				
			#===========================================================
			# Her bir kategor ve her onun her bir source'i icin tek tek islem yapiliyor
			#===========================================================
			count = 1
			newsLinkDict = {}

			for data in self.newsSources.iteritems():
				category = data[0]
				sources = data[1]

				#Kose yazilari 2 saaate bir kontrol edilsin	
				if present.hour % 2 != 0 and category == "koseyazilari":
					continue
				
				if self.initCategory:
					if self.initCategory.split('-')[0] != 'non' and self.initCategory != category:
						continue
					
					if self.initCategory.split('-')[0] == 'non' and self.initCategory.split('-')[1] == category:
						continue
					
				
				for sourceList in sources:
					startSource = datetime.now()
					source = sourceList[0]
					if self.initSource and source != self.initSource:
						continue
					
					#===========================================================
					# Siteye ozel asiri baglanma problemleri
					# Buraya eklenen code downloadImage metodunada eklenecek
					#===========================================================
					if source == 'cumhuriyet.com.tr':
						try:
							ln = 'http://www.cumhuriyet.com.tr'
							req = urllib2.Request(ln, headers={'User-Agent' : self.userAgent})
							html = urllib2.urlopen(req, timeout=5).read()
							if len(html) < 300:
								firstIndex = html.find('url=')
								endIndex = html[firstIndex:].find('"') + firstIndex
								
								url = html[firstIndex + len('url='): endIndex]
								if url and url.find('http') != -1:
									req = urllib2.Request(url, headers={'User-Agent' : self.userAgent})
									html = urllib2.urlopen(req, timeout=5).read()
									print url
						except:
							self.logHandler.logger("run")
					
					if source == 'odatv.com':
						try:
							ln = 'http://www.odatv.com'
							req = urllib2.Request(ln, headers={'User-Agent' : self.userAgent})
							html = urllib2.urlopen(req, timeout=5).read()
							if len(html) < 300:
								firstIndex = html.find('url=')
								endIndex = html[firstIndex:].find('"') + firstIndex
								
								url = html[firstIndex + len('url='): endIndex]
								if url and url.find('http') != -1:
									req = urllib2.Request(url, headers={'User-Agent' : self.userAgent})
									html = urllib2.urlopen(req, timeout=5).read()
									print url
						except:
							self.logHandler.logger("run")
					
					#===========================================================
					# Kaynagin parse islemi basliyor, ozellikleri aliniyor
					#===========================================================
					newsSourceLink = sourceList[1]
					newsSourceDiffWords = ()
					newsSourceBlackWords = ()
					if len(sourceList) > 2:
						newsSourceDiffWords = sourceList[2]
					if len(sourceList) > 3:
						newsSourceBlackWords = sourceList[3]
					
					self.logHandler.printMsg("Source: (%d / %d) %s"%(count, totalSource, newsSourceLink), 1)
					# #Linkdeki haberleri bul
					#===================================================
					try:
						newsLinkDict.update(self.getNewsLinkFromSource(present, category, source, newsSourceLink, newsSourceDiffWords, newsSourceBlackWords))
					except Exception, ex:
						self.logHandler.logger("run: %s:%s"%(newsSourceLink, ex))
					count += 1
					
					self.logHandler.printMsg("Time: %s"%(str(datetime.now() - startSource)[:7]), 1)
					self.insertToDatabase(category, newsLinkDict, 5)
					newsLinkDict.clear()

				
			self.logHandler.printMsg(str(datetime.now()) + ": Finished [%s]\n"%str(datetime.now() - present)[:19])
		except:
			self.logHandler.logger("run")
			
			
	def closeProcess(self, arg1, signal):
		self.serverHandler.closeConnection()
		sys.exit(1)
		
if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	main = Main()
	#Ctrl+C sinyalini yakalayan fonksiyonu cagirir. Cikis islemleri yaptirilir
	signal.signal(signal.SIGINT, main.closeProcess)
