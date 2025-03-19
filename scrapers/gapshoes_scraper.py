import pandas as pd
import PyPDF2
import numpy as np

def Gapshoes_scrape():
    all_firms = []
    
    pdf_path = "data/input\Gapshoes.pdf"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    if (line.startswith('GAPSHOES') or 
                        not line or 
                        line.isdigit() or 
                        len(line) < 3):
                        continue
                    
                    if line[0].isdigit() and ' ' in line:
                        line = line.split(' ', 1)[1].strip()
                    
                    all_firms.append(line)
                    
        unique_firms = []
        seen = set()
        for firm in all_firms:
            if firm not in seen and not firm.isdigit():
                seen.add(firm)
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

    for firma in range(0, len(unique_firms)):
        firma_info = {"Firma Adı": unique_firms[firma],
                      "Sektör": np.nan,
                      "Yetkili Ad-Soyad": np.nan,
                      "Unvan": np.nan,
                      "Telefon": np.nan,
                      "Email": np.nan,
                      'Adres': np.nan,
                      'Website': np.nan,
                      'Katıldığı Fuar': 'GAPSHOES'
                    }
        firma_list = firma_list.append(firma_info, ignore_index=True)
    
    firma_list = firma_list.drop_duplicates(subset=['Firma Adı'], keep='first')
    
    firma_list.to_excel('data/output/gapshoes_companies.xlsx', index=False)
    
    return firma_list


Gapshoes_scrape()