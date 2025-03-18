import pandas as pd
import PyPDF2
import numpy as np
import re

def clean_unicode_issues(text):
    """Unicode sorunlarını temizler, özellikle Türkçe karakterleri düzeltir"""
    if not isinstance(text, str):
        return text
        
    # Türkçe karakterleri düzelt
    text = re.sub(r'/uni015E', 'Ş', text)
    text = re.sub(r'/uni015ETİ', 'ŞTİ', text)
    text = re.sub(r'/uni0130', 'İ', text)
    text = re.sub(r'/uni00DC', 'Ü', text)
    text = re.sub(r'/uni00D6', 'Ö', text)
    text = re.sub(r'/uni00C7', 'Ç', text)
    text = re.sub(r'/uni011E', 'Ğ', text)
    
    # Genel unicode temizliği
    text = re.sub(r'/uni[0-9A-F]{4}', '', text)
    
    return text

def Aysaf_scrape():
    all_firms = []
    
    pdf_path = "katilimci_liste_pdf/AYSAF_Exhibitor_List.pdf"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                lines = text.split('\n')
                current_company = None
                current_country = None
                current_stand = None
                
                for line in lines:
                    line = line.strip()
                    
                    # Skip headers, empty lines, page numbers, and labels
                    if (line.startswith('KATILIMCI LİSTESİ') or 
                        line.startswith('FİRMA ADI / COMPANY NAME') or
                        line.startswith('HALL / STAND NO.') or
                        line.startswith('ÜLKE / COUNTRY') or
                        line.startswith('13-16 KASIM') or
                        line.startswith('İSTANBUL EXPO CENTER') or
                        line.isdigit() or
                        line == "EXHIBITOR LIST" or
                        not line or
                        len(line) < 3):
                        continue
                    
                    # Line format usually: Company Name, Country, Stand Number
                    parts = line.split()
                    
                    # Check if line ends with a stand number pattern (HALL X / XXXX)
                    if "HALL" in line and "/" in line:
                        # This line likely contains all three parts: company, country, stand
                        stand_index = line.find("HALL")
                        country_index = line.rfind("TÜRKİYE", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("CHINA", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("GERMANY", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("ITALY", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("THAILAND", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("INDIA", 0, stand_index)
                        if country_index == -1:
                            country_index = line.rfind("UZBEKISTAN", 0, stand_index)
                            
                        if country_index > 0:
                            current_company = line[:country_index].strip()
                            # Temizleme işlemi - Unicode karakterleri düzelt
                            current_company = clean_unicode_issues(current_company)
                            current_country = line[country_index:stand_index].strip()
                            current_stand = line[stand_index:].strip()
                            
                            all_firms.append({
                                "Firma Adı": current_company,
                                "Ülke": current_country,
                                "Stand": current_stand
                            })
                    
                    # Reset for the next line
                    current_company = None
                    current_country = None
                    current_stand = None
                    
        # Remove duplicates and clean any remaining unicode issues
        unique_firms = []
        seen = set()
        for firm in all_firms:
            firm_name = firm["Firma Adı"]
            # Ek temizleme işlemi
            firm_name = clean_unicode_issues(firm_name)
            firm["Firma Adı"] = firm_name
            
            if firm_name not in seen:
                seen.add(firm_name)
                unique_firms.append(firm)
                
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return []
    
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
    firma_list.insert(9, 'Ülke', '')

    for firma in unique_firms:
        firma_info = {
            "Firma Adı": clean_unicode_issues(firma["Firma Adı"]),
            "Sektör": np.nan,
            "Yetkili Ad-Soyad": np.nan,
            "Unvan": np.nan,
            "Telefon": np.nan,
            "Email": np.nan,
            'Adres':  np.nan,
            'Website': np.nan,
            'Katıldığı Fuar': 'AYSAF',
            'Ülke': firma["Ülke"]
        }
        firma_list = firma_list.append(firma_info, ignore_index=True)
    
    firma_list = firma_list.drop_duplicates(subset=['Firma Adı'], keep='first')
    
    # Son bir temizlik daha yap - tüm DataFrame üzerinde
    for col in firma_list.columns:
        if firma_list[col].dtype == 'object':  # Sadece string (object) sütunlarını işle
            firma_list[col] = firma_list[col].apply(lambda x: clean_unicode_issues(x))
    
    firma_list.to_excel('Firma_katılımcı_liste/Aysaf_Firmalar.xlsx', index=False)
    
    return firma_list


Aysaf_scrape()