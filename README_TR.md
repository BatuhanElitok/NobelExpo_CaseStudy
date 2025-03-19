# Fuar Şirket Veri Scraper'ı

## Genel Bakış

Bu proje, çeşitli ticaret fuarlarındaki katılımcı listelerinden şirket bilgilerini çıkarmak için tasarlanmış bir dizi scraper içerir. Scraper'lar, farklı kaynaklardan (web siteleri, PDF'ler) ve farklı formatlardaki verileri işleyebilir, ardından bunları şirketlerin iletişim bilgileriyle birlikte konsolide bir veritabanında birleştirebilir.

## Özellikler

* PDF katılımcı listelerinden şirket bilgilerini çıkarma
* Fuar web sitelerinden şirket verilerini scrape etme
* Şirket bilgilerini temizleme ve standartlaştırma
* Yinelemeleri önleyerek birden fazla fuardan gelen verileri birleştirme
* Şirket web sitelerinden otomatik olarak ek iletişim bilgilerini toplama

## Proje Yapısı

```
├── data/
│   ├── input/          # Giriş dosyaları (PDF'ler, vb.)
│   ├── output/         # Bireysel fuar şirket listeleri
│   └── events/         # Ticaret fuarı etkinlik bilgileri
├── scrapers/
│   ├── aymod_scraper.py    # AYMOD fuarı scraper'ı
│   ├── aysaf_scraper.py    # AYSAF fuarı scraper'ı
│   ├── gapshoes_scraper.py # GAPSHOES fuarı scraper'ı
│   ├── sawo_scraper.py     # SAWO fuarı scraper'ı
│   ├── shoexpo_scraper.py  # SHOEXPO fuarı scraper'ı
│   └── fair_event_scraper.py # Ticaret fuarı etkinlik bilgisi scraper'ı
└── utils/
    ├── merge_company_data.py     # Tüm şirket verilerini birleştir
    └── contact_info_collector.py # Ek iletişim bilgileri toplama aracı
```

## Kurulum

### Ön Koşullar

* Python 3.6+
* Pip (Python paket yöneticisi)

### Kurulum

1. Bu repoyu klonlayın:
   ```
   git clone https://github.com/kullaniciadi/trade-fair-scraper.git
   cd trade-fair-scraper
   ```
2. Sanal bir ortam oluşturun ve etkinleştirin (önerilen):
   ```
   python -m venv venv
   source venv/bin/activate  # Windows'ta: venv\Scripts\activate
   ```
3. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

### Kütüphaneler

* pandas
* numpy
* PyPDF2
* selenium
* beautifulsoup4
* webdriver-manager
* ve diğer gerekli kütüphaneler (requirements.txt dosyasında tam liste mevcuttur)

## Kullanım

### Dizin Yapısını Hazırlama

Kazıyıcıları çalıştırmadan önce, uygun dizin yapısının oluşturulduğundan emin olun:

```
mkdir -p data/input data/output data/events
```

### Bireysel Scraper'ları Çalıştırma

Her scraper bağımsız olarak çalıştırılabilir:

```bash
# AYMOD fuarı scraper'ını çalıştır
python scrapers/aymod_scraper.py

# AYSAF fuarı scraper'ını çalıştır
python scrapers/aysaf_scraper.py

# GAPSHOES fuarı scraper'ını çalıştır
python scrapers/gapshoes_scraper.py

# SAWO fuarı scraper'ını çalıştır
python scrapers/sawo_scraper.py

# SHOEXPO fuarı scraper'ını çalıştır
python scrapers/shoexpo_scraper.py

# Yaklaşan ticaret fuarı etkinliklerini scrape et
python scrapers/fair_event_scraper.py
```

### Şirket Verilerini Birleştirme

Bireysel kazıyıcıları çalıştırdıktan sonra, tüm şirket verilerini tek bir dosyada birleştirin:

```bash
python utils/merge_company_data.py
```

Bu, `data/output` dizininde `all_companies_merged.xlsx` dosyasını oluşturacaktır.

### Ek İletişim Bilgilerini Toplama

Veri setini şirket web sitelerinden alınan iletişim bilgileriyle zenginleştirmek için:

```bash
python utils/contact_info_collector.py
```

Bu, ek web sitesi, e-posta ve telefon bilgileriyle `all_companies_updated.xlsx` dosyasını oluşturacaktır.

## Scraper Detayları

### PDF Scraper'ları

Aşağıdaki kazıyıcılar, PDF katılımcı listelerinden veri çıkarır:

* `sawo_scraper.py` - SAWO fuarı PDF'inden şirket adlarını ve ülkelerini çıkarır
* `gapshoes_scraper.py` - GAPSHOES fuarı PDF'inden şirket adlarını çıkarır
* `aysaf_scraper.py` - AYSAF fuarı PDF'inden şirket adlarını, ülkelerini ve stand bilgilerini çıkarır
* `shoexpo_scraper.py` - SHOEXPO fuarı PDF'inden şirket adlarını çıkarır

### Web Scraper'ları

* `aymod_scraper.py` - AYMOD ziyaretçi portalına giriş yapar ve detaylı şirket bilgilerini çıkarır
* `fair_event_scraper.py` - TOBB'un fuar takviminden ayakkabı sektörüyle ilgili yaklaşan ticaret fuarlarını scrape eder

### Yardımcı Araçlar

* `merge_company_data.py` - Tüm bireysel fuar Excel dosyalarını birleştirir, birden fazla fuarda yer alan şirketler için verileri birleştirir
* `contact_info_collector.py` - Şirket web sitelerini bulmak ve iletişim bilgilerini çıkarmak için web scraping kullanır

## Veri Şeması

Konsolide şirket verileri aşağıdaki alanları içerir:

* Firma Adı
* Sektör
* Yetkili Ad-Soyad
* Unvan
* Telefon
* Email
* Adres
* Website
* Katıldığı Fuar
* Ülke

## Notlar

* Scraper'lar, farklı PDF formatları ve web sitesi yapılarıyla başa çıkmak için güçlü hata yönetimi içerir.
* İletişim bilgileri toplayıcısı, hız sınırlamasından kaçınmak için rastgele gecikmeler ve kullanıcı ajan rotasyonu kullanır.
* Türkçe karakterlerle ilgili Unicode sorunları, `clean_unicode_issues` fonksiyonu kullanılarak özel olarak ele alınır.

## Karşılaşılan Zorluklar

- **CAPTCHA Sorunları**: Uygun proxy bulamadığım için sıklıkla CAPTCHA'ya yakalanma sorunu yaşadım. Uygulanan çözüm, CAPTCHA görüldüğünde kodu durdurup, CAPTCHA'yı elle çözdükten sonra devam etmek için Enter tuşuna basmak veya Google erişimi olan proxy'ler kullanmaktır.
- **Hesap Gereksinimleri**: AYMOD scraper'ı için sisteme giriş yapacak hesap bilgilerinin kod içerisinde düzenlenmesi gerekmektedir.
- **İletişim Bilgisi Doğruluğu**: İletişim bilgileri çıkarma işlemi %100 doğru olmamakla beraber, telefon numarası hatası veya faks numarasının telefon numarası olarak alınması gibi sorunlar yaşanabilmektedir.

## Gereksinimler

Tüm bağımlılıkları kurmak için, `pip install -r requirements.txt` komutunu çalıştırabilirsiniz. Gerekli tüm paketler requirements.txt dosyasında listelenmiştir.
