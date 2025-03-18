import pandas as pd
import PyPDF2
import os
import numpy as np
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def shoexpo_scrape():
    all_brands = []
    brands = []
    
    pdf_path = "katilimci_liste/SHOEXPO-KATILIMCI-LISTESI.pdf"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    if not line or line.isdigit() or len(line) < 3:
                        continue
                    
                    all_brands.append(line)
        
        # Remove duplicates while preserving order
        seen = set()
        for brand in all_brands:
            if brand not in seen:
                seen.add(brand)
                brands.append(brand)
                
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
    
    firma_list = pd.DataFrame()

    firma_list.insert(0, "Firma Adı", "")
    firma_list.insert(1, 'Sektör', "")
    firma_list.insert(2, 'Yetkili Ad-Soyad', '')
    firma_list.insert(3, 'Unvan', '')
    firma_list.insert(4, 'Telefon', '')
    firma_list.insert(5, 'Email', '')
    firma_list.insert(6, 'Adres', '')
    firma_list.insert(7, 'Website', '')
    firma_list.insert(8, 'Katıldığı Fuar', '')

    for firma in range(0, len(brands)):
        firma_info = {"Firma Adı": brands[firma],
                      "Sektör": np.nan,
                      "Yetkili Ad-Soyad": np.nan,
                      "Unvan": np.nan,
                      "Telefon": np.nan,
                      "Email": np.nan,
                      'Adres': np.nan,
                      'Website': np.nan,
                      'Katıldığı Fuar': 'SHOEXPO'
                    }
        firma_list = firma_list.append(firma_info, ignore_index=True)
    
    firma_list = firma_list.drop_duplicates(subset=['Firma Adı'], keep='first')
    
    firma_list.to_excel('Firma_katılımcı_liste/Shoexpo_Firmalar.xlsx', index=False)

shoexpo_scrape()