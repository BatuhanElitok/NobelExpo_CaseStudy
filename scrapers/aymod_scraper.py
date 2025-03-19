from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver import Keys
from selenium.webdriver.firefox.options import Options as foptions
from selenium.webdriver.edge.options import Options as eoptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def scrape_fuar():
    firma_adi_list = []
    firma_yetkili_list = []
    firma_telefon_list = []
    firma_email_list = []
    firma_website_list = []
    firma_adres_list = []

    Foptions = foptions()
    Foptions.headless = True

    Eoptions = eoptions()
    Eoptions.headless = True

    links = ["https://www.aymod.com/visitors/visitor-panel"]

    for link in links:
        driver = webdriver.Firefox(options=Foptions)
        driver.capabilities["unexpectedAlertBehaviour"] = "accept"
        driver.get(link)
        driver.maximize_window()
        time.sleep(2)

        login = driver.find_elements(By.CLASS_NAME, 'ps-5')[1]
        password = driver.find_elements(By.CLASS_NAME, 'ps-5')[2]
        login_btn = driver.find_element(By.XPATH, ('/html/body/div[1]/main/div[1]/div[2]/div[1]/div/div/form/button'))

        login.send_keys('email')
        password.send_keys('password')
        login_btn.send_keys(Keys.ENTER)
        time.sleep(2)
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            print("Alert bulunamadı, devam ediliyor")
        
        time.sleep(2)

        driver.get("https://www.aymod.com/participant")
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div/div[1]/div"))
        )

        firma_list= driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div/div')

        firma_in_list = firma_list.find_elements(By.CLASS_NAME, 'col-sm-4')
        for x in range(1,len(firma_in_list)+1):
            firma = driver.find_element(By.XPATH,f'/html/body/div[1]/main/div[2]/div[2]/div/div/div/div[{x}]/div')

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", firma)
            time.sleep(1)
            firma.click()
            time.sleep(1)
            try:
                firma_adi = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[1].text
                firma_adi_list.append(firma_adi)
            except:
                firma_adi_list.append(np.nan)

            try:
                firma_yetkili = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[2].text
                firma_yetkili_list.append(firma_yetkili)
            except:
                firma_yetkili_list.append(np.nan)

            try:
                firma_telefon = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[4].text
                firma_telefon_list.append(firma_telefon)
            except:
                firma_telefon_list.append(np.nan)

            try:
                firma_email = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[5].text
                firma_email_list.append(firma_email)
            except:
                firma_email_list.append(np.nan)

            try:
                firma_website = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[6].text
                firma_website_list.append(firma_website)
            except:
                firma_website_list.append(np.nan)

            try:
                firma_adres = driver.find_elements(By.CSS_SELECTOR, '.fs-sm.mb-0')[7].text
                firma_adres_list.append(firma_adres)
            except:
                firma_adres_list.append(np.nan)

            time.sleep(1)
            driver.back()
        
        driver.quit()

    firma_list = pd.DataFrame()

    firma_list.insert(0,"Firma Adı","")
    firma_list.insert(1,'Sektör',"")
    firma_list.insert(2,'Yetkili Ad-Soyad','')
    firma_list.insert(3,'Unvan','')
    firma_list.insert(4,'Telefon','')
    firma_list.insert(5,'Email','')
    firma_list.insert(6,'Adres','')
    firma_list.insert(7,'Website','')
    firma_list.insert(8,'Katıldığı Fuar','')

    for firma in range(0,len(firma_adi_list)):
            firma_info = {"Firma Adı": firma_adi_list[firma],
                          "Sektör": np.nan,
                          "Yetkili Ad-Soyad": firma_yetkili_list[firma],
                          "Unvan": 'Firma Yetkilisi',
                          "Telefon": firma_telefon_list[firma],
                          "Email": firma_email_list[firma],
                          'Adres': firma_adres_list[firma],
                          'Website': firma_website_list[firma],
                          'Katıldığı Fuar': 'AYMOD'
                        }
            firma_list = firma_list.append(firma_info, ignore_index=True)
        
    firma_list = firma_list.drop_duplicates(subset=['Firma Adı'], keep='first')
    
    firma_list.to_excel("data/output/aymod_companies.xlsx", index=False)
    print(f"Toplam {len(firma_list)} firma bilgisi Excel'e kaydedildi.")

if __name__ == "__main__":
    scrape_fuar()