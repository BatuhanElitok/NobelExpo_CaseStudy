# Trade Fair Company Data Scraper

## Overview

This project contains a collection of scrapers designed to extract company information from various trade fair exhibitor lists. The scrapers can process data from multiple sources (websites, PDFs) and formats, then merge them into a consolidated database of companies with their contact information.

## Features

* Extract company information from PDF exhibitor lists
* Scrape company data from trade fair websites
* Clean and standardize company information
* Merge data from multiple fairs while avoiding duplicates
* Automatically collect additional contact information from company websites

## Project Structure

```
├── data/
│   ├── input/          # Input files (PDFs, etc.)
│   ├── output/         # Individual fair company lists
│   └── events/         # Trade fair event information
├── scrapers/
│   ├── aymod_scraper.py    # AYMOD fair scraper
│   ├── aysaf_scraper.py    # AYSAF fair scraper
│   ├── gapshoes_scraper.py # GAPSHOES fair scraper
│   ├── sawo_scraper.py     # SAWO fair scraper
│   ├── shoexpo_scraper.py  # SHOEXPO fair scraper
│   └── fair_event_scraper.py # Trade fair event information scraper
└── utils/
    ├── merge_company_data.py     # Combine all company data
    └── contact_info_collector.py # Additional contact info collection tool
```

## Installation

### Prerequisites

* Python 3.6+
* Pip (Python package manager)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/trade-fair-scraper.git
   cd trade-fair-scraper
   ```
2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Dependencies

* pandas
* numpy
* PyPDF2
* selenium
* beautifulsoup4
* webdriver-manager

## Usage

### Directory Setup

Before running the scrapers, ensure you have the proper directory structure:

```
mkdir -p data/input data/output data/events
```

### Running Individual Scrapers

Each scraper can be run independently:

```bash
# Run AYMOD fair scraper
python scrapers/aymod_scraper.py

# Run AYSAF fair scraper
python scrapers/aysaf_scraper.py

# Run GAPSHOES fair scraper
python scrapers/gapshoes_scraper.py

# Run SAWO fair scraper
python scrapers/sawo_scraper.py

# Run SHOEXPO fair scraper
python scrapers/shoexpo_scraper.py

# Scrape upcoming trade fair events
python scrapers/fair_event_scraper.py
```

### Merging Company Data

After running individual scrapers, merge all company data into a single file:

```bash
python utils/merge_company_data.py
```

This will create `all_companies_merged.xlsx` in the `data/output` directory.

### Collecting Additional Contact Information

To enrich the dataset with contact information from company websites:

```bash
python utils/contact_info_collector.py
```

This will create `all_companies_updated.xlsx` with additional website, email, and phone information.

## Scraper Details

### PDF Scrapers

The following scrapers extract data from PDF exhibitor lists:

* `sawo_scraper.py` - Extracts company names and countries from SAWO fair PDF
* `gapshoes_scraper.py` - Extracts company names from GAPSHOES fair PDF
* `aysaf_scraper.py` - Extracts company names, countries, and stand info from AYSAF fair PDF
* `shoexpo_scraper.py` - Extracts company names from SHOEXPO fair PDF

### Web Scrapers

* `aymod_scraper.py` - Logs in to the AYMOD visitor portal and extracts detailed company information
* `fair_event_scraper.py` - Scrapes upcoming footwear industry trade fairs from TOBB's trade fair calendar

### Utilities

* `merge_company_data.py` - Combines all individual fair Excel files, merging data for companies that appear in multiple fairs
* `contact_info_collector.py` - Uses web scraping to find company websites and extract contact information

## Data Schema

The consolidated company data includes the following fields:

* Firma Adı (Company Name)
* Sektör (Sector)
* Yetkili Ad-Soyad (Contact Person)
* Unvan (Title)
* Telefon (Phone)
* Email
* Adres (Address)
* Website
* Katıldığı Fuar (Participating Fair)
* Ülke (Country)

## Notes

* The scrapers include robust error handling to deal with different PDF formats and website structures.
* The contact information collector uses random delays and user agent rotation to avoid rate limiting.
* Unicode issues with Turkish characters are specifically handled using the `clean_unicode_issues` function.

## Challenges Faced

- **CAPTCHA Issues**: Finding suitable proxies was difficult, resulting in frequent CAPTCHA challenges. The solution implemented is to pause the code when a CAPTCHA appears, allowing for manual resolution before continuing (pressing Enter to resume the script), or using proxies with Google access.
- **Account Requirements**: The AYMOD scraper requires login credentials that need to be configured in the code before running.
- **Contact Information Accuracy**: The contact information extraction is not 100% accurate - there are occasional issues with phone number extraction or fax numbers being incorrectly identified as phone numbers.

## Requirements

To install all dependencies, create a requirements.txt file with:

```
pandas
numpy
PyPDF2
selenium
beautifulsoup4
webdriver-manager
```

Then run `pip install -r requirements.txt`
