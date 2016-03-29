#! -*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup
from LogHandler import LogHandler
import requests
import urllib2

class LinkHandler:
    def __init__(self, link, imageClass="", descMetaType="", linkContentDownload=False, requestType=0, cleanBrokenCh=False, timeout=3):
        self.logHandle = LogHandler("LinkHandler")
		
        self.htmlSource = ""
        self.soup = ""
        self.titleContent = ""
        self.descContent = ""
        self.imgContent = ""
		
        self.imageClass = imageClass		
        self.descMetaType = descMetaType
        self.link = link
        self.linkContentDownload = linkContentDownload
        self.requestType = requestType 
        self.cleanBrokenCh = cleanBrokenCh
        self.timeout = timeout
		
    def cleanUp(self, xstr):
        xstr = xstr.encode('utf-8').replace('Äą', 'ı').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ä±', "ı").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ĺ&Yuml;', 'ş').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Å', "ş").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('â&euro;&trade;', "'").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('â', "'").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ăź', 'ü').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ã¼', "ü").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ä&Yuml;', 'ğ').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ä', "ğ").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ä°', 'İ').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ă§', 'ç').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ã§', "ç").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ã¶', "ö").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ăś', 'ö').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Å&Yuml;', "ş").decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ã&oelig', 'ü').decode('utf-8')
        xstr = xstr.encode('utf-8').replace('Ã&Dagger;', 'Ç').decode('utf-8')

		
        return xstr
	
    def run(self):			
        try:
            try:
                if self.requestType:
                    self.htmlSource = requests.get(self.link, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"}, timeout=self.timeout).text
                else:
                    req = urllib2.Request(self.link, None, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"})
                    self.htmlSource = urllib2.urlopen(req, timeout=self.timeout).read()
            except Exception, error:
                print "\t\t\t%s: %s" % (error, self.link)
                self.soup = -1
                self.htmlSource = -1
                return
				
            #Link indirme degilse buraya
            if not self.linkContentDownload:
                #meta, title, content siralamasina gore parse
                self.soup = BeautifulSoup(self.htmlSource)
				
                #===============================================================
                # #Title
                #===============================================================
                titleContent = self.soup.findAll(attrs={"property":"og:title"})
                if not titleContent:
                    titleContent = self.soup.findAll(attrs={"name":"title"})
                if not titleContent:
                    titleContent = self.soup.findAll(attrs={"name":"twitter:title"})
                if not titleContent:
                    titleContent = self.soup.findAll(attrs={"name":"Search.Title"})
                if not titleContent:
                    titleContent = self.soup.findAll(attrs={"name":"Title"})
                if not titleContent:
                    titleContent = self.soup.findAll(attrs={"name":"TITLE"})
                if not titleContent:
                    try:
                        titleContent = self.soup.html.head.title
                    except:
                        pass
				
                #===============================================================
                # #Description
                #===============================================================
                if self.descMetaType:
                    descContent = self.soup.findAll(attrs=self.descMetaType)
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"name":"description"})
                else:
                    descContent = self.soup.findAll(attrs={"name":"description"})
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"property":"og:description"})
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"name":"twitter:description"})
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"name":"Search.Description"})
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"name":"Description"})
                    if not descContent:
                        descContent = self.soup.findAll(attrs={"name":"DESCRIPTION"})
						
                #===============================================================
                # #Image
                #===============================================================
                imgContent = ""
                if self.imageClass:
                    for imgClass in self.imageClass.split(','):
                        imgContentSpecial = self.soup.findAll(attrs={"id":"%s" % imgClass})
                        if imgContentSpecial:
                            imgContent = imgContentSpecial
                            break
				
                if not imgContent:
                    if self.imageClass:
                        for imgClass in self.imageClass.split(','):
                            imgContentSpecial = self.soup.findAll(attrs={"class":"%s" % imgClass})
                            if imgContentSpecial:
                                imgContent = imgContentSpecial
                                break
							
                if not imgContent:
                    if self.imageClass:
                        for imgClass in self.imageClass.split(','):
                            imgContentSpecial = self.soup.findAll(attrs={"itemprop":"%s" % imgClass})
                            if imgContentSpecial:
                                imgContent = imgContentSpecial
                                break

                if not imgContent:
                    if self.imageClass:
                        for imgClass in self.imageClass.split(','):
                            imgContentSpecial = self.soup.findAll(attrs={"rel":"%s" % imgClass})
                            if imgContentSpecial:
                                imgContent = imgContentSpecial
                                break
							
                if not imgContent:
                    if self.imageClass:
                        for imgClass in self.imageClass.split(','):
                            imgContentSpecial = self.soup.findAll(attrs={"name":"%s" % imgClass})
                            if imgContentSpecial:
                                imgContent = imgContentSpecial
                                break
							
                try:
                    if len(imgContent) > 0:
                        for i in imgContent:
                            if i.get('title'):
                                imgContent = i.get('src')
                            if i.find('img'):
                                img = i.find('img')
                                imgContent = img['src']

                except:
                    pass

                if len(str(imgContent)) < 4:
                    imgContent = ""

                try:
                    if str(imgContent).lower().find('.jpg') == -1 and str(imgContent).lower().find('.png') == -1 and str(imgContent).lower().find('.jpeg') == -1:
                        imgContent = ""
                except:
                    imgContent = ""
				
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"property":"og:image"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"name":"image"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"name":"twitter:image"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"name":"Search.Image"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"name":"Image"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"name":"IMAGE"})
				
                #Resim varmi yokmu kontrolu
                if str(imgContent)[str(imgContent).find('/'):].rfind('.') == -1:
                    imgContent = ""
					
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"id":"NewsImagePath"})
                if not imgContent:
                    imgContent = self.soup.findAll(attrs={"class":"yenihaberresmi"})
                if not imgContent:
                    imgContent = self.soup.find("link", {"rel": "image_src"})
					
                #=======================================================================
                # Title hazirlaniyor
                #=======================================================================
                if titleContent:
                    if str(titleContent)[0] == '<':
                        self.titleContent = titleContent.text
                    else:
                        try:
                            self.titleContent = titleContent[0]['content']
                        except:
                            try:
                                self.titleContent = titleContent[0]['value']
                            except:
                                pass
							
                #===============================================================
                # Description hazirlaniyor
                #===============================================================
                if descContent:
                    try:
                        self.descContent = descContent[0]['content']
                    except Exception, error:
                        try:
                            self.descContent = descContent[0]['value']
                        except:
                            pass
						
                #===========================================================
                # Image hazirlaniyor
                #===========================================================
                if imgContent:
                    try:
                        imgContent = imgContent[0]['src']
                    except:
                        try:
                            imgContent = imgContent[0]['content']
                        except:
                            try:
                                imgContent = imgContent[0]['value']
                            except:
                                try:
                                    imgContent = imgContent[0]['href']
                                except:
                                    try:
                                        imgContent = dict(imgContent.attrs)['href']
                                    except:	
                                        imgContent = str(imgContent)
							
						
                    if imgContent.count('http://') > 1:
                        imgContent = imgContent[imgContent[5:].find('http://') + 5:]
                    if imgContent.find('https://') != -1:
                        imgContent = imgContent.replace('https://', 'http://')
						
                    if imgContent.find('http://') == -1:
                        #Uzanti var ise hostname ekleme
                        from urlparse import urlparse
                        hostname = urlparse(self.link).netloc
                        ext = '.' + hostname.split('.')[-1]
                        if imgContent.find(ext) == -1:
                            imgContent = hostname + '/' + imgContent
                        #http ekle
                        imgContent = "http://" + imgContent
						
                    imgContent = imgContent.replace('////', '//')
                    #===========================================================
                    # imgContent = imgContent[:10] + imgContent[10:].replace('//', '/')
                    #===========================================================
                    if imgContent.find('mc.yandex.ru/watch') == -1:
                        self.imgContent = imgContent
				
                #===============================================================
                # Html'ler yok ediliyor
                #===============================================================
                soup = BeautifulSoup(self.titleContent)
                self.titleContent = soup.text
                soup = BeautifulSoup(self.descContent)
                self.descContent = soup.text
                soup = BeautifulSoup(self.imgContent)
                self.imgContent = soup.text
	
                if self.cleanBrokenCh:
                    self.titleContent = self.cleanUp(self.titleContent)
                    self.descContent = self.cleanUp(self.descContent)
				
                #===============================================================
                # Print
                #===============================================================
                #===============================================================
                # print "=" * 50
                # print self.link
                # print test.titleContent
                # print test.descContent
                # print test.imgContent
                # print "=" * 50
                #===============================================================
					
        except ValueError, error:
            if str(error).find('unichr() arg not in range(0x10000) (narrow Python build)') == -1:
                self.logHandle.logger("run", self.link)
            self.soup = -1
            self.htmlSource = -1
            return
        except TypeError, error:
            if str(error).find("cannot concatenate 'str' and 'NoneType' objects") == -1:
                self.logHandle.logger("run", self.link)
            self.soup = -1
            self.htmlSource = -1
            return
        except:
            self.soup = -1
            self.htmlSource = -1
            self.logHandle.logger("run", self.link)
            self.logHandle.logger("run")
            return
		

#===============================================================================
# test = LinkHandler("http://www.haber7.com/ortadogu/haber/1453906-isidten-dunyayi-sarsacak-plan", imageClass="image_src")
# test.run()
# test = LinkHandler("http://amkspor.com/2014/03/03/torogludan-f-bahce-gondermesi-266914/", imageClass="in_image")
# test.run()
# test = LinkHandler("http://www.trthaber.com/haber/gundem/hsyk-kanun-teklifi-kabul-edildi-118319.html", imageClass="image")
# test.run()
# test = LinkHandler("http://amkspor.com/2013/12/28/ruya-gibi-proje-235880/")
# test.run()
# test = LinkHandler("http://www.donanimhaber.com/hdd_ssd/haberleri/Samsung-840-Pro-256GB-SSD-video-inceleme-Sinifinda-liderlige-oynuyor.htm")
# test.run()
# test = LinkHandler("http://www.webrazzi.com/2013/08/26/web-uyelik-kapatma-justdeleteme")
# test.run()
# test = LinkHandler("http://www.chip.com.tr/haber/iphone-5s-ve-5c-yan-yana_42250.html")
# test.run()
# test = LinkHandler("http://www.cnnturk.com/2013/spor/futbol/08/26/stuttgartta.labbadianin.bileti.kesildi/720882.0/index.html")
# test.run()
# test = LinkHandler("http://www.ajansspor.com/futbol/superlig/h/20130826/muslera_ne_zaman_burada_oynasak.html")
# test.run()
# test = LinkHandler("http://www.zaman.com.tr/kultur_kerkukun-anadolunun-bir-parcasi-oldugunu-herkese-anlatmak-istedim_2124305.html")
# test.run()
# test = LinkHandler("http://www.ajansspor.com/yazarlar/lutfilutic/h/20130901/imparatore_olur_yalantore.html")
# test.run()
#===============================================================================
