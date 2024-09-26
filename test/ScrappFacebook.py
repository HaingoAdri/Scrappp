import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_page(url):
    driver.get(url)
    time.sleep(5)
    
    try:
        page_title = driver.title
        
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.xyamay9.xykv574.xbmpl8g.x4cne27.xifccgj"))
        )
        address = None
        phone_number = None
        email = None
        website = None
        review = None

        for element in elements:
            text = element.text.strip()
            if text:
                if ',' in text:
                    address = text
                elif text.startswith('+') and len(text) > 10:
                    phone_number = text
                elif '@' in text:
                    email = text
                elif '/' in text:
                    website = text
                elif 'Pas encore évalué' in text:
                    review = text

        return {
            'Title': page_title,
            'Address': address,
            'Phone Number': phone_number,
            'Email': email,
            'Website': website,
            'Review': review
        }
    
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {url} : {e}")
        return {
            'Title': 'N/A',
            'Address': 'N/A',
            'Phone Number': 'N/A',
            'Email': 'N/A',
            'Website': 'N/A',
            'Review': 'N/A'
        }

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

input_csv = 'data.csv'

df = pd.read_csv(input_csv)

titles = []
addresses = []
phone_numbers = []
emails = []
websites = []
reviews = []

for index, row in df.iterrows():
    url = row['URL']
    print(f"Scraping {url}...")
    data = scrape_page(url)
    
    titles.append(data['Title'])
    addresses.append(data['Address'])
    phone_numbers.append(data['Phone Number'])
    emails.append(data['Email'])
    websites.append(data['Website'])
    reviews.append(data['Review'])

df['Title'] = titles
df['Address'] = addresses
df['Phone Number'] = phone_numbers
df['Email'] = emails
df['Website'] = websites
df['Review'] = reviews

df = df[['Title', 'Address', 'Phone Number', 'Email', 'Website', 'Review']]

df.to_csv(input_csv, index=False, encoding='utf-8')

driver.quit()

print(f"Les données mises à jour ont été enregistrées dans {input_csv}")
