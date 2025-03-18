import pandas as pd
import PyPDF2
import numpy as np
import re

def clean_unicode_issues(text):
    """Unicode sorunlarını temizler"""
    if not isinstance(text, str):
        return text
        
    # Türkçe ve Polonyaca karakterleri düzelt
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

def AA_scrape():
    all_firms = []
    
    pdf_path = "katilimci_liste_pdf/lista_wystawców_sawo_2024-04-02.pdf"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    # Skip headers, empty lines, page numbers
                    if (line.startswith('NAZWA FIRMY / COMPANY NAME') or
                        line.startswith('KRAJ') or
                        line.startswith('COUNTRY') or
                        line.startswith('PAWILON/HALL') or
                        line.startswith('NR / NO') or
                        not line or
                        len(line) < 3):
                        continue
                    
                    # PDF'den line için düzgün bir deseni yakalayalım
                    # Format genellikle: Şirket Adı, Ülke Kodu, Ülke, Salon/Hall, Stand No
                    parts = line.split()
                    
                    # En az 4 parça varsa (şirket, ülke kodu, ülke, stand)
                    if len(parts) >= 4:
                        # Son kısım genellikle stand numarası
                        stand_no = parts[-1]
                        hall_no = parts[-2]
                        
                        # Ülke ve ülke kodu genellikle stand numarasından önce gelir
                        country_name = parts[-3]
                        country_code = parts[-4]
                        
                        # İlk kısmı şirket adı olarak al (son 4 parça hariç)
                        company_name = " ".join(parts[:-4])
                        
                        all_firms.append({
                            "Firma Adı": company_name,
                            "Ülke": country_name
                        })
                
        # PDF düzeni tutarlı değilse, doğrudan tüm satırı işleyelim
        if not all_firms:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    # Özel satırları atla
                    if (line.startswith('NAZWA FIRMY / COMPANY NAME') or
                        line.startswith('KRAJ') or
                        line.startswith('COUNTRY') or
                        line.startswith('PAWILON/HALL') or
                        line.startswith('NR / NO') or
                        not line or
                        len(line) < 3):
                        continue
                    
                    # En az bir boşluk içeren satırları işle
                    if " " in line:
                        # Son kelime genellikle stand numarasıdır
                        parts = line.split()
                        if len(parts) >= 3:
                            stand_no = parts[-1]
                            
                            # İkinci son kelime genellikle salon/hall numarasıdır
                            hall_no = parts[-2]
                            
                            # Üçüncü son kelime genellikle ülke adıdır
                            country = parts[-3]
                            
                            # Geri kalan her şey şirket adıdır
                            company = " ".join(parts[:-3])
                            
                            all_firms.append({
                                "Firma Adı": company,
                                "Ülke": country
                            })
    
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return []
    
    # Bu PDF için alternatif bir yaklaşım kullanalım - tablolu yapıyı yakala
    if not all_firms:
        try:
            all_firms = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                lines = text.split('\n')
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    
                    if not line or len(line) < 3:
                        continue
                    
                    # Eğer satır bir rakamla başlıyorsa veya header satırıysa atla
                    if (line[0].isdigit() or 
                        "COMPANY NAME" in line or 
                        "KRAJ" in line or 
                        "COUNTRY" in line or
                        "PAWILON" in line or
                        "NR / NO" in line):
                        continue
                    
                    # Satırda en az 2 boşluk var mı kontrol et
                    spaces = [pos for pos, char in enumerate(line) if char == ' ']
                    if len(spaces) < 2:
                        continue
                    
                    # Stand numarası genellikle son kelimedir ve sayısal değer içerir
                    parts = line.split()
                    if len(parts) < 3:
                        continue
                    
                    # Sayı olan son kelimeyi bul
                    stand_index = -1
                    for i in range(len(parts)-1, -1, -1):
                        if any(c.isdigit() for c in parts[i]):
                            stand_index = i
                            break
                    
                    if stand_index == -1:
                        continue
                    
                    # Hall/Salon numarası genellikle stand numarasından önce gelir
                    hall_index = stand_index - 1
                    if hall_index < 0:
                        continue
                    
                    # Ülke genellikle hall numarasından önce gelir
                    country_index = hall_index - 1
                    if country_index < 0:
                        continue
                    
                    stand = parts[stand_index]
                    hall = parts[hall_index]
                    country = parts[country_index]
                    
                    # Şirket adı geri kalan her şeydir
                    company = " ".join(parts[:country_index])
                    
                    all_firms.append({
                        "Firma Adı": company,
                        "Ülke": country
                    })
                    
        except Exception as e:
            print(f"Alternatif PDF okuma hatası: {e}")
    
    # Manuel olarak PDF'yi analiz edelim
    if not all_firms:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    
                    # Tabloda genellikle şirket adı, ülke kodu (Örn. POLSKA), ülke adı (POLAND) ve salon+stand (3A 123) şeklinde düzen vardır
                    # "COMPANY NAME", "KRAJ", "COUNTRY", "PAWILON/HALL", "NR / NO" başlıklarını bul
                    if "NAZWA FIRMY / COMPANY NAME" in text and "COUNTRY" in text and "PAWILON/HALL" in text:
                        lines = text.split('\n')
                        
                        for line in lines:
                            if (not line or 
                                "NAZWA FIRMY / COMPANY NAME" in line or 
                                "KRAJ" in line or 
                                "COUNTRY" in line or
                                "PAWILON/HALL" in line or
                                "NR / NO" in line):
                                continue
                            
                            # Satırın 4 sütundan oluştuğunu varsayalım: Şirket, Ülke Kodu, Ülke, Hall, Stand No
                            columns = line.split()
                            
                            if len(columns) >= 5:
                                # Son iki sütun: Hall ve Stand No
                                stand_no = columns[-1]
                                hall_no = columns[-2]
                                
                                # Üçüncü son sütun: Ülke (POLAND, CHINA vs.)
                                country = columns[-3]
                                
                                # Dördüncü son sütun: Ülke Kodu (POLSKA, CHINY vs.)
                                # country_code = columns[-4]
                                
                                # İlk sütunlar: Şirket Adı (tüm geri kalanlar)
                                company_name = " ".join(columns[:-4])
                                
                                all_firms.append({
                                    "Firma Adı": company_name,
                                    "Ülke": country
                                })
        except Exception as e:
            print(f"Manuel PDF okuma hatası: {e}")
    
    # Eğer hala veri toplayamadıysak, en basit yöntemi uygula
    if not all_firms:
        try:
            # Elle ayırma yöntemi - satırlara böl, alanları kendi belirle
            data_lines = []
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    lines = text.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        
                        # Header satırlarını atla
                        if (not line or 
                            "COMPANY NAME" in line or 
                            "KRAJ" in line or 
                            "COUNTRY" in line or
                            "PAWILON" in line or
                            "NR / NO" in line):
                            continue
                        
                        # En az bir boşluk içeren satırları işle
                        if " " in line:
                            data_lines.append(line)
            
            # Her bir satırı işle
            for line in data_lines:
                parts = line.split()
                
                # En az 4 parça olmalı: şirket adı, ülke kodu, ülke adı, salon+stand
                if len(parts) >= 4:
                    # Son iki parça genellikle salon ve stand numarasıdır
                    stand_info = f"{parts[-2]} {parts[-1]}"
                    
                    # 3. son ve 4. son parçalar genellikle ülke bilgisidir
                    country_info = parts[-3]
                    
                    # Geri kalan parçalar şirket adıdır
                    company_name = " ".join(parts[:-3])
                    
                    all_firms.append({
                        "Firma Adı": company_name,
                        "Ülke": country_info
                    })
        except Exception as e:
            print(f"Son çare PDF okuma hatası: {e}")
    
    # Tekrarlanan girişleri kaldır
    unique_firms = []
    seen = set()
    for firm in all_firms:
        firm_name = firm["Firma Adı"]
        if firm_name not in seen:
            seen.add(firm_name)
            unique_firms.append(firm)
    
    # Veri çerçevesi oluştur
    firma_list = pd.DataFrame()
    
    # Sütunları ekle
    firma_list.insert(0, "Firma Adı", "")
    firma_list.insert(1, 'Sektör', np.nan)
    firma_list.insert(2, 'Yetkili Ad-Soyad', np.nan)
    firma_list.insert(3, 'Unvan', np.nan)
    firma_list.insert(4, 'Telefon', np.nan)
    firma_list.insert(5, 'Email', np.nan)
    firma_list.insert(6, 'Adres', np.nan)
    firma_list.insert(7, 'Website', np.nan)
    firma_list.insert(8, 'Katıldığı Fuar', 'A+A')
    firma_list.insert(9, 'Ülke', "")
    
    # Verileri ekle
    for firma in unique_firms:
        firma_info = {
            "Firma Adı": clean_unicode_issues(firma["Firma Adı"]),
            "Ülke": firma["Ülke"],
            "Katıldığı Fuar": 'SAWO'
        }
        firma_list = firma_list.append(firma_info, ignore_index=True)
    
    # Tekrarlanan girişleri kaldır
    firma_list = firma_list.drop_duplicates(subset=['Firma Adı'], keep='first')
    
    # Excel dosyasına kaydet
    firma_list.to_excel('Firma_katılımcı_liste/AA_Firmalar.xlsx', index=False)
    
    return firma_list

AA_scrape()