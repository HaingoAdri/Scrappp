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

        # Vérifier si l'endroit est définitivement fermé
        try:
            closure_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-opening-state.sc-place-permanent-closure')))
            info['Horaires'] = closure_element.text
            info['Statut'] = "Fermé définitivement"
            print(f"Statut : {info['Statut']}")
        except Exception:
            info['Statut'] = "Ouvert"

        # Vérifier si l'endroit est ouvert 24h/24
        if info['Statut'] == "Ouvert":
            try:
                open_24h_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-hours-row.sc-hours-everyday.sc-open-24-hours')))
                info['Horaires'] = open_24h_element.text
                info['Statut'] = "Ouvert 24h/24, tous les jours"
                print(f"Statut : {info['Statut']}")
            except Exception:
                pass

        # Vérifier si la classe contient sc-platter-cell-content et récupérer les horaires détaillés
        try:
            hours_unfolded_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-hours-unfolded')))
            hours_rows = hours_unfolded_element.find_elements(By.CSS_SELECTOR, 'div.sc-hours-row')

            horaires = []
            for row in hours_rows:
                # Extraire le jour
                day_element = row.find_element(By.CSS_SELECTOR, 'div.sc-day-range.sc-hours-day')
                day = day_element.text

                # Extraire les horaires pour ce jour
                hours_element = row.find_element(By.CSS_SELECTOR, 'div.sc-hours-range')
                spans = hours_element.find_elements(By.TAG_NAME, 'span')
                hours = " – ".join([span.text for span in spans])  # Joindre les horaires entre " – "

                # Ajouter les horaires à la liste
                horaires.append({'Jour': day, 'Horaires': hours})

            info['Horaires détaillés'] = horaires
            print("Horaires détaillés récupérés avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'extraction des horaires détaillés : {e}")
            info['Horaires détaillés'] = "Non trouvés"

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
