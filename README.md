# haberbus
Haberbüs, Türkçe haber sitelerinden haberleri toplamak için kullanılan bir parser sistemidir.
Bir haber bağlantısından title, description ve imageLink çekilip bugün yayımlananlar DB'e kaydedilir.
Site: [www.haberbus.com](http://www.haberbus.com)

Temel olarak şu şekilde çalışmaktadır.
- Ana parser, kaynak listesinde (config/sources.yaml) tanımlı olan 5 kategori altındaki yaklaşık 50 bağlantıyı Parser.py script'ine hiç bir parametre verilmez ise sırayla gezer.
- Her haber sitesinin kendine özel keyword'ları yine config/sources.yaml içinde tanımlıdır. Ve bu keyword'lar ile bağlantıları toplayıp, DB'e kaydetmeye başlar.

Yaklaşık tekil olarak 50 kaynak config/sources.yaml'da tanımlıdır. (haberbus.com sitesi aktif oldugu icin bu kisim surekli gunceldir)
![Kaynak Listesi](/screenshots/sourcelist.png)

![Günlük Toplama sonucu örnek istatisikler](/screenshots/statistics.png)

![Parser Çıktısı](/screenshots/parseroutput.png)

## Kurulum İçin Gerekenler

- Python 3.x 
	- mysql.connector
	- bs4
	- requests
	- yaml
* Mysql Database

Bunlar sağlandıktan sonra, yapılması gereken, MySql üzerinde bir db oluşturmak ve
user, password, dbName bilgilerini DbHandler.py dosyamıza girmek. Ve her şey hazır.

Test için: `python Parser.py teknoloji webrazzi.com` komutu ile sadece bu kategori ve bu domain için linkleri toplayabilirsiniz.
Tüm sourcelist linklerini toplamak için `python Parser.py` demeniz yeterli. İlk çalşmada tüm linkler tarandığı için 30 dk'ı bulabilir.
Sonraki çalışmalarında 5 dk içerisinde tüm kaynaklar taranabilmektedir. Tabi sistemin bandwitdth ve kaynağına göre bu zamanlar değişebilmektedir.
