# -*- coding: utf-8 -*-

import sys, operator, time
import signal
from datetime import datetime, timedelta
from LogHandler import LogHandler
from ServerDatabaseHandler import ServerDatabaseHandler


class Main:
	def __init__(self):		
		
		#=======================================================================
		# Configuration
		#=======================================================================
		#Alinmamasi gereken kelimeler
		self.blackWordListOne = []
		self.blackWordListTwo = []
		
		self.present = datetime.now().date()
		self.yesterday = self.present - timedelta(days=1)
		self.yearMonth = str(self.present.strftime('%Y%m'))
		self.presentLastMonth = self.present - timedelta(days=30)
		self.yearLastMonth = str(self.presentLastMonth.strftime('%Y%m'))
		
		self.serverHandler = ServerDatabaseHandler()
		print datetime.now()
		
		self.serverHandler.executeQuery("""CREATE TABLE IF NOT EXISTS `trendWords` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `text` varchar(255) CHARACTER SET utf32 COLLATE utf32_unicode_ci DEFAULT NULL,
  `newscount` int(11) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;""")
		try:
			self.serverHandler.executeQuery("ALTER TABLE `trendWords` ADD PRIMARY KEY (`id`)")
		except:
			pass
		
		lsCategories = ["gundem", "videohaber", "spor", "koseyazilari", "kulturvesanat", "teknoloji"]
		lsDataTypes = ["guncel"]
		for category in lsCategories:
			for dataType in lsDataTypes:
				self.category = category
				self.dataType = dataType
				print self.category, self.dataType
				mostCommonWordsList = self.getMostCommonWordsFromMetaContent()
				for i in mostCommonWordsList:
					text = i[0]
					text = text.replace("'", "''")
					count = i[1]
					if 0 == self.serverHandler.executeQuery("SELECT COUNT(*) FROM `trendWords` WHERE category='%s' and text='%s' and date=CURRENT_DATE()"%(self.category, text))[0][0]:
						self.serverHandler.executeQuery("INSERT INTO `trendWords` VALUES(NULL, CURRENT_DATE(), '%s', '%s', %d)"%(self.category, text, count))
					print "\t", self.category, text, count
		print ""
		print ""

		
	def isUpper(self, text):
		try:
			wordDictU = {'İ':'I', 'Ö':'O', 'Ü':'U', 'Ç':'C', 'Ş':'S', 'Ğ':'G'}
			wordDictL = {'ı':'i', 'ö':'o', 'ü':'u', 'ç':'c', 'ş':'s', 'ğ':'g'}
			
			for data in wordDictU.iteritems():
				if text[0:2].find(data[0]) != -1:
					text = text.replace(data[0], data[1])
			
			for data in wordDictL.iteritems():
				if text[0:2].find(data[0]) != -1:
					text = text.replace(data[0], data[1])
			
			try:
				int(text)
				return True
			except ValueError:
				pass
			
			if text[0].isupper():
				return True
			else:
				return False
		except:
			self.logHandler.logger("isUpper", text)
			return False
		
	def getMostCommonWordsFromMetaContent(self):
		
		metaContents = ""
		linkForNews = []
		
		if self.category == "gundem":
			linkForNews.extend(list(self.serverHandler.executeQuery("SELECT title, description FROM `links_%s` WHERE tweetCount+facebookCount > 10 AND `date` = '%s' AND category = '%s'"% (self.yearMonth, self.present, self.category))))
		else:
			linkForNews.extend(list(self.serverHandler.executeQuery("SELECT title, description FROM `links_%s` WHERE `date` = '%s' AND category = '%s'"% (self.yearMonth, self.present, self.category))))
		for items in linkForNews:
			metaContents += ' ' + items[0] + ' ' + items[1] + ' '
		metaWordList = metaContents.split()
		wordsDict = {}
		indexList = []

		#Blackwordlist'de var ise sil
		for index, word in enumerate(metaWordList):
			try:
				self.blackWordListOne.index(word)
				metaWordList.remove(word)
			except:
				pass
	
		for index, word in enumerate(metaWordList):
			mostWord = []
			try:
				indexList.index(index)
				continue
			except:
				pass
			
			while True:
				try:
					metaWordList[index]
				except:
					break
				if self.isUpper(metaWordList[index]):
					mostWord.append(metaWordList[index])
					index += 1
					indexList.append(index)
				else:
					break
				
			mostWord = ' '.join(mostWord)
			
			#Icinde nokta virgul olanlari alma anlamsiz
			if mostWord[2:-2].find('.') != -1:
				continue
			if mostWord[2:-2].find(',') != -1:
				continue
			
			if mostWord:
				#' kaldiriliyor
				sp = mostWord.split()
				if len(sp) == 2:
					if sp[0].find("'") != -1:
						mostWord = ' '.join([sp[0][:sp[0].find("'")], sp[1]])
						sp = mostWord.split()
					if sp[1].find("'") != -1:
						mostWord = ' '.join([sp[0], sp[1][:sp[1].find("'")]])
						sp = mostWord.split()

					if sp[0].find("’") != -1:
						mostWord = ' '.join([sp[0][:sp[0].find("’")], sp[1]])
						sp = mostWord.split()
					if sp[1].find("’") != -1:
						mostWord = ' '.join([sp[0], sp[1][:sp[1].find("’")]])
		
				#en sondaki , varsa kaldiriliyor
				if mostWord[-1] == ',':
					mostWord = mostWord[:-1]
				
				#Blackwordlist'de var ise sil
				try:
					flag = False
					for blackWord in self.blackWordListTwo:
						if mostWord.find(blackWord) != -1:
							flag = True
					if flag:
						continue
				except:
					pass
				
				try:
					wordsDict[mostWord] += 1
				except:
					wordsDict[mostWord] = 1
	
		#En yaygin kelimeler aliniyor
		lastDict = {}
		index = 0
		while len(wordsDict):
			index += 1
			if index > 100:
				break;

			commonWord = max(wordsDict, key=wordsDict.get)
			#En az 3 haber olsun
			if wordsDict[commonWord] < 3:
				continue
	
			#Count 1'den fazla ise
			if len(commonWord.split()) == 2: 
				lastDict[' '.join(commonWord.split()[0:3])] = wordsDict[commonWord]
				index += 1
	
			del wordsDict[commonWord]
			
		return reversed(sorted(lastDict.iteritems(), key=operator.itemgetter(1)))


	def closeProcess(self, arg1, signal):
		sys.exit(1)
		
		
if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	main = Main()
	# Ctrl+C sinyalini yakalayan fonksiyonu cagirir. Cikis islemleri yaptirilir
	signal.signal(signal.SIGINT, main.closeProcess)
