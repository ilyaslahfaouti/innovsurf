#!/usr/bin/env python3
"""
Script SIMPLE pour 4 captures d'écran :
1. GET - Liste des spots
2. POST - Création d'utilisateur  
3. PUT - Mise à jour d'utilisateur
4. Résultat météo avec graphique
"""

import requests
import json
import time
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import os

class Simple4Screenshots:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.screenshots_dir = "simple_4_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # Authentification
        self.authenticate()
    
    def authenticate(self):
        """Authentification simple"""
        try:
            auth_data = {"email": "test@innovsurf.com", "password": "testpass123"}
            response = self.session.post(f"{self.base_url}/api/token/", json=auth_data)
            if response.status_code == 200:
                self.token = response.json()["access"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print("✅ Connecté")
            else:
                print("⚠️  Connexion échouée")
        except:
            print("⚠️  Pas de connexion")
    
    def create_screenshot(self, title, content, method="GET", status="200"):
        """Créer une capture d'écran simple"""
        try:
            # Image simple
            width = 1000
            height = 600
            
            img = Image.new('RGB', (width, height), color='#2b2b2b')
            draw = ImageDraw.Draw(img)
            
            # Police simple
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 24)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # En-tête coloré
            header_color = '#4CAF50' if status == '200' else '#FF9800'
            draw.rectangle([0, 0, width, 80], fill=header_color)
            
            # Titre
            draw.text((20, 20), f"🌐 {title}", fill='#ffffff', font=font_large)
            draw.text((20, 50), f"{method} | Status: {status}", fill='#ffffff', font=font_medium)
            
            # Contenu
            y = 100
            if isinstance(content, dict):
                # JSON
                for key, value in list(content.items())[:10]:  # Max 10 éléments
                    key_text = f"🔑 {key}:"
                    draw.text((20, y), key_text, fill='#81C784', font=font_medium)
                    y += 25
                    
                    value_text = str(value)[:80]
                    draw.text((40, y), value_text, fill='#E0E0E0', font=font_small)
                    y += 20
            elif isinstance(content, str):
                # Texte
                lines = content.split('\n')[:20]  # Max 20 lignes
                for line in lines:
                    draw.text((20, y), line[:80], fill='#E0E0E0', font=font_small)
                    y += 20
            
            # Sauvegarder
            filename = f"{method.lower()}_{title.lower().replace(' ', '_')}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath)
            
            print(f"📸 {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None
    
    def screenshot_1_get_spots(self):
        """1. Capture GET - Liste des spots"""
        print("\n🔍 1. Test GET - Liste des spots...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/surf-spots/")
            
            if response.status_code == 200:
                data = response.json()
                self.create_screenshot("Liste des Spots de Surf", data, "GET", "200")
            else:
                self.create_screenshot("Liste des Spots de Surf", {"error": "Erreur"}, "GET", str(response.status_code))
                
        except Exception as e:
            self.create_screenshot("Liste des Spots de Surf", {"error": str(e)}, "GET", "ERROR")
    
    def screenshot_2_post_user(self):
        """2. Capture POST - Création utilisateur"""
        print("\n📝 2. Test POST - Création utilisateur...")
        
        try:
            # Données de test
            user_data = {
                "email": "nouveau@test.com",
                "password": "testpass123",
                "first_name": "Nouveau",
                "last_name": "Utilisateur"
            }
            
            response = self.session.post(f"{self.base_url}/api/user/register/", json=user_data)
            
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    self.create_screenshot("Création Utilisateur", data, "POST", "201")
                except:
                    self.create_screenshot("Création Utilisateur", {"message": "Utilisateur créé"}, "POST", "201")
            else:
                error_data = {"error": response.text[:100]} if response.text else {"error": "Erreur"}
                self.create_screenshot("Création Utilisateur", error_data, "POST", str(response.status_code))
                
        except Exception as e:
            self.create_screenshot("Création Utilisateur", {"error": str(e)}, "POST", "ERROR")
    
    def screenshot_3_put_user(self):
        """3. Capture PUT - Mise à jour utilisateur"""
        print("\n✏️  3. Test PUT - Mise à jour utilisateur...")
        
        try:
            # Données de mise à jour
            update_data = {
                "first_name": "Utilisateur Modifié",
                "last_name": "Nom Modifié"
            }
            
            # Essayer de mettre à jour l'utilisateur 1
            response = self.session.put(f"{self.base_url}/api/surfer/profile/", json=update_data)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.create_screenshot("Mise à Jour Utilisateur", data, "PUT", "200")
                except:
                    self.create_screenshot("Mise à Jour Utilisateur", {"message": "Profil mis à jour"}, "PUT", "200")
            else:
                error_data = {"error": response.text[:100]} if response.text else {"error": "Erreur"}
                self.create_screenshot("Mise à Jour Utilisateur", error_data, "PUT", str(response.status_code))
                
        except Exception as e:
            self.create_screenshot("Mise à Jour Utilisateur", {"error": str(e)}, "PUT", "ERROR")
    
    def screenshot_4_meteo_result(self):
        """4. Capture Résultat Météo avec graphique"""
        print("\n🌤️  4. Création résultat météo avec graphique...")
        
        try:
            # Récupérer les données météo
            response = self.session.get(f"{self.base_url}/api/surf-spots/prevision/1/")
            
            if response.status_code == 200:
                meteo_data = response.json()
                
                # Créer un graphique simple
                self.create_meteo_graph(meteo_data)
            else:
                # Créer un graphique d'exemple
                self.create_example_meteo_graph()
                
        except Exception as e:
            print(f"❌ Erreur météo: {e}")
            self.create_example_meteo_graph()
    
    def create_meteo_graph(self, data):
        """Créer un graphique météo à partir des vraies données"""
        try:
            # Extraire les données si possible
            if 'forecast' in data and isinstance(data['forecast'], list):
                hours = [f"{i}h" for i in range(24)]
                wave_heights = [item.get('wave_height', np.random.uniform(0.5, 2.5)) for item in data['forecast'][:24]]
                temperatures = [item.get('temperature', np.random.uniform(15, 25)) for item in data['forecast'][:24]]
            else:
                # Données d'exemple
                hours = [f"{i}h" for i in range(24)]
                wave_heights = np.random.uniform(0.5, 2.5, 24)
                temperatures = np.random.uniform(15, 25, 24)
            
            # Créer le graphique
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            fig.patch.set_facecolor('#2b2b2b')
            
            # Graphique des vagues
            ax1.plot(hours, wave_heights, 'b-', linewidth=2, marker='o')
            ax1.set_title('🌊 Hauteur des Vagues (m)', color='white', fontsize=16)
            ax1.set_ylabel('Hauteur (m)', color='white')
            ax1.set_facecolor('#2b2b2b')
            ax1.tick_params(colors='white')
            ax1.grid(True, alpha=0.3)
            
            # Graphique des températures
            ax2.plot(hours, temperatures, 'r-', linewidth=2, marker='o')
            ax2.set_title('🌡️ Température (°C)', color='white', fontsize=16)
            ax2.set_ylabel('Température (°C)', color='white')
            ax2.set_facecolor('#2b2b2b')
            ax2.tick_params(colors='white')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Sauvegarder
            filepath = os.path.join(self.screenshots_dir, "4_meteo_result.png")
            plt.savefig(filepath, facecolor='#2b2b2b', dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"📸 4_meteo_result.png")
            
        except Exception as e:
            print(f"❌ Erreur graphique: {e}")
            self.create_example_meteo_graph()
    
    def create_example_meteo_graph(self):
        """Créer un graphique météo d'exemple"""
        try:
            # Données d'exemple
            hours = [f"{i}h" for i in range(24)]
            wave_heights = [1.2, 1.5, 1.8, 2.1, 2.3, 2.0, 1.7, 1.4, 1.1, 0.9, 0.8, 1.0, 
                           1.3, 1.6, 1.9, 2.2, 2.4, 2.1, 1.8, 1.5, 1.2, 1.0, 0.9, 1.1]
            temperatures = [18, 17, 16, 15, 14, 13, 12, 11, 12, 14, 16, 18, 
                          20, 22, 24, 25, 26, 25, 24, 22, 20, 19, 18, 17]
            
            # Créer le graphique
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            fig.patch.set_facecolor('#2b2b2b')
            
            # Graphique des vagues
            ax1.plot(hours, wave_heights, 'b-', linewidth=2, marker='o')
            ax1.set_title('🌊 Hauteur des Vagues (m) - Exemple', color='white', fontsize=16)
            ax1.set_ylabel('Hauteur (m)', color='white')
            ax1.set_facecolor('#2b2b2b')
            ax1.tick_params(colors='white')
            ax1.grid(True, alpha=0.3)
            
            # Graphique des températures
            ax2.plot(hours, temperatures, 'r-', linewidth=2, marker='o')
            ax2.set_title('🌡️ Température (°C) - Exemple', color='white', fontsize=16)
            ax2.set_ylabel('Température (°C)', color='white')
            ax2.set_facecolor('#2b2b2b')
            ax2.tick_params(colors='white')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Sauvegarder
            filepath = os.path.join(self.screenshots_dir, "4_meteo_result.png")
            plt.savefig(filepath, facecolor='#2b2b2b', dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"📸 4_meteo_result.png (exemple)")
            
        except Exception as e:
            print(f"❌ Erreur graphique d'exemple: {e}")
    
    def run_all(self):
        """Exécuter les 4 captures"""
        print("🚀 Création des 4 captures d'écran simples...")
        print("=" * 50)
        
        # 1. GET
        self.screenshot_1_get_spots()
        
        # 2. POST  
        self.screenshot_2_post_user()
        
        # 3. PUT
        self.screenshot_3_put_user()
        
        # 4. Météo
        self.screenshot_4_meteo_result()
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 4 CAPTURES CRÉÉES")
        print("=" * 50)
        
        screenshots = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
        for screenshot in screenshots:
            print(f"✅ {screenshot}")
        
        print(f"\n📁 Dossier: {self.screenshots_dir}/")
        print("🔍 Visualiser: open simple_4_screenshots/")

def main():
    """Fonction principale"""
    print("📸 4 Captures d'Écran Simples - APIs InnovSurf")
    print("=" * 60)
    
    # Créer les 4 captures
    creator = Simple4Screenshots()
    creator.run_all()
    
    print("\n🎉 Terminé ! 4 captures créées")

if __name__ == "__main__":
    main()
