# haberbus
Haberbüs, Türkçe haber sitelerinden haberleri toplamak için kullanılan bir parser sistemidir.
Bir haber bağlantısından title, description ve imageLink çekilip DB'e kaydedilir.
Site: [www.haberbus.com](http://www.haberbus.com)

ÖNEMLİ NOT: Bir zamanlar mevcut olan Twitter,Facebook,GooglePlus'dan alınan paylaşım oranları, bu sistemler api'lerini 
kapattığı için koddan kaldırılmıştır.
Facebook Graph Public Api yeniden eklenmiş ama aktif değildir. Sürekli request'de cevap dönmemektedir. GraphApi'de 
belirli zamanda belirli sayıda istek gönderme olayı var. Bu limitin aşılması bu kısmın 0 dönmesine sebep olur.
Sonuç olarak link'lerin paylaşım oranları şu andaki default kodda toplanmamaktadır

Temel olarak şu şekilde çalışmaktadır.
- Ana parser, kaynak listesinde (sourceList.py) tanımlı olan 5 kategori altındaki 50 link'i mainParseSources.py script'ine hiç bir parametre verilmez ise teker teker gezer.
- Her haber sitesinin kendine özel keyword'ları yine sourceList.py içinde tanımlıdır. Ve bu keyword'lar ile link'leri toplayama başlar.

Yaklaşık tekil olarak 50 kaynak sourcelist'de tanımlıdır. (haberbus.com sitesi aktif oldugu icin bu kisim surekli gunceldir)
![Kaynak Listesi](/screenshots/sourcelist.png)

![Günlük Toplama sonucu örnek istatisikler](/screenshots/statistics.png)

![Parser Çıktısı](/screenshots/parser.png)

## Kurulum İçin Gerekenler

- Python 2.x (2.6 ve üstü)
	- MySQLdb
	- BeautifulSoup
	- requests
	- simplejson
* Mysql Database

Bunlar sağlandıktan sonra yapılması gereken bir db oluşturmak MySql üzerinde ve
gerekli bilgileri ServerDatabaseHandler.py dosyamıza girmektir. Ve her şey hazır.

Test için: `python mainParseSources.py teknoloji webrazzi.com` komutu ile sadece bu kategori bu linkleri toplayabilirsiniz.
Tüm sourcelist'i gezmek için `python mainParseSources.py` demeniz yeterli. İlk sefer tüm link'ler tarandığı için 30 dk'ı bulabilir.
Sonraları için 10 dk içerisinde tüm kaynaklar taranabilmektedir. Tabi sisteminde bandwitdth ve resource'una göre bu zamanlar değişebilir.
