from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.scraper import extract_data
import pandas as pd
import os
import json
import io

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/results', methods=['POST'])
def results():
    # Récupérer les URLs soumises par l'utilisateur
    urls = request.form['urls']
    
    # Diviser les URLs par ligne et supprimer les espaces vides
    url_list = [url.strip() for url in urls.splitlines() if url.strip()]

    # Créer un DataFrame pour stocker les résultats
    all_data = []

    for url in url_list:
        data = extract_data(url)
        all_data.append(data)

    # Enregistrer les résultats dans un fichier CSV
    output_csv = 'data/extracted_info.csv'
    results_df = pd.DataFrame(all_data)
    if os.path.exists(output_csv):
        results_df.to_csv(output_csv, mode='a', header=False, index=False)
    else:
        results_df.to_csv(output_csv, mode='w', header=True, index=False)

    return render_template('results.html', data=all_data)

# Route to export data to CSV
@main.route('/export')
def export():
    file_path = os.path.join('data', 'extracted_info.csv')
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='text/csv', as_attachment=True, download_name='extracted_info.csv')
    else:
        return "Le fichier CSV n'existe pas", 404

@main.route('/view_csv')
def view_csv():
    file_path = os.path.join('data', 'extracted_info.csv')

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data = df.to_dict(orient='records')
        
        # Paramètres de pagination
        page = request.args.get('page', 1, type=int)  # Page courante, par défaut 1
        per_page = 30  # Nombre de lignes par page
        total = len(data)  # Total des lignes
        
        # Calculer les données à afficher pour la page courante
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = data[start:end]

        # Calculer le nombre de pages
        total_pages = (total + per_page - 1) // per_page  # Arrondi vers le haut

        return render_template(
            'view.html',
            data=paginated_data,
            page=page,
            total_pages=total_pages
        )
    else:
        return "Le fichier CSV n'existe pas", 404
