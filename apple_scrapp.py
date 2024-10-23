from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécuter en mode headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_data(url):
    info = {'URL': url}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Récupérer le titre
        try:
            h1_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="axHeader"]/h1')))
            h1_text = h1_element.text
            info['Titre'] = h1_text
            print(f"Titre: {h1_text}")
        except Exception as e:
            info['Titre'] = "Non trouvé"
            print(f"Erreur lors de l'extraction du texte h1 : {e}")

        # Récupérer l'adresse
        try:
            address_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class*="sc-platter-cell-content with-sc-icon"]')))
            info['Adresse'] = address_element.text
        except Exception:
            info['Adresse'] = "Non trouvée"

        # Récupérer le numéro de téléphone
        try:
            phone_bdo = wait.until(EC.visibility_of_element_located((By.XPATH, '//section[@class="sc-platter-cell"]//bdo')))
            phone_number = phone_bdo.text
            info['Numéro de téléphone'] = phone_number
            print(f"Numéro de téléphone : {phone_number}")
        except Exception as e:
            info['Numéro de téléphone'] = "Non trouvé"
            print(f"Erreur lors de l'extraction du numéro de téléphone : {e}")

        # Récupérer le lien du site web
        try:
            website_link = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "sc-unified-action-row-item") and contains(., "Site web")]')))
            website_href = website_link.get_attribute('href')
            info['Site web'] = website_href
            print(f"Lien du site web : {website_href}")
        except Exception as e:
            info['Site web'] = "Non trouvé"
            print(f"Erreur lors de l'extraction du lien du site web : {e}")

    except Exception as e:
        print(f"Erreur lors de l'extraction des données pour l'URL {url}: {e}")
    
    return info

# Exemple d'utilisation de la fonction
url = "https://maps.apple.com/place?auid=17157473234473157612"
data = extract_data(url)

# Afficher les données extraites
print(data)

# Fermer le driver
driver.quit()
