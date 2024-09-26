import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os  # Pour vérifier si le fichier existe

# Configurer les options de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_data(url):
    info = {'URL': url}
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        try:
            div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.PZPZlf.ssJ7i.xgAzOe, .PZPZlf.ssJ7i.B5dxMb')))
            info['Nom Google'] = div_element.text
        except Exception:
            info['Nom Google'] = "Non trouvé"
        
        try:
            span_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'LrzXr')))
            info['Adresse'] = span_element.text
        except Exception:
            info['Adresse'] = "Non trouvée"
        
        try:
            phone_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-dtype="d3ph"]')))
            info['Numéro de téléphone'] = phone_link.text
        except Exception:
            info['Numéro de téléphone'] = "Non trouvé"

        try:
            a_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.n1obkb.mI8Pwc')))
            info['URL du lien'] = a_element.get_attribute('href')
        except Exception:
            info['URL du lien'] = "Non trouvé"

        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "WgFkxc")]')))
            rows = table.find_elements(By.XPATH, './/tr')
            horaires = {}
            for row in rows:
                cells = row.find_elements(By.XPATH, './/td[contains(@class, "SKNSIb")]')
                cells2 = row.find_elements(By.XPATH, './/td[not(contains(@class, "SKNSIb"))]')
                if len(cells) == 1 and len(cells2) == 1:
                    day = driver.execute_script("return arguments[0].innerText;", cells[0])
                    hours = driver.execute_script("return arguments[0].innerText;", cells2[0])
                    horaires[day] = hours
            info['Horaires'] = horaires
        except Exception:
            info['Horaires'] = "Non trouvés"
    
    except Exception as e:
        print(f"Erreur lors de l'extraction des données pour l'URL {url}: {e}")
    
    return info

# Liste d'URLs à traiter
urls = [
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDA0SjJNTTIzMLY0TbVISUmyMqhIsTA0Nk42SrQwNExJNjUxX8Qq7JyfU5qbVFqs4JyYdnilgpqCcz4Ayvx61T8AAAA&hl=fr&mat=CZBa2HqgWZpyElMBEKoLaYTcNucrwWkMXmlCVUvDGczrKPcC6aI35uTOuU_TFWCY1zLHjWwg8RYHegHsKX9LL6FdKf9ZSE6m6UTWBsRYeUaebRVmHNbp8-lO5V3wkA&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDAxTzZIM062sEhNS7YwSTa0MqhIM0s0tEyxNEk0NDNLSTYxW8Qq7JyfU5qbVFqs4JyYdnilgpqCcz4Aod9U0z8AAAA&hl=fr&mat=Ccy7nxgDFDVRElcBEKoLaSd8IuPLNRHz3b5mxLdAXF09rqkOLS_xRdUoMhe9GW8h5Xe6Aao0IEx-ABvMpFhsHp-0Yjqasw_eh4jdswdk_tljqFL6AbS796AfGI2PAWlqsNI&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDA0SjE3MjU0MzZKTU1JsrS0MqiwTDI1SDE1MjMxTTVKSzM0XsQq7JyfU5qbVFqs4JyYdnilgpqCcz4Ar-QU9D8AAAA&hl=fr&mat=CXKJ8sPY5NaJElYBEKoLaSVPR6tc5x7FEwvwMi5NW8qFugJtI_7CMzRUQivElxO1w2HAgQacgqk5DedFAjGzBV86mtz4X7odADYZdt76jaqha2tC9qjfh78Bl0ncYD7U5g&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDAxTzUzMDW2MEoxT0pLNja2MqgwNTIzTEsysEw1szRLTbQwXsQq7JyfU5qbVFqs4JyYdnilgpqCcz4ADU_dXz8AAAA&hl=fr&mat=CTwYNcFS4u2pElYBEKoLaRW9D448Y0J2D36M_WJQ5mZgMYCgUANJZ9Cr-f3Ny0ITvrINtNIBuLEgWxCz2-O26MMao-sGASfCclntgiTr6jX4GJDAD86tUb5LQ96YsGkxRg&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1IxqEgxNTQxNDdISrIwTDY3s7QCiqSZmxsYGaZamFskJlkaGixiFXbOzynNTSotVnBOTDu8UkFNwTkfAARoGmo-AAAA&hl=fr&mat=CbHVxF-AWSJcElYBEKoLabN3tP5LUYVpIlDtfUs2zl3eeknp9ekk1J21PGsyXsraklWmsV6jhUuQhCPnsJ830-YFM8Qv1vSSOry5SX3cgtfaEUcxdSECQfmk2B-39DBwvQ&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co+Beauvais&stick=H4sIAAAAAAAA_-NgU1I1qDAxTzU3MDcxNEgzSEkxMk6yMqgwN7NMNDE2MTIwNUm2sEwxWcQq45yfU5qbVFqs4JyYdnilgpqCc76CU2piaVliZjEAPU9oJ0gAAAA&hl=fr&mat=CWmsktRhjPOxElcBEKoLaYLoIgrXZl1q78BAviKCriitJXb4vQjv_r7cmo8AoafHyR-suO7Oz5fbZbu0KcgPPJIwjCPJCcC_VcBSkG4tD3YtFDfrW7FO2VreXmhsbdF7tcE&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1IxqEgxNTUys7RINktKMjY0TrEyqEi2sLQ0TzE2TjQyMUpMTklaxCrsnJ9TmptUWqzgnJh2eKWCmoJzPgBHakRrPgAAAA&hl=fr&mat=CXWnrh_v0W-hElcBEKoLacx3qYp6kUrkuKKZtLAgPVFVrCJe-0KC52chwXT1h-R2Y8PxdQ6moGrARlOeQlWihzcPI8tB2jhk9UxIAZI9kfjW8qRz0G0zahltKleEuTTivPw&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDAxtzQyTrZMSzEyMTFPTkmzMqhINktLNjJONTAxMzY1MUo0XsQq7JyfU5qbVFqs4JyYdnilgpqCcz4AqWav1z8AAAA&hl=fr&mat=CVGMXV45gWyzElcBEKoLaXMZL-ei48djZ0O1NTNlpPHDVISQr9oC1Y4sjZeWp5svxj1HYLUtNDiKyOv635WXnT7EsnmgCYLhLwa0ODoZ8Am-lW4Mmkx-Yarn10k6avTek50&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co&stick=H4sIAAAAAAAA_-NgU1I1qDAxt0gxMzZOSTZINDAyT06zMqhIS0s2TjMyNjK0tEwxS7ZMXcQq7JyfU5qbVFqs4JyYdnilgpqCcz4Ah8sahz8AAAA&hl=fr&mat=CXMzbEL-ZC3eElcBEKoLaSebXW6knmJTZuww7ATJ5lMgzWoC81pVxYo1D9oDkKo5iV0g44y9QPWlJn-wzY0bB_fUy2JRuf2_mxuHybAWXtgNc00h1n5esH_n0fYozE05oW8&authuser=0",
    "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co+B%C3%A9ziers&stick=H4sIAAAAAAAA_-NgU1I1qDA0SjI0SEs2STIxNzROSrK0AgqlJpoZGpikpKUYJBqnJacsYpVxzs8pzU0qLVZwTkw7vFJBTcE5X8Hp8MqqzNSiYgBC092SSAAAAA&hl=fr&mat=Cc5i_GFNfC8HElcBEKoLaWMEvZRRT1AQxacSK4Z_SQC1XtLuhCBcXuBIxqZ5gM_bK1UhbjzXaEEG3VtTJ_JD23OCNRGT-uWKjaJZTnWIzOxmg38zNV7phGkMDh2hvU7Zcnc&authuser=0"
    
]

# Préparer une liste pour stocker les résultats
results = []

# Traiter chaque URL
for url in urls:
    data = extract_data(url)
    results.append(data)

# Convertir les résultats en DataFrame
results_df = pd.DataFrame(results)

# Nom du fichier CSV de sortie
output_csv = 'extracted_info.csv'

# Vérifier si le fichier existe déjà
if os.path.exists(output_csv):
    # Ajouter les nouvelles données à la fin du fichier existant sans réécrire les anciennes données
    results_df.to_csv(output_csv, mode='a', header=False, index=False)
else:
    # Si le fichier n'existe pas, créer un nouveau fichier avec l'en-tête
    results_df.to_csv(output_csv, mode='w', header=True, index=False)

# Fermer le navigateur
driver.quit()
