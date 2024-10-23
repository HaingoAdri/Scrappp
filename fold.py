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

        # Récupérer l'adresse
        try:
            address_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-platter-cell-content')))
            info['Horaire'] = address_element.text
        except Exception:
            info['Horaire'] = "Non trouvée"

        # Récupérer les horaires
        try:
            hours_rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-hours-row')))
            horaires = []
            for row in hours_rows:
                # Récupérer le texte de la div avec la classe sc-day-range
                day_range_element = row.find_element(By.CSS_SELECTOR, 'div.sc-day-range')
                hours_range_element = row.find_element(By.CSS_SELECTOR, 'div.sc-hours-range')

                # Extraire le texte
                day_text = day_range_element.text
                hours_text = hours_range_element.text
                
                horaires.append({'Jour': day_text, 'Horaires': hours_text})
            info['Horaires'] = horaires
        except Exception as e:
            print(f"Erreur lors de l'extraction des horaires : {e}")
            info['Horaires'] = "Non trouvés"

    except Exception as e:
        print(f"Erreur lors de l'extraction des données pour l'URL {url}: {e}")
    
    return info

# Exemple d'utilisation de la fonction
url = "https://maps.apple.com/place?auid=12514569602141617662"
data = extract_data(url)

# Afficher les données extraites
print(data)

# Fermer le driver
driver.quit()
