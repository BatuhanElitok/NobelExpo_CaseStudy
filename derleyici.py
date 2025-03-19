import pandas as pd
import time
import random
import re
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("contact_finder.log", mode='w'),
        logging.StreamHandler()
    ]
)

# User agent listesi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.63',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/82.0.4227.23',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 OPR/79.0.4143.50'
]

# Proxy listesi
PROXIES = [
    '5.161.146.73:24079',
    '51.210.111.216:16466'
]

def clean_unicode_issues(text):
    """Unicode sorunlarını temizler"""
    if not isinstance(text, str):
        return text
        
    # Türkçe ve özel karakterleri düzelt
    text = re.sub(r'/uni015E', 'Ş', text)
    text = re.sub(r'/uni015ETİ', 'ŞTİ', text)
    text = re.sub(r'/uni0130', 'İ', text)
    text = re.sub(r'/uni00DC', 'Ü', text)
    text = re.sub(r'/uni00D6', 'Ö', text)
    text = re.sub(r'/uni00C7', 'Ç', text)
    text = re.sub(r'/uni011E', 'Ğ', text)
    text = re.sub(r'/uni0141', 'Ł', text)
    text = re.sub(r'/uni00F3', 'ó', text)
    
    # Genel unicode temizliği
    text = re.sub(r'/uni[0-9A-F]{4}', '', text)
    
    return text

def setup_opera_driver(headless=False):
    """Opera GX tarayıcısını hazırlar"""
    options = Options()
    
    if headless:
        options.add_argument("--headless")  # Görünmez modda çalıştır
    
    # Rastgele user agent seç
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")
    
    # Rastgele proxy seç
    proxy = random.choice(PROXIES)
    options.add_argument(f'--proxy-server=http://{proxy}')
    logging.info(f"Kullanılan proxy: {proxy}")
    
    # Opera GX ayarları (Chromium tabanlı)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-infobars")
    
    # Opera GX'in yolunu belirleme (Windows için örnek, kendi yolunuzu belirtmelisiniz)
    opera_path = "C:\\Users\\KULLANICI_ADI\\AppData\\Local\\Programs\\Opera GX\\opera.exe"  # Bu yolu kendi sisteminize göre değiştirin
    if not os.path.exists(opera_path):
        logging.warning(f"Opera GX belirtilen yolda bulunamadı: {opera_path}")
        logging.info("Sistem tarafından tespit edilebilen Opera GX kullanılacak")
    else:
        options.binary_location = opera_path
    
    try:
        # Chrome Driver yolu (Opera GX'in kullandığı Chromium sürümüne uygun olmalı)
        driver_path = "./chromedriver.exe"  # Windows için .exe uzantısı, diğer sistemlerde gerekli değil
        
        if not os.path.exists(driver_path):
            logging.error(f"ChromeDriver belirtilen yolda bulunamadı: {driver_path}")
            logging.info("Lütfen uygun ChromeDriver'ı indirip, doğru yolu belirtin")
            raise FileNotFoundError(f"ChromeDriver bulunamadı: {driver_path}")
            
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Opera GX tarayıcısı başlatıldı (ChromeDriver ile)")
        
    except Exception as e:
        logging.error(f"ChromeDriver hatası: {str(e)}")
        raise
    
    driver.set_page_load_timeout(30)
    
    return driver

def get_company_website(driver, company_name, country):
    """
    Şirket web sitesini manuel arama yoluyla bulmaya çalışır
    """
    if pd.isna(country):
        query = f"{company_name} official website"
    else:
        query = f"{company_name} {country} official website"
        
    logging.info(f"Aranan şirket: {company_name}")
    website_url = None
    
    try:
        driver.get('https://www.google.com')
        time.sleep(random.uniform(2, 4))
        
        try:
            cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept all') or contains(text(), 'Kabul et') or contains(text(), 'I agree') or contains(text(), 'Akzeptieren')]")
            cookies_button.click()
            time.sleep(random.uniform(1, 2))
        except Exception as cookie_error:
            logging.info(f"Çerez bildirimi bulunamadı veya zaten kabul edildi: {str(cookie_error)}")
        
        try:
            search_bar = driver.find_element(By.NAME, "q")
            search_bar.clear()
            
            for char in query:
                search_bar.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
                
            time.sleep(random.uniform(0.5, 1))
            search_bar.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 5))
        except Exception as e:
            logging.error(f"Arama kutusu hatası: {str(e)}")
            
            selectors = ['#APjFqb', 'input[name="q"]', 'input[title="Search"]', '.gLFyf']
            
            success = False
            for selector in selectors:
                try:
                    search_bar = driver.find_element(By.CSS_SELECTOR, selector)
                    search_bar.clear()
                    search_bar.send_keys(query)
                    time.sleep(random.uniform(0.5, 1))
                    search_bar.send_keys(Keys.RETURN)
                    time.sleep(random.uniform(3, 5))
                    success = True
                    break
                except:
                    continue
            
            if not success:
                logging.error("Tüm arama kutusu seçicileri başarısız oldu")
                return None
        
        time.sleep(random.uniform(3, 5))
        
        if "captcha" in driver.current_url.lower() or "bot" in driver.current_url.lower() or "consent" in driver.current_url.lower():
            logging.warning("CAPTCHA algılandı!")
            input("CAPTCHA algılandı. Lütfen CAPTCHA'yı çözün ve Enter tuşuna basın...")
            time.sleep(2)
        
        links = driver.find_elements(By.TAG_NAME, "a")
        valid_links = []
        
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and href.startswith("http") and not href.startswith(("https://www.google", "https://support.google", "https://accounts.google", "https://maps.google")):
                    valid_links.append(href)
            except:
                continue
        
        if valid_links:
            common_directories = ["linkedin.com", "facebook.com", "twitter.com", "instagram.com", "youtube.com"]
            filtered_links = [link for link in valid_links if not any(directory in link for directory in common_directories)]
            
            if filtered_links:
                website_url = filtered_links[0]
                logging.info(f"Bulunan web sitesi (filtrelenmiş): {website_url}")
            else:
                website_url = valid_links[0]
                logging.info(f"Bulunan web sitesi: {website_url}")
        else:
            logging.warning("Hiçbir geçerli link bulunamadı")
            input("Hiçbir geçerli link bulunamadı. Devam etmek için Enter tuşuna basın...")
        
        return website_url
        
    except Exception as e:
        logging.error(f"Web sitesi arama hatası: {str(e)}")
        return None

def extract_contact_info(driver, website_url):
    """
    Verilen web sitesinden iletişim bilgilerini çıkarır (sadece telefon ve email)
    """
    if not website_url:
        return {}
    
    contact_info = {
        'Telefon': None,
        'Email': None
    }
    
    try:
        logging.info(f"Web sitesi ziyaret ediliyor: {website_url}")
        driver.get(website_url)
        time.sleep(random.uniform(3, 5))
        
        contact_page_url = None
        links = driver.find_elements(By.TAG_NAME, "a")
        
        contact_keywords = ["contact", "iletişim", "kontakt", "contact-us", "about-us", "about", "hakkımızda", "firma", "company", "ulaşım"]
        
        for link in links:
            try:
                href = link.get_attribute("href")
                text = link.text.lower()
                
                if href and any(keyword in text or keyword in href.lower() for keyword in contact_keywords):
                    contact_page_url = href
                    logging.info(f"İletişim sayfası bulundu: {contact_page_url}")
                    break
            except:
                continue
        
        if contact_page_url:
            try:
                driver.get(contact_page_url)
                time.sleep(random.uniform(2, 4))
                logging.info("İletişim sayfası yüklendi")
            except Exception as e:
                logging.error(f"İletişim sayfası yükleme hatası: {str(e)}")
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        phone_patterns = [
            r'(?:Tel|Phone|Telefon|T|Ph|Fon)[^\d+]*((?:\+|00)?[\d\s\(\).-]{7,})',
            r'(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{1,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}'
        ]
        
        for pattern in phone_patterns:
            phone_matches = re.findall(pattern, page_text)
            if phone_matches:
                longest_match = max(phone_matches, key=len)
                contact_info['Telefon'] = longest_match.strip()
                logging.info(f"Telefon numarası bulundu: {contact_info['Telefon']}")
                break
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = re.findall(email_pattern, page_text)
        
        if email_matches:
            contact_info['Email'] = email_matches[0].strip()
            logging.info(f"E-posta adresi bulundu: {contact_info['Email']}")
        
        return contact_info
        
    except Exception as e:
        logging.error(f"İletişim bilgisi çıkarma hatası: {str(e)}")
        return contact_info

def process_companies():
    """
    Ana işleme fonksiyonu
    """
    input_file = 'Tüm_Firmalar_Birleşik.xlsx'
    output_file = 'Tüm_Firmalar_Birleşik_Guncel.xlsx'
    
    if not os.path.exists(input_file):
        logging.error(f"Giriş dosyası bulunamadı: {input_file}")
        return
    
    try:
        df = pd.read_excel(input_file)
        logging.info(f"Excel dosyası okundu. Toplam {len(df)} kayıt.")
    except Exception as e:
        logging.error(f"Excel okuma hatası: {str(e)}")
        return
    
    start_index = 0
    if os.path.exists(output_file):
        try:
            saved_df = pd.read_excel(output_file)
            for idx, row in saved_df.iterrows():
                if pd.notna(row.get('Website')) and row.get('Website') != '':
                    start_index = idx + 1
            
            if start_index > 0:
                df = saved_df.copy()
                logging.info(f"Kayıtlı ilerleme bulundu. {start_index}. kayıttan devam ediliyor.")
        except:
            logging.warning("Kayıtlı dosya okunamadı, baştan başlanıyor.")
    
    for column in ['Telefon', 'Email', 'Website']:
        if column not in df.columns:
            df[column] = None
    
    driver = None
    try:
        driver = setup_opera_driver(headless=False)
        logging.info("Opera GX tarayıcısı başlatıldı.")
        
        total_remaining = len(df) - start_index
        logging.info(f"İşlenecek {total_remaining} kayıt kaldı.")
        
        for index, row in df.iloc[start_index:].iterrows():
            company_name = row['Firma Adı']
            country = row.get('Ülke', '')
            
            logging.info(f"[{index+1}/{len(df)}] İşleniyor: {company_name}")
            
            website = get_company_website(driver, company_name, country)
            
            if website:
                df.at[index, 'Website'] = website
                
                contact_info = extract_contact_info(driver, website)
                
                for key, value in contact_info.items():
                    if value:
                        df.at[index, key] = value
            
            df.to_excel(output_file, index=False)
            logging.info(f"İlerleme kaydedildi: {index+1}/{len(df)}")
            
            wait_time = random.uniform(10, 15)
            logging.info(f"Sonraki şirket için {wait_time:.1f} saniye bekleniyor...")
            time.sleep(wait_time)
    
    except Exception as e:
        logging.error(f"Genel işlem hatası: {str(e)}")
    
    finally:
        if driver:
            driver.quit()
            logging.info("Tarayıcı kapatıldı.")
        
        if 'df' in locals():
            df.to_excel(output_file, index=False)
            logging.info(f"İşlem tamamlandı. Sonuçlar '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    logging.info("=== Şirket İletişim Bilgisi Toplama Başlatılıyor ===")
    process_companies()