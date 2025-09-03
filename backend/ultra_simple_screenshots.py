#!/usr/bin/env python3
"""
Script ULTRA SIMPLE pour 4 captures d'écran
GET, POST, PUT + Météo
"""

import requests
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import os

def create_simple_screenshot(title, data, method="GET", status="200"):
    """Créer une capture simple"""
    # Image basique
    img = Image.new('RGB', (800, 500), color='#2b2b2b')
    draw = ImageDraw.Draw(img)
    
    # Police simple
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
        font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # En-tête
    color = '#4CAF50' if status == '200' else '#FF9800'
    draw.rectangle([0, 0, 800, 60], fill=color)
    
    # Titre
    draw.text((20, 15), f"🌐 {title}", fill='#ffffff', font=font_large)
    draw.text((20, 40), f"{method} | Status: {status}", fill='#ffffff', font=font_small)
    
    # Contenu
    y = 80
    if isinstance(data, dict):
        for key, value in list(data.items())[:8]:
            draw.text((20, y), f"🔑 {key}: {str(value)[:50]}", fill='#81C784', font=font_small)
            y += 25
    
    # Sauvegarder
    filename = f"{method.lower()}_{title.lower().replace(' ', '_')}.png"
    img.save(filename)
    print(f"📸 {filename}")
    return filename

def create_meteo_graph():
    """Créer graphique météo simple"""
    # Données d'exemple
    hours = [f"{i}h" for i in range(24)]
    waves = [1.2, 1.5, 1.8, 2.1, 2.3, 2.0, 1.7, 1.4, 1.1, 0.9, 0.8, 1.0, 
             1.3, 1.6, 1.9, 2.2, 2.4, 2.1, 1.8, 1.5, 1.2, 1.0, 0.9, 1.1]
    temps = [18, 17, 16, 15, 14, 13, 12, 11, 12, 14, 16, 18, 
             20, 22, 24, 25, 26, 25, 24, 22, 20, 19, 18, 17]
    
    # Graphique
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    fig.patch.set_facecolor('#2b2b2b')
    
    # Vagues
    ax1.plot(hours, waves, 'b-', linewidth=2, marker='o')
    ax1.set_title('Vagues (m)', color='white')
    ax1.set_facecolor('#2b2b2b')
    ax1.tick_params(colors='white')
    
    # Température
    ax2.plot(hours, temps, 'r-', linewidth=2, marker='o')
    ax2.set_title('Temperature (C)', color='white')
    ax2.set_facecolor('#2b2b2b')
    ax2.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('4_meteo_result.png', facecolor='#2b2b2b', dpi=150)
    plt.close()
    
    print("📸 4_meteo_result.png")
    return '4_meteo_result.png'

def main():
    """Fonction principale - 4 captures simples"""
    print("🚀 4 Captures Ultra-Simples")
    print("=" * 40)
    
    # 1. GET - Spots
    print("\n🔍 1. GET - Spots de surf...")
    try:
        response = requests.get("http://localhost:8000/api/surf-spots/")
        if response.status_code == 200:
            create_simple_screenshot("Liste des Spots", response.json(), "GET", "200")
        else:
            create_simple_screenshot("Liste des Spots", {"error": "Erreur"}, "GET", str(response.status_code))
    except:
        create_simple_screenshot("Liste des Spots", {"error": "Pas de connexion"}, "GET", "ERROR")
    
    # 2. POST - Utilisateur
    print("\n📝 2. POST - Création utilisateur...")
    try:
        user_data = {"email": "test@test.com", "password": "test123"}
        response = requests.post("http://localhost:8000/api/user/register/", json=user_data)
        if response.status_code in [200, 201]:
            create_simple_screenshot("Creation Utilisateur", {"message": "Utilisateur créé"}, "POST", "201")
        else:
            create_simple_screenshot("Creation Utilisateur", {"error": "Erreur"}, "POST", str(response.status_code))
    except:
        create_simple_screenshot("Creation Utilisateur", {"error": "Pas de connexion"}, "POST", "ERROR")
    
    # 3. PUT - Mise à jour
    print("\n✏️  3. PUT - Mise à jour utilisateur...")
    try:
        update_data = {"first_name": "Modifié"}
        response = requests.put("http://localhost:8000/api/surfer/profile/", json=update_data)
        if response.status_code == 200:
            create_simple_screenshot("Mise a Jour Utilisateur", {"message": "Profil mis à jour"}, "PUT", "200")
        else:
            create_simple_screenshot("Mise a Jour Utilisateur", {"error": "Erreur"}, "PUT", str(response.status_code))
    except:
        create_simple_screenshot("Mise a Jour Utilisateur", {"error": "Pas de connexion"}, "PUT", "ERROR")
    
    # 4. Météo
    print("\n🌤️  4. Graphique météo...")
    create_meteo_graph()
    
    # Résumé
    print("\n" + "=" * 40)
    print("📊 4 CAPTURES CRÉÉES")
    print("=" * 40)
    
    screenshots = [f for f in os.listdir('.') if f.endswith('.png')]
    for screenshot in screenshots:
        print(f"✅ {screenshot}")
    
    print("\n🎉 Terminé ! 4 captures créées")

if __name__ == "__main__":
    main()
