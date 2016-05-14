# haberbus
Haberbüs, Türk haber sitelerinden sosyal medyada en çok paylaşılan haberleri toplamak için kullanılan bir parser sistemidir.
Site: [www.haberbus.com](http://www.haberbus.com)

Temel olarak şu şekilde çalışmaktadır.
- Kaynak listesinde (sourceList.py) tanımlı olan 5 kategori altındaki 50 link'i mainParseSources.py script'ine hiç bir parametre verilmez ise teker teker gezer.
- Her haber sitesinin kendine özel keyword'ları yine sourceList.py içinde tanımlıdır. Ve bu keyword'lar ile link'leri toplayama başlar.
- Topladığı her link için facebook, google ve twitter'ın api'lerini kullanarak paylaşım sayılarını alır.
- Tüm linkleri paylaşım sırasına göre büyükten küçüğe sıralayarak ilk 100 link'i alıp tabloya kaydeder.
- Bu şekilde sürekli çalışarak, hem önceden alınan linklerin paylaşım oranları güncellenir hem de yeni linkler sürekli alınmaya devam edilir.

Yaklaşık tekil olarak 50 kaynak sourcelist'de tanımlıdır.
![Kaynak Listesi](/screenshots/sourcelist.png)

![Günlük Toplama sonucu örnek istatisikler](/screenshots/statistics.png)

![Parser Çıktısı](/screenshots/parser.png)

## Kurulum İçin Gerekenler

- Python 2.x (2.6 ve üstü)
	- MySQLdb
	- BeautifulSoup
	- simplejson
* Mysql Database

Bunlar sağlandıktan sonra yapılması gereken ServerDatabaseHandler.py
dosyamızı mysql db'imize ve oluşturduğumuz database'e göre editlemek ve
her şey hazır.

Test için: `python mainParseSources.py teknoloji webrazzi.com` sadece bu kategori bu link taranır.

Tüm kaynakları taramak için: `python mainParseSources.py` komutu ile ekran görüntüsündeki gibi haber sitelerinden
dataları toplayama başlayabiliriz. Gerekli tüm tabları bu scrit �al�ştığında üretilmektedir
