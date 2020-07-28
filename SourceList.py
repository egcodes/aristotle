# -*- coding: utf-8 -*-
from datetime import datetime

def createNewsSource(present):
		months = {
			'01':'Ocak',
			  '02':'Şubat',
			  '03':'Mart',
			  '04':'Nisan',
			  '05':'Mayıs',
			  '06':'Haziran',
			  '07':'Temmuz',
			  '08':'Ağustos',
			  '09':'Eylül',
			  '10':'Ekim',
			  '11':'Kasım',
			  '12':'Aralık'
		  }

		dateFormats = {
			"slash": str(present.strftime('%Y/%m/%d')),
			"nosep": str(present.strftime('%Y%m%d')),
			"dash": str(present.strftime('%Y-%m-%d')),
			"dot": str(present.strftime('%d.%m.%Y')),
			"empty": str(present.strftime('%d %m %Y')),
			"empty_sub": str(present.strftime('%#d %m %Y')),
			"turkish": str(present.strftime('%d')) + ' ' +
					   		months[str(present.strftime('%m'))] + ' ' +
					   		str(present.strftime('%Y')),
			"turkish_sub": str(present.strftime('%#d')) + ' ' +
							months[str(present.strftime('%m'))] + ' ' +
					   		str(present.strftime('%Y')),
			"slash_reverse": str(present.strftime('%d/%m/%Y')),
			"dash_reverse": str(present.strftime('%d-%m-%Y')),
			"dot_reverse": str(present.strftime('%d.%m.%Y')),
		}

		#Haber kaynakları
		# Kaynak parametreleri sırası ile
			# Kaynak adi
			# Kaynak adresi
			# Kaynak haberinin linkinde olmasi gerekenler
			# Kaynak haberin linkinde olmaması gerekenler
			# Bugun tarihi icin ayirac 0, 1, 2 turleri var
			# Title sonlarinda gazete ismi silmek icin -> {karakter:sayisi verildidinde sola dogru siler}
			# Sadece silinecek kelime(ler) ve 1 verilerek o yazi silinir

		newsSources = {
				'gundem':
					[
						('sozcu.com.tr', 'http://www.sozcu.com.tr', ('/gundem/', '/gunun-icinden/', '/dunya/', '/ekonomi/', '/egitim/', '/saglik/',), ('spor_', 'video.', ), ({'date-time': dateFormats["empty_sub"]},)),

						('t24.com.tr', 'http://t24.com.tr', ('/haber/',), (), ({'_392lz': dateFormats["empty"]},)),

						('milliyet.com.tr','http://www.milliyet.com.tr', ('-',), ('secure.milliyet.com.tr','/ydetay/', 'skorer.'),({'date': dateFormats["dot_reverse"]},), {'-':1}),

						('hurriyet.com.tr', 'http://www.hurriyet.com.tr', ('-',), ('-haberleri',), ({'rhd-time-box-text hidden-sm-down': dateFormats["dot_reverse"]},)),

						('haber7.com', 'http://www.haber7.com', ('/haber/',), ('/teknoloji/', 'spor.','/yazarlar/'), ({'date-item added': dateFormats["dot_reverse"]}, )),

						('odatv.com', 'http://www.odatv.com', ('-',), (), ({'yaziboyut': dateFormats["dot_reverse"]},)),

						('haberturk.com','https://www.haberturk.com', ('-',), ('/yazarlar/', '/fiskos/', '/video/', '/teknoloji/', '/spor/', '/kultur-sanat/','spor.', 'magazin.',), ({'date': dateFormats["dot_reverse"]},), {'|':1}),

						('gazetevatan.com', 'http://www.gazetevatan.com', ('-gundem', '-dunya', '-siyaset', '-ekonomi', '-finas', '-yasam', '-egitim',), (), ({'cdate': dateFormats["empty"]},{'datesrc': dateFormats["empty"]}), {'|':1},),

						('ntv.com.tr', 'http://www.ntv.com.tr', ('/turkiye/','/dunya/', '/ekonomi/', '/saglik/','/yasam/', '/egitim/',), (), ({'news-info-text': dateFormats["dot_reverse"]},), ),

						('cnnturk.com', 'http://www.cnnturk.com', ('/ekonomi/', '/turkiye/', '/dunya/', '/yasam/',  ), (), ({'detail-metadata': dateFormats["dot_reverse"]},), {'-':1}),

						('ensonhaber.com', 'http://www.ensonhaber.com', ('/gundem/',), (),({'c-date': dateFormats["dot_reverse"]},)),

						('birgun.net', 'https://www.birgun.net', ('/haber/',), (),({'category-line': dateFormats["dot_reverse"]},)),

						('sol.org.tr', 'http://sol.org.tr/bugun', ('/haber/',), (), ({'datetime': dateFormats["dot_reverse"]},), {'|':2},),

						('trthaber.com', 'http://www.trthaber.com', ('/gundem/', '/turkiye/', '/dunya/', '/ekonomi/', '/egitim/',), (), ({'detTarih': dateFormats["empty_sub"]},)),

						('star.com.tr', 'http://www.star.com.tr/default.asp', ('/guncel/', '/politika/', '/ekonomi/', '/dunya/', '/medya/', '/egitim/',), (), ({'time color-gray-medium margin-bottom-lg': dateFormats["empty"]},), {'|':1}),

						('internethaber.com', 'https://www.internethaber.com', ('.htm',), ('gazeteoku.com', 'otomobil.internethaber.com', 'spor.', ), ({'ml-auto':'%s'%dateFormats["dot_reverse"]},{'info':'Tarihi :%s'%dateFormats["dash_reverse"]})),

						('mynet.com', 'https://www.mynet.com', ('/haber/',), ('/teknoloji/','spor.',), ({'post-date col-auto': dateFormats["dot_reverse"]},)),

						('cumhuriyet.com.tr', 'https://www.cumhuriyet.com.tr', ('/haber/',), (), ({'datePublished': dateFormats["dash"]},)),

						('yenisafak.com', 'http://www.yenisafak.com', ('/dunya/', '/gundem/', '/politika/', '/ekonomi/', '/saglik/', '/egitim/',), ('/yazarlar/', '/spor/', '/teknoloji/',), ({'item time': dateFormats["empty"]},), {'-':1}),

						('haberler.com', 'http://www.haberler.com', ('-haberi',), ('fotogaleri.','futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({'hbptDate': dateFormats["dot_reverse"]},)),

						('diken.com.tr', 'http://www.diken.com.tr', ('-',), ('/kategori/', 'bu-gazete/', '-ekim-', '-kasim-', '-aralik-', '-ocak-', '-subat-', '-mart-', '-nisan-', '-mayis-', '-haziran-', '-temmuz-', '-agustos-', '-eylul-',), ({'entry-time': dateFormats["slash_reverse"]},), {'-':1}),

						('tr.sputniknews.com', 'http://tr.sputniknews.com', (dateFormats["nosep"],), ('/spor/', '/bilim/',), (1),),

						('bbc.co.uk/turkce', 'http://www.bbc.co.uk/turkce',  ('haberler-',), (), ({'mini-info-list__item': dateFormats["empty_sub"]},), {'-':1}),

						#('yeniakit.com.tr', 'http://www.yeniakit.com.tr/gundem', ('/haber/',), ('futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({"date": dateFormats["empty"]},)),

						#('sabah.com.tr', 'http://www.sabah.com.tr', (dateFormats["slash"]), ('/yazarlar/', '/teknoloji/', '/kultur_sanat/', '/sinema/', '/fotohaber/', '/magazin/', '/multimedya/', '/spor/', '/spor-haberleri/', '/webtv/', '/otomobil/', '/eGazete/',), (1), {'-':1}),

						#('aksam.com.tr', 'http://www.aksam.com.tr', ('/siyaset/', '/guncel/', '/yasam/', '/ekonomi/', '/dunya/',), ('/teknoloji/', '/spor/', '/magazin/', '/yazarlar/',), ({'newsDate': dateFormats["empty"]},), {'-':1}),

						#('takvim.com.tr', 'http://www.takvim.com.tr', (dateFormats["slash"]), ('/Yazarlar/', '/yazarlar/', '/spor/', '/Spor/', '/Televizyon', '/multimedya/', '/Saklambac/', '/saklambac/'), (1),),

						#('posta.com.tr', 'http://www.posta.com.tr', ('-',), ('futbol','Fenerbahce', 'Galatasaray', 'Besiktas', 'Trabzonspor', 'fenerbahce', 'besiktas', 'galatasaray', 'trabzonspor'), ({'news-detail__info__date__item': dateFormats["empty"]},), {'-':1},),

						#('turkiyegazetesi.com.tr', 'http://www.turkiyegazetesi.com.tr', ('/gundem/','/dunya/', '/egitim/', '/yasam/', '/saglik/', '/politika/', '/ekonomi/', ), ('/spor/','/teknoloji/', '/yazarlar/',), ({'story_date clearfix': dateFormats["dot_reverse"]},),),
					],

				'videohaber':
					[
						('hurriyet.com.tr', 'http://www.hurriyet.com.tr/video/', ('/video/',), ('/playlist/',), ({'date': dateFormats["dot_reverse"]}, )),

						('cnnturk.com', 'http://www.cnnturk.com/video', ('/video/',), (), ({'detail-metadata hidden-xs hidden-sm': dateFormats["dot_reverse"]},), {'-':1}),

						('ensonhaber.com', 'http://videonuz.ensonhaber.com', ('/izle/',), (), ({'timeInfo': dateFormats["dash"]},)),

						('haber7.com', 'http://video.haber7.com/', ('/video-galeri/',), (), ({'description': dateFormats["dot_reverse"]},)),

						('trthaber.com', 'http://www.trthaber.com/video-galerileri.html', ('/videolar/',), ('/videolar/ekonomi','/videolar/kultur-sanat', '/videolar/yasam', '/videolar/spor', '/videolar/gundem', '/videolar/magazin', '/videolar/cevre', '/videolar/dunya', '/videolar/medya', '/videolar/saglik', '/videolar/egitim', '/videolar/turkiye', '/videolar/bilim-teknik' ), ({'detTarih': dateFormats["dash"]},)),

						('milliyet.com.tr', 'https://www.milliyet.com.tr/milliyet-tv/', ('-',), (), ({'date': dateFormats["dash"]},)),

						('ntv.com.tr', 'http://www.ntv.com.tr/video', ('/video/',), (), ({'clock': dateFormats["dot_reverse"]},)),

						('haberturk.com','http://www.haberturk.com/video/haber', ('/haber/',), (), ({'mb10': dateFormats["empty"]},)),
					],

				'teknoloji':
					[
						('chip.com.tr', 'http://www.chip.com.tr', ('/haber/', '/makale/','/blog/','/inceleme/'), (), ({'datePublished': dateFormats["empty"]},)),

						('webrazzi.com', 'https://webrazzi.com', (dateFormats["slash"]), (), (1), {'|':1}),

						('shiftdelete.net', 'https://shiftdelete.net', ('-',), ('forum.',), ({'article:published_time': dateFormats["dash"]},), {'-':1}),

						('ntv.com.tr', 'http://www.ntv.com.tr/teknoloji', ('/teknoloji/',), (),({'news-info-text': dateFormats["dot_reverse"]},),),

						('teknolojioku.com', 'http://www.teknolojioku.com', ('-',), (),({'time': dateFormats["slash_reverse"]},) ),

						('mynet.com', 'http://www.mynet.com/teknoloji-haberler', ('-',), (), ({'post-date col-auto': dateFormats["dot_reverse"]},)),

						('bigumigu.com', 'http://www.bigumigu.com', ('/haber/',), (), ({'updated':'%s'%dateFormats["dot_reverse"]},)),

						('webtekno.com', 'http://www.webtekno.com', ('.html',), (), ({'content-info__date':"önce"},), ),

						('fizikist.com', 'http://www.fizikist.com', ('-',), (), ({'content_time': dateFormats["empty"]},), {'-':1}),

						('bilimpro.com', 'https://bilimpro.com', (dateFormats["slash"],), (), (1),),

						('log.com.tr', 'http://www.log.com.tr', ('-',), (), ({'date': dateFormats["empty"]},), {'-':1}),
					],

				'kulturvesanat':
					[
						('haberturk.com','https://www.haberturk.com/kultur-sanat', ('-',), (), ({'date': dateFormats["dot_reverse"]},), {'|':1}),

						('hurriyet.com.tr', 'https://www.hurriyet.com.tr/keyif', ('-',), (), ({'rhd-time-box-text ': dateFormats["dot_reverse"]},)),

						('cnnturk.com', 'https://www.cnnturk.com/kultur-sanat-haberleri', ('/kultur-sanat/', ), (), ({'modified-date': dateFormats["dash"]},),  {'-':1}),

						('ntv.com.tr', 'https://www.ntv.com.tr/sanat', ('-',), (),({'news-info-update': dateFormats["dot_reverse"]},),),

						('trthaber.com', 'https://www.trthaber.com/haber/kultur-sanat/', ('/kultur-sanat/', ), (), ({'detTarih': dateFormats["empty_sub"]},)),

						('sozcu.com', 'https://www.sozcu.com.tr/hayatim/kultur-sanat-haberleri/', ('/kultur-sanat-haberleri/', ), (), ({'news-date': dateFormats["empty_sub"]},)),
					],

				'spor':
					[
						('fanatik.com.tr', 'http://www.fanatik.com.tr', ('-',), (), ({'news-detail__info__date__item': dateFormats["empty"]},),),

						('ntvspor.net', 'https://www.ntvspor.net', ('-',), (), ({'time': dateFormats["empty_sub"]},),),

						('skor.sozcu.com.tr', 'http://skor.sozcu.com.tr', (dateFormats["slash"]), (), (1), {'-':1}),

						('sporx.com', 'http://www.sporx.com/?giris=ok', ('-',), (), ({'haberdate': dateFormats["empty"]},)),

						('mackolik.com', 'http://www.mackolik.com/default.aspx', ('/Haber/',), (), ({'datePublished': dateFormats["dash"]},)),

						('cnnturk.com', 'http://www.cnnturk.com/spor', ('/spor/', ), (), ({'detail-metadata': dateFormats["dot_reverse"]},),),

						('fotomac.com.tr', 'https://www.fotomac.com.tr', (dateFormats["slash"]), ('/Yazarlar/',), (1), {'–':2}),
					],

				'koseyazilari':
					[
						('haberturk.com','http://www.haberturk.com/htyazarlar', ('/yazarlar/',), (), ({'date': dateFormats["dot_reverse"]},), {'-':1}),

						('milliyet.com.tr','http://www.milliyet.com.tr/yazarlar/', ('/yazarlar/',), (), ({'article__date': dateFormats["empty"]},), {'|':2}),

						('haber7.com', 'http://www.haber7.com', ('/yazarlar/',), (), ({'readInfo': dateFormats["dot_reverse"]},)),

						('sozcu.com.tr', 'http://www.sozcu.com.tr/kategori/yazarlar/', ('/yazarlar/',), (), ({'date': dateFormats["empty_sub"]},)),

						('star.com.tr', 'http://www.star.com.tr/yazarlar/', ('/yazar/',), (), ({'date font-weight-7 font-size-17': dateFormats["empty"]},), {'-': 2}),

						('sabah.com.tr', 'http://www.sabah.com.tr/yazarlar', (dateFormats["slash"]), ('/gundem/','/ekonomi/', '/yasam/', '/dunya/', '/piyasa/', '/teknoloji/', '/egitim/', '/kultur_sanat/', '/sinema/', '/turizm/', '/fotohaber/', '/Turizm/', '/magazin/', '/multimedya/', '/spor/', '/webtv/', '/otomobil/'), (1), {'-':2}),

						('cumhuriyet.com.tr', 'http://www.cumhuriyet.com.tr/yazarlar', ('/yazarlar/',), (), ({'yayin-tarihi': dateFormats["empty"]},)),

						('t24.com.tr', 'http://t24.com.tr/son-yazilar', ('/yazarlar/', ), (), ({'_392lz': dateFormats["empty"]},)),

						('hurriyet.com.tr', 'http://www.hurriyet.com.tr/yazarlar/', ('/yazarlar/',), (), ({'article-date': dateFormats["empty_sub"]},)),

						#('yenisafak.com', 'http://www.yenisafak.com/Yazarlar', ('/yazarlar/',), (), ({'author-share': dateFormats["empty"]},), {'|':1}),

						#('yeniakit.com.tr', 'http://www.yeniakit.com.tr/yazarlar', ('/yazarlar/',), (), ({'inside': dateFormats["empty"]},)),

						#('gazetevatan.com', 'http://www.gazetevatan.com/yazarlar/', ('-yazar-yazisi-',), (), ({'cdate': dateFormats["empty"]},), {'|':1}),
					],
			}

		return newsSources


createNewsSource(datetime.now())
