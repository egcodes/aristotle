# -*- coding: utf-8 -*-

def createNewsSourceByPresent(present):
		months = {'01':'Ocak', '02':'Şubat', '03':'Mart', '04':'Nisan', '05':'Mayıs', '06':'Haziran', '07':'Temmuz', '08':'Ağustos', '09':'Eylül', '10':'Ekim', '11':'Kasım', '12':'Aralık'}
		monthsUpper = {'01':'OCAK', '02':'ŞUBAT', '03':'MART', '04':'NİSAN', '05':'MAYIS', '06':'HAZİRAN', '07':'TEMMUZ', '08':'AĞUSTOS', '09':'EYLÜL', '10':'EKİM', '11':'KASIM', '12':'ARALIK'}
		monthsShort = {'01':'Oca', '02':'Şub', '03':'Mar', '04':'Nis', '05':'May', '06':'Haz', '07':'Tem', '08':'Ağu', '09':'Eyl', '10':'Eki', '11':'Kas', '12':'Ara'}
		
		monthEng = {'Haziran':'June', 'Temmuz':'July', 'Ağustos':'August', 'Mart':'March', 'Nisan':'April', 'Mayıs':'May',  'Eylül':'September', 'Ekim':'October', 'Kasım':'November', 'Aralık':'December', 'Ocak':'January', 'Şubat':'February'}

		today = str(present.strftime('%Y/%m/%d'))
		todayFirstYear = str(present.strftime('%Y-%m-%d'))
		todayNonZeroMounthNonYear = '/'.join(today.split('/')[1:])
		todayNonZeroMounthNonZeroDayYear = todayNonZeroMounthNonYear
		todayMonth = str(present.strftime('%m'))
		todayTrFormat = str(present.strftime('%d %m %Y'))
		todayTrFormat = todayTrFormat[:3] + todayTrFormat[3:-4].replace(todayMonth, months[todayMonth]) + todayTrFormat[-4:]
		todayTrShortFormat = str(present.strftime('%d %m %Y'))
		todayTrShortFormat = todayTrShortFormat[:3] + todayTrShortFormat[3:-4].replace(todayMonth, monthsShort[todayMonth]) + todayTrShortFormat[-4:]
		todayTrPointFormat2 = str(present.strftime('%d %m. %Y'))
		todayTrPointFormat2 = todayTrPointFormat2[:3] + todayTrPointFormat2[3:-4].replace(todayMonth, months[todayMonth]) + todayTrPointFormat2[-4:]
		todayTrFormatSpace = todayTrFormat.replace(' ', '&nbsp;')
		todayTrFormatUpper = str(present.strftime('%d %m %Y'))
		todayTrFormatUpper = todayTrFormatUpper[:3] + todayTrFormatUpper[3:-4].replace(todayMonth, monthsUpper[todayMonth]) + todayTrFormatUpper[-4:]
		todaySlashFormat = str(present.strftime('%d/%m/%Y'))
		todaySlashFormatReverse = str(present.strftime('%Y/%m/%d'))
		todayLineFormat = str(present.strftime('%d-%m-%Y'))
		todayLineFormatReverse = str(present.strftime('%Y-%m-%d'))
		todayPointFormat = str(present.strftime('%d.%m.%Y'))
		todayTrFormatSpecial = str(present.strftime('%d %m, %Y'))
		todayTrFormatSpecial = todayTrFormatSpecial[:3] + todayTrFormatSpecial[3:-4].replace(todayMonth, monthsUpper[todayMonth]) + todayTrFormatSpecial[-4:]
		todayNoneZeroTrFormatSpecial = todayTrFormatSpecial[1:]
		todayBbcFormat = '/'.join(today.split("/")[:2]) + '/' + today.split("/")[0][2:] + today.split("/")[1] + today.split("/")[2]
		
		todayTrNonZeroFormat = todayTrFormat
		if todayTrFormat[0] == '0':
			todayTrNonZeroFormat = todayTrFormat[1:]
		
		todayTrNonZeroShortFormat = todayTrNonZeroFormat.split()[0] + " " + todayTrNonZeroFormat.split()[1][:3] + " " + todayTrNonZeroFormat.split()[2]
		
		todayEnNonZeroFormat = todayTrNonZeroFormat.split()[0] + ' ' + monthEng[todayTrNonZeroFormat.split()[1]] + ' ' + todayTrNonZeroFormat.split()[2]
			
		if todayNonZeroMounthNonYear[0] == '0':
			todayNonZeroMounthNonYear = todayNonZeroMounthNonYear[1:]
			
		todayNonZeroMounthNonZeroDayYear = str(present.strftime('%m/%d'))
		if todayNonZeroMounthNonZeroDayYear[-2] == '0':
			todayNonZeroMounthNonZeroDayYear = todayNonZeroMounthNonZeroDayYear.split('/')[0] + '/' + todayNonZeroMounthNonZeroDayYear[-1]

		todayTrFormatSpecial2 = str(present.strftime('%m %d, %Y'))
		todayTrFormatSpecial3 = str(present.strftime('%m %d, %Y'))
		if todayTrFormatSpecial2.split()[1][0] == '0':
			todayTrFormatSpecial2 = todayTrFormatSpecial2.split()[0] + ' ' + todayTrFormatSpecial2.split()[1][1:] + ' ' +todayTrFormatSpecial2.split()[2]
			todayTrFormatSpecial3 = todayTrFormatSpecial3.split()[0] + ' ' + todayTrFormatSpecial3.split()[1] + ' ' +todayTrFormatSpecial3.split()[2]
		else:
			todayTrFormatSpecial2 = todayTrFormatSpecial2.split()[0] + ' ' + todayTrFormatSpecial2.split()[1] + ' ' + todayTrFormatSpecial2.split()[2]
			todayTrFormatSpecial3 = todayTrFormatSpecial3.split()[0] + ' ' + todayTrFormatSpecial3.split()[1] + ' ' +todayTrFormatSpecial3.split()[2]
		todayTrFormatSpecial2 = todayTrFormatSpecial2[:3].replace(todayMonth, months[todayMonth]) + todayTrFormatSpecial2[3:] 
		todayTrFormatSpecial3 = todayTrFormatSpecial3[:3].replace(todayMonth, months[todayMonth]) + todayTrFormatSpecial3[3:] 

		todayTrNonZeroFormatUpper = str(present.strftime('%d %m %Y'))
		todayTrNonZeroFormatUpper = todayTrNonZeroFormatUpper[:3] + todayTrNonZeroFormatUpper[3:-4].replace(todayMonth, monthsUpper[todayMonth]) + todayTrNonZeroFormatUpper[-4:]
		if todayTrFormatUpper[0] == '0':
			todayTrNonZeroFormatUpper = todayTrFormatUpper[1:]
		if todayTrShortFormat[0] == '0':
			todayTrNonZeroShortFormat = todayTrShortFormat[1:]
		else:
			todayTrNonZeroShortFormat = todayTrShortFormat
		
		#Haber kaynaklari
		# Asagidaki dict sirasi ve anlamlari
			# Kaynak adi
			# Kaynak adresi
			# Kaynak haberinin linkinde olmasi gerekenler
			# Kaynak haberin linkinde olmaması gerekenler
			# Bugun tarihi icin ayirac 0, 1, 2 turleri var
			# Title sonlarinda gazete ismi silmek icin -> {karakter:sayisi verildidinde sola dogru siler}
			# Sadece silinecek kelime(ler) ve 1 verilerek o yazi silinir
		
		newsSources = {
				'gundem':	[
								 #('zaman.com.tr', 'http://www.zaman.com.tr', ('haber_', 'gundem_', 'ekonomi_', 'dunya_', 'aile-saglik_', 'egitim_',), ('wetransfer.','ihsan-dagi', 'abdulhamit-bilici', 'mumtazer-turkone'), ({'detayTarihNew':todayTrNonZeroFormat},)),
								 ('sozcu.com.tr', 'http://www.sozcu.com.tr', ('/gundem/', '/gunun-icinden/', '/dunya/', '/ekonomi/', '/egitim/', '/saglik/',), ('spor_', 'video.', ), ({'news-content-date _flex _aic':todayTrFormatSpecial2},)),
								 ('milliyet.com.tr','http://www.milliyet.com.tr', ('/detay/',), ('secure.milliyet.com.tr','/ydetay/', 'skorer.'),({'date':todayPointFormat},{'detSpan':todayTrFormat}, {'detSpan2':todayTrFormat}), {'-':1}),
								 ('hurriyet.com.tr', 'http://www.hurriyet.com.tr/', ('-',), (), ({'col-md-4 text-right':todayTrFormat},)),
								 ('haber7.com', 'http://www.haber7.com', ('/haber/',), ('/teknoloji/', 'spor.','/yazarlar/'), ({'info readInfo':todayTrFormat}, )),
								 ('haberturk.com','http://www.haberturk.com', ('/haber/','/yasam/', '/gundem/', '/ekonomi/', '/dunya/', '/medya/', '/saglik/'), ('/yazarlar/', '/fiskos/', '/video/', '/teknoloji/', '/spor/', '/kultur-sanat/','spor.', 'magazin.',), ({'date':todayTrFormat}, {'HaberTarih':todayTrFormat}, {'videoDetayInfo':todayPointFormat}), {'|':1}),
								 ('t24.com.tr', 'http://t24.com.tr', ('/haber/', '/gundem/','/politika/', '/egitim/', '/yasam/', '/ekonomi/', '/dunya/', ), (), ({'story-date':todayTrFormat},)),
								 #('radikal.com.tr', 'http://www.radikal.com.tr', ('/turkiye/', '/ekonomi/', '/politika/', '/dunya/', '/hayat/', '/radikalist/', ), (), ({'date':todaySlashFormat},), {'-':1}),
								 ('ntv.com.tr', 'http://www.ntv.com.tr', ('/turkiye/','/dunya/', '/ekonomi/', '/saglik/','/yasam/', '/egitim/',), (), ({'time':todayTrNonZeroFormat},), ),
								 ('cnnturk.com', 'http://www.cnnturk.com', ('/ekonomi/', '/turkiye/', '/dunya/', '/yasam/',  ), (), ({'date':todayPointFormat}, {'sm':todayPointFormat},), {'-':1}),
								 ('gazetevatan.com', 'http://www.gazetevatan.com', ('-gundem', '-dunya', '-siyaset', '-ekonomi', '-finas', '-yasam', '-egitim',), (), ({'cdate':todayTrFormat},{'datesrc':todayTrFormat}), {'|':1}),
								 ('ensonhaber.com', 'http://www.ensonhaber.com', (todayLineFormatReverse,), ('kralspor.',), (1)),
								 ('haber.sol.org.tr', 'http://haber.sol.org.tr/anasayfa', ('/turkiye/','/emek-sermaye/', '/dunya/', '/toplum/', '/medya/',), (), ({'date-display-single':todayTrFormat},), {'|':2},),
								 ('trthaber.com', 'http://www.trthaber.com', ('/gundem/', '/turkiye/', '/dunya/', '/ekonomi/', '/egitim/',), (), ({'detTarih':todayTrFormat},)),
								 ('star.com.tr', 'http://www.star.com.tr/default.asp', ('/guncel/', '/politika/', '/ekonomi/', '/dunya/', '/medya/', '/egitim/',), (), ({'date2':todayPointFormat},), {'-':1}),
								 ('sabah.com.tr', 'http://www.sabah.com.tr', (today,), ('/yazarlar/', '/teknoloji/', '/kultur_sanat/', '/sinema/', '/fotohaber/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/otomobil/', '/eGazete/',), (1), {'-':1}),
								 ('internethaber.com', 'http://www.internethaber.com/?interstitial=true', ('.htm',), ('gazeteoku.com', 'otomobil.internethaber.com', 'spor.', ), ({'rpt':'%s'%todaySlashFormat},{'info':'Tarihi :%s'%todayLineFormat})),
								 ('mynet.com', 'http://www.mynet.com', ('haber.', '/detay/', 'yurthaber.','.finans','/haber/','/yasam/', '/galeri/', '/ekonomi/', '/dunya/', '/medya/', '/saglik/'), ('/teknoloji/','spor.',), ({'newsInfo':todayTrNonZeroFormat},)),
								 ('samanyoluhaber.com', 'http://www.samanyoluhaber.com', ('-',), ('/yazar/', 'fenerbahce', 'besiktas', 'galatasaray',), ({'wrap':todayTrShortFormat},)),
								 ('cumhuriyet.com.tr', 'http://www.cumhuriyet.com.tr', ('/siyaset/','/turkiye/', '/dunya/', '/ekonomi/','/yasam/', '/egitim/', '/saglik/',), (), ({'publish-date':todayTrFormat},)),
								 #('yeniakit.com.tr', 'http://www.yeniakit.com.tr/gundem', ('/haber/',), (), ({"news_analysis":todayTrFormat},)),	
								 ('takvim.com.tr', 'http://www.takvim.com.tr', (today,), ('/Yazarlar/', '/yazarlar/', '/spor/', '/Spor/', '/Televizyon', '/multimedya/', '/Saklambac/', '/saklambac/'), (1),),
								 ('posta.com.tr', 'http://www.posta.com.tr', ('/HaberDetay/',), ('/video/','video.', '/YazarHaberDetay/', '/spor/', '/teknoloji/', ), ({'date':todayTrFormat},), {'-':1},),										
								 ('turkiyegazetesi.com.tr', 'http://www.turkiyegazetesi.com.tr', ('/gundem/','/dunya/', '/egitim/', '/yasam/', '/saglik/', '/politika/', '/ekonomi/', ), ('/spor/','/teknoloji/', '/yazarlar/',), ({'story_date clearfix':todayPointFormat},),),										
								 ('yenisafak.com.tr', 'http://www.yenisafak.com.tr', ('/dunya/', '/gundem/', '/politika/', '/ekonomi/', '/saglik/', '/egitim/',), ('/yazarlar/', '/spor/', '/teknoloji/',), ({'info':todayTrFormatSpecial3},), {'-':1}),										 
								 ('odatv.com', 'http://www.odatv.com', ('-',), (), ({'yaziboyut':todayPointFormat},)),
								 ('bugun.com.tr', 'http://www.bugun.com.tr', ('/gundem/', '/dunya/', '/yasam/', '/ekonomi/', '/politika/', '/egitim/', '/saglik/',), (), ({'pubdate':todayPointFormat},)),
								 ('taraf.com.tr', 'http://www.taraf.com.tr', ('-', ), ('/kategori/',), ({'post-meta':todayTrNonZeroFormat},), {'|':1}),
								 ('aljazeera.com.tr', 'http://www.aljazeera.com.tr', ('/haber/','/al-jazeera-ozel/', '/gorus/', '/izle/',), (), ({'meta':todayTrNonZeroShortFormat},)),
								 ('bbc.co.uk/turkce', 'http://www.bbc.co.uk/turkce', (todayBbcFormat,), ('/konular/','/sport/' '/spor/',), (1),{'-':1}),
								 ('haberler.com', 'http://www.haberler.com', ('-haberi',), ('fotogaleri.',), ({'nav1':todayTrFormat},)),
								 ('diken.com.tr', 'http://www.diken.com.tr', ('-',), ('/kategori/', 'bu-gazete/', '-ekim-', '-kasim-', '-aralik-', '-ocak-', '-subat-', '-mart-', '-nisan-', '-mayis-', '-haziran-', '-temmuz-', '-agustos-', '-eylul-',), ({'entry-time':todaySlashFormat},), {'-':1}),
								 ('aksam.com.tr', 'http://www.aksam.com.tr', ('/siyaset/', '/guncel/', '/yasam/', '/ekonomi/', '/dunya/',), ('/teknoloji/', '/spor/', '/magazin/', '/yazarlar/',), ({'newsDate':todayTrFormat},), {'-':1}),
							
								],
			
				'videohaber': [
								('hurriyet.com.tr', 'http://webtv.hurriyet.com.tr', ('webtv.',), (), ({'upload-date':todayPointFormat}, )),
								('cnnturk.com', 'http://www.cnnturk.com/video', ('/video/',), (), ({'date':todayPointFormat},), {'-':1}),
								('ensonhaber.com', 'http://videonuz.ensonhaber.com', ('/izle/',), (), ({'timeInfo':todayFirstYear},)),
								('haber7.com', 'http://video.haber7.com/', ('/video-galeri/',), (), ({'description':todayPointFormat},)),
								('trthaber.com', 'http://www.trthaber.com/video-galerileri.html', ('/videolar/',), ('/videolar/ekonomi','/videolar/kultur-sanat', '/videolar/yasam', '/videolar/spor', '/videolar/gundem', '/videolar/magazin', '/videolar/cevre', '/videolar/dunya', '/videolar/medya', '/videolar/saglik', '/videolar/egitim', '/videolar/turkiye', '/videolar/bilim-teknik' ), ({'balonIc_bilgi':todayPointFormat},)),
								#('izlesene.com', 'http://www.izlesene.com/videolar/haber/bugun', ('/video/',), (), ({'show-for-md-up':todayTrFormat},)),
								('milliyet.com.tr', 'http://www.milliyet.com.tr/Milliyet-Tv/', ('video-izle',), ('canli-yayin-videosu',), ({'detSpan':todayTrFormat},)), 
								('ntv.com.tr', 'http://www.ntv.com.tr/video', ('/video/',), (), ({'clock':todayPointFormat},)),
							    # Tarih yok sayfada
							    #('haberturk.com','http://video.haberturk.com/', ('/video/',), (), ({'date':todayTrFormat}, {'HaberTarih':todayTrFormat}, {'videoDetayInfo':todayPointFormat})),
								 ],
			
				'teknoloji':[
								('chip.com.tr', 'http://www.chip.com.tr', ('/haber/', '/makale/','/blog/','/inceleme/'), (), ({'datePublished':todayTrFormat},)),
								('donanimhaber.com', 'http://www.donanimhaber.com', ('/haberleri/',), ('forum.donanimhaber.com','/2si1/','/mesut-cevik-ile-canli/',), ({'tarih post-date':todayTrNonZeroFormat},)),
								('webrazzi.com', 'http://www.webrazzi.com', (today,), (), (1), {'|':1}),
								('shiftdelete.net', 'http://shiftdelete.net', ('-',), ('forum.',), ({'pdate':todayPointFormat},), {'-':1}),
								('ntv.com.tr', 'http://www.ntv.com.tr/teknoloji', ('/teknoloji/',), (),({'time':todayTrNonZeroFormat},),),
								('teknokulis.com', 'http://www.teknokulis.com', (today,), ('teknokulis.com/Haberler/%s'%today,), (1),),
								('teknolojioku.com', 'http://www.teknolojioku.com', ('/haber/',), (), ({'newsDetailInfo':todaySlashFormat}, )),
								('mynet.com', 'http://www.mynet.com/teknoloji', ('/teknoloji/',), (), ({'newsInfo':todayTrNonZeroFormat},)),
								('bigumigu.com', 'http://www.bigumigu.com', ('/haber/',), (), ({'category':'%s'%todayTrFormat},)),
								('sosyalmedya.co', 'http://www.sosyalmedya.co', ("-",), ('/sosyal-medya', '/sosyal-marka', '/yeni-girisimler', '/e-ticaret',), ({'date':'%s'%todayTrNonZeroFormat},), {'Sosyal Medya':1}),
								('silikonvadisi.tv', 'http://www.silikonvadisi.tv', ('.html',), (), ({'entry-date updated td-module-date':todayTrNonZeroFormat},), {'-':1}),
								('webtekno.com', 'http://www.webtekno.com', ('.html',), (), ({'author show-for-large-up':"önce"},), ),
 								('fizikist.com', 'http://www.fizikist.com', ('-',), (), ({'content_time':todayTrFormat},), {'-':1}),
 								# Haber disinda sayfalar geliyor ayirt edici kelime yok
 								#('gercekbilim.com', 'http://www.gercekbilim.com', ('-',), (), ({'entry-meta':todayTrFormat},), {'-':1}),
 								#link'de tr. olmasi isleri karistiyor
 								#('tr.sputniknews.com/bilim', 'http://tr.sputniknews.com/bilim', ('/bilim/',), (), ({'b-article__refs-date':todayPointFormat},), {'-':1}),
 								# Ayni date class'i sayfada birden cok geliyor
 								# (bilimfili.com), 


							   ],
			
				'kulturvesanat':
								[
								 ('haberturk.com','http://www.haberturk.com/kultur-sanat', ('/kultur-sanat/',), (), ({'date':todayTrFormat}, {'HaberTarih':todayTrFormat}, {'videoDetayInfo':todayPointFormat}), {'|':1}),
								 ('hurriyet.com.tr', 'http://www.hurriyet.com.tr/keyif', ('-',), (), ({'date FR':todayTrFormat},)),
								 #('radikal.com.tr', 'http://www.radikal.com.tr/kultur', ('/kultur/', '/sinema/', ), (), ({'date':todaySlashFormat},), {'-':1}),
								 #('zaman.com.tr', 'http://www.zaman.com.tr/kultur', ('kultur_',), ('/roportaj',), ({'detayTarihNew':todayTrNonZeroFormat},)),
								 #('zaman.com.tr', 'http://www.zaman.com.tr/muzik', ('cumaertesi_', 'pazar_', 'kultur_', 'cumartesi_'), ('/roportaj',), ({'detayTarihNew':todayTrNonZeroFormat},)),
								 #('zaman.com.tr', 'http://www.zaman.com.tr/tv-rehberi', ('tv-rehberi_',), ('/roportaj',), ({'detayTarihNew':todayTrNonZeroFormat},)),
								 ('cnnturk.com', 'http://www.cnnturk.com/kultur-sanat', ('/kultur-sanat/', ), (), ({'date':todayPointFormat},{'sm':todayPointFormat},), {'-':1}),
								 ('t24.com.tr', 'http://t24.com.tr/kultur-sanat', ('/haber/',), (), ({'story-date':todayTrFormat},)),
								 ('ntv.com.tr', 'http://www.ntv.com.tr/sanat', ('/sanat/',), (),({'time':todayTrNonZeroFormat},),),
								 ('haber7.com', 'http://www.haber7.com/kultur', ('/kultur/', '/kulturel-etkinlikler/', '/mimari/', '/muzik/', '/arkeoloji/', '/sinema/', '/tarih-ve-fikir/', '/edebiyat/', '/fotograf/', '/plastik-sanatlar/', 'tiyatro-ve-sahne-sanatlari',), (), ({'info readInfo':todayTrFormat}, )),
								 ('sabah.com.tr', 'http://www.sabah.com.tr/kultur_sanat', (today,), ('/gundem/','/ekonomi/', '/yasam/', '/dunya/', '/piyasa/', '/teknoloji/', '/egitim/', '/turizm/', '/fotohaber/', '/Turizm/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/otomobil/'), (1), {'-':1}),
								 ('trthaber.com', 'http://www.trthaber.com/haber/kultur-sanat/', ('/kultur-sanat/', ), (), ({'detTarih':todayTrFormat},)),

								],
			
				'spor':		[
								('fanatik.com.tr', 'http://www.fanatik.com.tr', (today,), ('KategoriSayfasi','AnketmerkeziTumYorumlar',"tum-yorumlar",), (1), {'-':1}),
								('ntvspor.net', 'http://www.ntvspor.net', ('/haber/', '/video-galeri/', '/foto-galeri/'), (), ({'newsDate':todayTrNonZeroFormat},),),
								('amkspor.sozcu.com.tr', 'http://amkspor.sozcu.com.tr', (today,), (), (1), {'-':1}),
								('sporx.com', 'http://www.sporx.com/?giris=ok', ('-',), (), ({'haberdate':todayTrFormat},)),
								('mackolik.com', 'http://www.mackolik.com/default.aspx', ('/Haber/',), (), ({'float:left;text-align:left;padding-left:20px;':todayPointFormat},)),
								('ajansspor.com', 'http://www.ajansspor.com/index.html', ('/futbol/', '/basketbol/', '/voleybol/', '/motorsporlari/',), ('Motokros', 'amputefutbol', '/yazarlar/',), ({'tamGrey10':todayTrFormatSpace},)),
								('cnnturk.com', 'http://www.cnnturk.com/spor', ('/spor/', ), (), ({'date':todayPointFormat},{'sm':todayPointFormat},),),
								('fotomac.com.tr', 'http://www.fotomac.com.tr', (today,), ('/Yazarlar/',), (1), {'–':2}),
								],
				
				'koseyazilari': [
								 ('haberturk.com','http://www.haberturk.com/htyazarlar', ('/yazarlar/',), (), ({'date':todayTrFormatUpper}, {'HaberTarih':todayTrFormat}, {'videoDetayInfo':todayPointFormat}, {'group news-date-create mbottom10 ':todayTrFormat})),
								 ('milliyet.com.tr','http://www.milliyet.com.tr/Yazar.aspx?aType=Yazarlar', ('/ydetay/',), ('secure.milliyet.com.tr',), ({'date':todayPointFormat},{'detSpan':todayTrFormat}, {'detSpan2':todayTrFormat}), {'|':2}),
								 #('radikal.com.tr', 'http://www.radikal.com.tr/yazarlar', ('/yazarlar/',), ('/rss/','/spor/'), ({'date':todaySlashFormat},), {'-':1}),
								 ('haber7.com', 'http://www.haber7.com', ('/yazarlar/',), (), ({'info readInfo':todayTrFormat},)),
								 #('zaman.com.tr', 'http://www.zaman.com.tr/yazarlar', ('_',), ('yorum_', 'haber_', 'spor_', 'kultur_', 'gundem_', 'ekonomi_', 'dunya_', 'aile-saglik_', 'egitim_', 'wetransfer.'), ({'detayTarih':todayTrNonZeroFormat},)),										  
								 ('gazetevatan.com', 'http://www.gazetevatan.com/yazarlar/', ('-yazar-yazisi-',), (), ({'cdate':todayTrFormat},), {'|':1}),
								 ('sozcu.com.tr', 'http://www.sozcu.com.tr/kategori/yazarlar/', ('/yazarlar/',), (), ({'news-content-date _flex _aic':todayTrFormatSpecial2},)),
								 ('star.com.tr', 'http://www.star.com.tr/yazarlar/', ('/yazar/',), (), ({'date2':todayTrFormat},), {'-': 2}),
								 ('sabah.com.tr', 'http://www.sabah.com.tr/Yazarlar', (today,), ('/gundem/','/ekonomi/', '/yasam/', '/dunya/', '/piyasa/', '/teknoloji/', '/egitim/', '/kultur_sanat/', '/sinema/', '/turizm/', '/fotohaber/', '/Turizm/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/otomobil/'), (1), {'-':2}),
								 ('cumhuriyet.com.tr', 'http://www.cumhuriyet.com.tr/yazarlar', ('/koseyazisi/',), (), ({'publish-date':todayTrFormat},)),
								 ('t24.com.tr', 'http://t24.com.tr/yazarlar', ('/yazarlar/', ), (), ({'datePublished':todayTrFormat},)),
								 ('taraf.com.tr', 'http://www.taraf.com.tr/yazarlar/', ('-',), ('/page/','/kategori/',), ({'post-meta':todayTrNonZeroFormat},), {'-':2}),
								 ('yenisafak.com.tr', 'http://www.yenisafak.com.tr/yazarlar/', ('/yazarlar/',), (), ({'info':todayTrFormatSpecial3},), {'|':1}),										 
								 ('yeniakit.com.tr', 'http://www.yeniakit.com.tr/yazarlar', ('/yazarlar/',), (), ({'datePublished':todayTrFormat},)),	
 								 ('bugun.com.tr', 'http://www.bugun.com.tr/yazarlar', ('-yazisi-',), (), ({'yazarDateString':todayTrFormat},)),
								#Dinamik uretiliyor haber ondan alinamadi 
								#('hurriyet.com.tr', 'http://www.hurriyet.com.tr/yazarlar/', ('/yazar/',), (), ({'hsaalih-date':todayPointFormat},)),
								
								],
			}
		
		return newsSources

from datetime import datetime	
createNewsSourceByPresent(datetime.now())
