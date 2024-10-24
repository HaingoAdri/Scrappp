import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    # Lancement du navigateur en mode headless (sans interface graphique)
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    # URL à visiter
    url = "https://www.google.com/search?q=Columbus+Caf%C3%A9+%26+Co+Carcassonne&stick=H4sIAAAAAAAA_-NgU1I1qDA0Skw1SrFMTElMS0mxTDK2MqhIM7IwNza2MEwysDA2skxNW8Qq75yfU5qbVFqs4JyYdnilgpqCcz6QWZScWFycn5eXCgDq6LyBSwAAAA&hl=fr&mat=CWVjN1UBJTEbElcBEKoLab-3b9Y60C3p7VUN7YOYdM7KbmX4K2-Eb-BNrrxIE-wtYtSD2QIwazF0arle49jHf8UvJ23cwm0_D0_u9WB8yuUNrpFRMIt79mEInyf-0MI9Yj4&authuser=0"
    await page.goto(url)

    # Dictionnaire pour stocker les informations extraites
    info = {'URL': url}

    try:
        # Nom Google
        try:
            div_element = await page.query_selector('div.PZPZlf.ssJ7i.xgAzOe, div.PZPZlf.ssJ7i.B5dxMb')
            if div_element:
                info['Nom Google'] = await div_element.inner_text()
            else:
                info['Nom Google'] = "Non trouvé"
        except Exception:
            info['Nom Google'] = "Non trouvé"

        # Adresse
        try:
            span_element = await page.query_selector('span.LrzXr')
            if span_element:
                info['Adresse'] = await span_element.inner_text()
            else:
                info['Adresse'] = "Non trouvée"
        except Exception:
            info['Adresse'] = "Non trouvée"

        # Numéro de téléphone
        try:
            phone_link = await page.query_selector('a[data-dtype="d3ph"]')
            if phone_link:
                info['Numéro de téléphone'] = await phone_link.inner_text()
            else:
                info['Numéro de téléphone'] = "Non trouvé"
        except Exception:
            info['Numéro de téléphone'] = "Non trouvé"

        # URL du lien
        try:
            a_element = await page.query_selector('a.n1obkb.mI8Pwc')
            if a_element:
                info['URL du lien'] = await a_element.get_attribute('href')
            else:
                info['URL du lien'] = "Non trouvé"
        except Exception:
            info['URL du lien'] = "Non trouvé"

        # Horaires d'ouverture
        try:
            table = await page.query_selector('//table[contains(@class, "WgFkxc")]')
            if table:
                rows = await table.query_selector_all('tr')
                horaires = []
                for row in rows:
                    cells = await row.query_selector_all('td')
                    if len(cells) >= 2:  # S'assure qu'il y a au moins deux cellules
                        day = await cells[0].inner_text()
                        hours = await cells[1].inner_text()
                        horaires.append({'Jour': day, 'Horaires': hours})
                info['Horaires'] = horaires
            else:
                info['Horaires'] = "Non trouvés"
        except Exception:
            info['Horaires'] = "Non trouvés"

    except Exception as e:
        print(f"Erreur lors de l'extraction des données : {e}")

    # Affichage des informations extraites
    print(info)

    # Fermeture du navigateur
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

# Exécution de l'extraction
asyncio.run(main())
