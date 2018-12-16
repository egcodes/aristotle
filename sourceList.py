# -*- coding: utf-8 -*-

def createNewsSourceByPresent(present):
		months = {'01':'Ocak', '02':'Şubat', '03':'Mart', '04':'Nisan', '05':'Mayıs', '06':'Haziran', '07':'Temmuz', '08':'Ağustos', '09':'Eylül', '10':'Ekim', '11':'Kasım', '12':'Aralık'}
		monthsUpper = {'01':'OCAK', '02':'ŞUBAT', '03':'MART', '04':'NİSAN', '05':'MAYIS', '06':'HAZİRAN', '07':'TEMMUZ', '08':'AĞUSTOS', '09':'EYLÜL', '10':'EKİM', '11':'KASIM', '12':'ARALIK'}
		monthsShort = {'01':'Oca', '02':'Şub', '03':'Mar', '04':'Nis', '05':'May', '06':'Haz', '07':'Tem', '08':'Ağu', '09':'Eyl', '10':'Eki', '11':'Kas', '12':'Ara'}
		
		monthEng = {'Haziran':'June', 'Temmuz':'July', 'Ağustos':'August', 'Mart':'March', 'Nisan':'April', 'Mayıs':'May',  'Eylül':'September', 'Ekim':'October', 'Kasım':'November', 'Aralık':'December', 'Ocak':'January', 'Şubat':'February'}

		today = str(present.strftime('%Y/%m/%d'))
		todayCombine = str(present.strftime('%Y%m%d'))
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
		todayTrFormatSpecial4 = str(present.strftime('%M %d, %Y'))

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
									('sozcu.com.tr', 'http://www.sozcu.com.tr', ('/gundem/', '/gunun-icinden/', '/dunya/', '/ekonomi/', '/egitim/', '/saglik/',), ('spor_', 'video.', ), ({'date':todayTrNonZeroFormat},)),
									#('yeniakit.com.tr', 'http://www.yeniakit.com.tr/gundem', ('/haber/',), ('futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({"date":todayTrFormat},)),	
									('t24.com.tr', 'http://t24.com.tr', ('/haber/', '/gundem/','/politika/', '/egitim/', '/yasam/', '/ekonomi/', '/dunya/', ), (), ({'story-date':todayTrFormat},)),
									('milliyet.com.tr','http://www.milliyet.com.tr', ('-',), ('secure.milliyet.com.tr','/ydetay/', 'skorer.'),({'date':todayPointFormat},), {'-':1}),
									('hurriyet.com.tr', 'http://www.hurriyet.com.tr', ('-',), ('-haberleri',), ({'rhd-time-box-text hidden-sm-down':todayPointFormat},)),
									('haber7.com', 'http://www.haber7.com', ('/haber/',), ('/teknoloji/', 'spor.','/yazarlar/'), ({'date-item added':todayPointFormat}, )),
									('odatv.com', 'http://www.odatv.com', ('-',), (), ({'yaziboyut':todayPointFormat},)),
									('haberturk.com','http://www.haberturk.com', ('-',), ('/yazarlar/', '/fiskos/', '/video/', '/teknoloji/', '/spor/', '/kultur-sanat/','spor.', 'magazin.',), ({'news-detail-featured-date':todayTrFormat},), {'|':1}),
									('gazetevatan.com', 'http://www.gazetevatan.com', ('-gundem', '-dunya', '-siyaset', '-ekonomi', '-finas', '-yasam', '-egitim',), (), ({'cdate':todayTrFormat},{'datesrc':todayTrFormat}), {'|':1},),
									('ntv.com.tr', 'http://www.ntv.com.tr', ('/turkiye/','/dunya/', '/ekonomi/', '/saglik/','/yasam/', '/egitim/',), (), ({'desktop-only':todayPointFormat},), ),
									('cnnturk.com', 'http://www.cnnturk.com', ('/ekonomi/', '/turkiye/', '/dunya/', '/yasam/',  ), (), ({'detail-metadata':todayPointFormat},), {'-':1}),
									('ensonhaber.com', 'http://www.ensonhaber.com', ('.html',), ('kralspor.',),({'margin-right:15px;margin-bottom:10px;':todayPointFormat},)),
									('birgun.net', 'http://www.birgun.net', ('/haber-detay/',), (),({'date':todayPointFormat},)),
									('haber.sol.org.tr', 'http://haber.sol.org.tr/anasayfa', ('/turkiye/','/emek-sermaye/', '/dunya/', '/toplum/', '/medya/',), (), ({'date-display-single':todayTrFormat},), {'|':2},),
									('trthaber.com', 'http://www.trthaber.com', ('/gundem/', '/turkiye/', '/dunya/', '/ekonomi/', '/egitim/',), (), ({'detTarih':todayTrFormat},)),
									('posta.com.tr', 'http://www.posta.com.tr', ('-',), ('futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({'news-detail__info__date__item':todayTrFormat},), {'-':1},),										
									('star.com.tr', 'http://www.star.com.tr/default.asp', ('/guncel/', '/politika/', '/ekonomi/', '/dunya/', '/medya/', '/egitim/',), (), ({'newsDate':todayPointFormat},), {'-':1}),
									('internethaber.com', 'http://www.internethaber.com', ('.htm',), ('gazeteoku.com', 'otomobil.internethaber.com', 'spor.', ), ({'rpt':'%s'%todayLineFormat},{'info':'Tarihi :%s'%todayLineFormat})),
									('mynet.com', 'http://www.mynet.com', ('/haber/',), ('/teknoloji/','spor.',), ({'post-date col-auto':todayTrNonZeroFormat},)),
									('cumhuriyet.com.tr', 'http://www.cumhuriyet.com.tr', ('/siyaset/','/turkiye/', '/dunya/', '/ekonomi/','/yasam/', '/egitim/', '/saglik/',), (), ({'publish-date':todayTrFormat},)),
									('yenisafak.com', 'http://www.yenisafak.com', ('/dunya/', '/gundem/', '/politika/', '/ekonomi/', '/saglik/', '/egitim/',), ('/yazarlar/', '/spor/', '/teknoloji/',), ({'item time':todayTrFormat},), {'-':1}),										 
									#('takvim.com.tr', 'http://www.takvim.com.tr', (today,), ('/Yazarlar/', '/yazarlar/', '/spor/', '/Spor/', '/Televizyon', '/multimedya/', '/Saklambac/', '/saklambac/'), (1),),
									('haberler.com', 'http://www.haberler.com', ('-haberi',), ('fotogaleri.','futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({'nav1':todayTrNonZeroFormat},)),
									('diken.com.tr', 'http://www.diken.com.tr', ('-',), ('/kategori/', 'bu-gazete/', '-ekim-', '-kasim-', '-aralik-', '-ocak-', '-subat-', '-mart-', '-nisan-', '-mayis-', '-haziran-', '-temmuz-', '-agustos-', '-eylul-',), ({'entry-time':todaySlashFormat},), {'-':1}),
									#('sabah.com.tr', 'http://www.sabah.com.tr', (today,), ('/yazarlar/', '/teknoloji/', '/kultur_sanat/', '/sinema/', '/fotohaber/', '/magazin/', '/multimedya/', '/spor/', '/spor-haberleri/', '/webtv/', '/otomobil/', '/eGazete/',), (1), {'-':1}),
									('tr.sputniknews.com', 'http://tr.sputniknews.com', (todayCombine,), ('/spor/', '/bilim/',), (1),),
									('aksam.com.tr', 'http://www.aksam.com.tr', ('/siyaset/', '/guncel/', '/yasam/', '/ekonomi/', '/dunya/',), ('/teknoloji/', '/spor/', '/magazin/', '/yazarlar/',), ({'newsDate':todayTrFormat},), {'-':1}),
									('bbc.co.uk/turkce', 'http://www.bbc.co.uk/turkce',  ('haberler-',), (), ({'mini-info-list__item': todayTrNonZeroFormat},), {'-':1}),
									#Resimleri gosterilmiyor
									#('turkiyegazetesi.com.tr', 'http://www.turkiyegazetesi.com.tr', ('/gundem/','/dunya/', '/egitim/', '/yasam/', '/saglik/', '/politika/', '/ekonomi/', ), ('/spor/','/teknoloji/', '/yazarlar/',), ({'story_date clearfix':todayPointFormat},),),										
								],
			
				'videohaber': 	[
									('hurriyet.com.tr', 'http://www.hurriyet.com.tr/video/', ('/video/',), ('/playlist/',), ({'date':todayPointFormat}, )),
									('cnnturk.com', 'http://www.cnnturk.com/video', ('/video/',), (), ({'detail-metadata hidden-xs hidden-sm':todayPointFormat},), {'-':1}),
									('ensonhaber.com', 'http://videonuz.ensonhaber.com', ('/izle/',), (), ({'timeInfo':todayFirstYear},)),
									('haber7.com', 'http://video.haber7.com/', ('/video-galeri/',), (), ({'description':todayPointFormat},)),
									('trthaber.com', 'http://www.trthaber.com/video-galerileri.html', ('/videolar/',), ('/videolar/ekonomi','/videolar/kultur-sanat', '/videolar/yasam', '/videolar/spor', '/videolar/gundem', '/videolar/magazin', '/videolar/cevre', '/videolar/dunya', '/videolar/medya', '/videolar/saglik', '/videolar/egitim', '/videolar/turkiye', '/videolar/bilim-teknik' ), ({'balonIc_bilgi':todayPointFormat},)),
									('milliyet.com.tr', 'http://www.milliyet.com.tr/Milliyet-Tv/', ('video-izle',), ('canli-yayin-videosu',), ({'detSpan':todayTrFormat},)), 
									('ntv.com.tr', 'http://www.ntv.com.tr/video', ('/video/',), (), ({'clock':todayPointFormat},)),
									('haberturk.com','http://www.haberturk.com/video/haber', ('/haber/',), (), ({'mb10':todayTrFormat},)),
								],
			
				'teknoloji':	[
									('chip.com.tr', 'http://www.chip.com.tr', ('/haber/', '/makale/','/blog/','/inceleme/'), (), ({'datePublished':todayTrFormat},)),
									('donanimhaber.com', 'http://www.donanimhaber.com', ('/haberleri/',), ('forum.donanimhaber.com','/2si1/','/mesut-cevik-ile-canli/',), ({'tarih post-date':todayTrNonZeroFormat},)),
									('webrazzi.com', 'https://webrazzi.com', (today,), (), (1), {'|':1}),
									('shiftdelete.net', 'http://shiftdelete.net', ('-',), ('forum.',), ({'font-size:14px;color:#888':"önce"},), {'-':1}),
									('ntv.com.tr', 'http://www.ntv.com.tr/teknoloji', ('/teknoloji/',), (),({'desktop-only':todayPointFormat},),),
									('teknokulis.com', 'http://www.teknokulis.com', (today,), ('teknokulis.com/Haberler/%s'%today,), (1), {'-':4}),
									('teknolojioku.com', 'http://www.teknolojioku.com', ('-',), (),({'time':todaySlashFormat},) ),
									('mynet.com', 'http://www.mynet.com/teknoloji', ('/teknoloji/',), (), ({'newsInfo':todayTrNonZeroFormat},)),
									('bigumigu.com', 'http://www.bigumigu.com', ('/haber/',), (), ({'article:published_time':'%s'%todayFirstYear},)),
									('sosyalmedya.co', 'http://www.sosyalmedya.co', ("-",), ('/sosyal-medya', '/sosyal-marka', '/yeni-girisimler', '/e-ticaret',), ({'article:published_time':'%s'%todayFirstYear},), {'Sosyal Medya':1}),
									#('silikonvadisi.tv', 'http://www.silikonvadisi.tv', ('.html',), ('sicak-haber',), ({'entry-date updated td-module-date':todayTrNonZeroFormat},), {'-':1}),
									('webtekno.com', 'http://www.webtekno.com', ('.html',), (), ({'content-info__date':"önce"},), ),
 									('fizikist.com', 'http://www.fizikist.com', ('-',), (), ({'content_time':todayTrFormat},), {'-':1}),
									('bilimpro.com', 'https://bilimpro.com', (todaySlashFormatReverse,), (), (1),),
 									('log.com.tr', 'http://www.log.com.tr', ('-',), (), ({'date':todayTrFormat},), {'-':1}),
 									('dunyahalleri.com', 'https://www.dunyahalleri.com', ('-',), (), ({'article:published_time':'%s'%todayFirstYear},), {'-':1}),
								],
			
				'kulturvesanat':
								[
									('haberturk.com','http://www.haberturk.com/kultur-sanat', ('-',), (), ({'date':todayTrFormat},), {'|':1}),
									('hurriyet.com.tr', 'http://www.hurriyet.com.tr/keyif', ('-',), (), ({'col-md-7 col-xs-12 text-right small-date':todayPointFormat},)),
									('cnnturk.com', 'http://www.cnnturk.com/kultur-sanat', ('/kultur-sanat/', ), (), ({'detail-metadata':todayPointFormat},),  {'-':1}),
									('ntv.com.tr', 'http://www.ntv.com.tr/sanat', ('/sanat/',), (),({'time':todayTrNonZeroFormat},),),
									('haber7.com', 'http://www.haber7.com/kultur', ('/kultur/', '/kulturel-etkinlikler/', '/mimari/', '/muzik/', '/arkeoloji/', '/sinema/', '/tarih-ve-fikir/', '/edebiyat/', '/fotograf/', '/plastik-sanatlar/', 'tiyatro-ve-sahne-sanatlari',), (), ({'info':todayPointFormat}, )),
									#('sabah.com.tr', 'http://www.sabah.com.tr/kultur_sanat', (today,), ('/gundem/','/ekonomi/', '/yasam/', '/dunya/', '/piyasa/', '/teknoloji/', '/egitim/', '/turizm/', '/fotohaber/', '/Turizm/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/yazarlar/', '/otomobil/'), (1), {'-':1}),
									('trthaber.com', 'http://www.trthaber.com/haber/kultur-sanat/', ('/kultur-sanat/', ), (), ({'detTarih':todayTrFormat},)),
									('sozcu.com', 'http://www.sozcu.com.tr/hayatim/kultur-sanat-haberleri/', ('/kultur-sanat-haberleri/', ), (), ({'news-date':todayTrFormat},)),


								],
			
				'spor':			[
									('fanatik.com.tr', 'http://www.fanatik.com.tr', (today,), ('KategoriSayfasi','AnketmerkeziTumYorumlar',"tum-yorumlar",), (1), {'-':1}),
									('ntvspor.net', 'http://www.ntvspor.net', ('-',), (), ({'time':todayTrNonZeroFormat},),),
									('skor.sozcu.com.tr', 'http://skor.sozcu.com.tr', (today,), (), (1), {'-':1}),
									('sporx.com', 'http://www.sporx.com/?giris=ok', ('-',), (), ({'haberdate':todayTrFormat},)),
									('mackolik.com', 'http://www.mackolik.com/default.aspx', ('/Haber/',), (), ({'datePublished':todayFirstYear},)),
									('cnnturk.com', 'http://www.cnnturk.com/spor', ('/spor/', ), (), ({'detail-metadata':todayPointFormat},),),
									#('fotomac.com.tr', 'http://www.fotomac.com.tr', (today,), ('/Yazarlar/',), (1), {'–':2}),
								],
				
				'koseyazilari': [
									('haberturk.com','http://www.haberturk.com/htyazarlar', ('/yazarlar/',), (), ({'author-detail-content':todayTrFormat},), {'-':1}),
									('milliyet.com.tr','http://www.milliyet.com.tr/yazarlar/', ('/yazarlar/',), (), ({'nn1':todayPointFormat},), {'|':2}),
									('haber7.com', 'http://www.haber7.com', ('/yazarlar/',), (), ({'info':todayPointFormat},)),
									('sozcu.com.tr', 'http://www.sozcu.com.tr/kategori/yazarlar/', ('/yazarlar/',), (), ({'date':todayTrNonZeroFormat},)),
									('star.com.tr', 'http://www.star.com.tr/yazarlar/', ('/yazar/',), (), ({'publisheddate':todayTrFormat},), {'-': 2}),
									#('sabah.com.tr', 'http://www.sabah.com.tr/Yazarlar', (today,), ('/gundem/','/ekonomi/', '/yasam/', '/dunya/', '/piyasa/', '/teknoloji/', '/egitim/', '/kultur_sanat/', '/sinema/', '/turizm/', '/fotohaber/', '/Turizm/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/otomobil/'), (1), {'-':2}),
									('cumhuriyet.com.tr', 'http://www.cumhuriyet.com.tr/yazarlar', ('/koseyazisi/',), (), ({'publish-date':todayTrFormat},)),
									('t24.com.tr', 'http://t24.com.tr/yazarlar', ('/yazarlar/', ), (), ({'datePublished':todayTrFormat},)),
	   								('hurriyet.com.tr', 'http://www.hurriyet.com.tr/yazarlar/', ('/yazarlar/',), (), ({'article-date':todayTrNonZeroFormat},)),
									# Haber tarihi split edilmis, o yuzden alinamiyor
									#('yenisafak.com', 'http://www.yenisafak.com/Yazarlar', ('/yazarlar/',), (), ({'author-share':todayTrFormat},), {'|':1}),										 
									# Haber tarihi yok 
									#('yeniakit.com.tr', 'http://www.yeniakit.com.tr/yazarlar', ('/yazarlar/',), (), ({'inside':todayTrFormat},)),	
									# Title tag var ama icerik yok
									#('gazetevatan.com', 'http://www.gazetevatan.com/yazarlar/', ('-yazar-yazisi-',), (), ({'cdate':todayTrFormat},), {'|':1}),
								],
			}
		
		return newsSources

from datetime import datetime	
createNewsSourceByPresent(datetime.now())
