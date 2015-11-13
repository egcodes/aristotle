# haberbus
Haberbüs, Türk haber sitelerinden sosyal medyada en çok paylaşılan haberleri toplamak için kullanılan bir parser sistemidir

Yaklaşık tekil olarak 50 kaynak sourcelist'de tanımlıdır.
![Kaynak Listesi](/screenshots/sourcelist.png)

![Parser Çıktısı](/screenshots/parser.png)

## Kurulum İçin Gerekenler

- Python 2.6 ve üstü
	- MySQLdb
	- BeautifulSoup
	- simplejson
* Mysql Database

Bunlar sağlandıktan sonra yapılması gereken ServerDatabaseHandler.py
dosyamızı mysql db'imize ve oluşturduğumuz database'e göre editlemek ve
her şey hazır.

`python mainParseSources.py` komutu ile ekran görüntüsündeki gibi haber sitelerinden
dataları toplayama başlayabiliriz. Gerekli tüm tablolara bu script'ler içinde üretilmektedir.
