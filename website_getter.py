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

def scrape_fuar():
    Fuar_name = []
    Fuar_url = []

    Foptions = foptions()
    Foptions.headless = False

    Eoptions = eoptions()
    Eoptions.headless = False

    links = ["https://fuarlar.tobb.org.tr/FuarTakvimi/2024"]

    

    for link in links:
        driver = webdriver.Firefox(options=Foptions)
        driver.get(link)
        driver.maximize_window()
        time.sleep(7)
        
        html = driver.page_source

        search_input = driver.find_elements(By.CSS_SELECTOR, '.dxbl-text-edit .dxbl-text-edit-input')
        search_input = search_input[4]
        search_input.send_keys("ayakkabı")
        search_input.send_keys(Keys.ENTER)

        time.sleep(10)

        tbody = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/dxbl-grid/dxbl-scroll-viewer/div/table/tbody')

        tr_elements = tbody.find_elements(By.TAG_NAME, 'tr')

        for x in range(1,len(tr_elements)+1):
            try:
                name = driver.find_element(By.XPATH,(f'//*[@id="wrapper"]/div/div[2]/div[2]/div[1]/dxbl-grid/dxbl-scroll-viewer/div/table/tbody/tr[{x}]/td[4]')).text
                Fuar_name.append(name)
            except:
                Fuar_name.append(np.nan)

            try:
                url = driver.find_element(By.XPATH,(f'//*[@id="wrapper"]/div/div[2]/div[2]/div[1]/dxbl-grid/dxbl-scroll-viewer/div/table/tbody/tr[{x}]/td[14]')).text
                Fuar_url.append(url)
            except:
                Fuar_url.append(np.nan)
       
    driver.quit()

    event_list = pd.DataFrame()

    event_list.insert(0,"Fuar_name","")

    for event in range(0,len(Fuar_name)):
            event_info = {"Fuar_name": Fuar_name[event],
                          "Fuar_website": Fuar_url[event]
                        }
            event_list = event_list.append(event_info, ignore_index=True)


    event_list = event_list.drop_duplicates(subset=['Fuar_website'],keep='first')

    event_list.to_excel("Fuar_2024.xlsx",index=True,merge_cells=False)

scrape_fuar()