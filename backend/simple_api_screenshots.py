#!/usr/bin/env python3
"""
Script simple pour capturer les résultats visuels des APIs
GET, POST, PUT avec captures d'écran des réponses
"""

import requests
import json
import time
from PIL import Image, ImageDraw, ImageFont
import os

class SimpleAPIScreenshots:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.screenshots_dir = "api_result_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # Endpoints à tester
        self.endpoints = {
            "GET": [
                ("/api/surf-spots/", "Liste des spots de surf"),
                ("/api/surf-spots/1/", "Détail d'un spot"),
                ("/api/surf-spots/prevision/1/", "Prévision météo"),
                ("/api/surf-clubs/1/lessons/", "Cours disponibles"),
                ("/api/surf-clubs/1/equipments/", "Équipements disponibles")
            ],
            "POST": [
                ("/api/surfers/book_surf_lesson/", "Réservation de cours", {
                    "surfer_id": 1,
                    "lesson_id": 1,
                    "date": "2025-08-28"
                }),
                ("/api/surfers/add-order/", "Création de commande", {
                    "surfer_id": 1,
                    "equipment_ids": [1, 2],
                    "total_amount": 50.00
                }),
                ("/api/contact/", "Formulaire de contact", {
                    "name": "Test User",
                    "email": "test@example.com",
                    "message": "Test de contact"
                })
            ]
        }
        
        # Authentification
        self.token = None
        self.authenticate()
    
    def authenticate(self):
        """Authentification pour obtenir un token"""
        try:
            auth_data = {
                "email": "test@innovsurf.com",
                "password": "testpass123"
            }
            
            response = self.session.post(f"{self.base_url}/api/token/", json=auth_data)
            if response.status_code == 200:
                self.token = response.json()["access"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print("✅ Authentification réussie")
            else:
                print("⚠️  Authentification échouée, tests publics uniquement")
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
    
    def create_screenshot(self, title, data, endpoint, method, status_code):
        """Créer une capture d'écran du résultat de l'API"""
        try:
            # Dimensions
            width = 1200
            height = 800
            
            # Créer l'image
            img = Image.new('RGB', (width, height), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # En-tête
            header_bg = '#2d2d30'
            draw.rectangle([0, 0, width, 100], fill=header_bg)
            
            # Titre
            draw.text((20, 20), f"🌐 {title}", fill='#ffffff', font=font_large)
            
            # Informations de l'API
            api_info = f"{method} {endpoint} | Status: {status_code}"
            draw.text((20, 50), api_info, fill='#cccccc', font=font_medium)
            
            # Timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            draw.text((20, 75), f"Testé le: {timestamp}", fill='#888888', font=font_small)
            
            # Ligne de séparation
            draw.line([(20, 100), (width-20, 100)], fill='#404040', width=2)
            
            # Contenu de la réponse
            y_position = 120
            
            if isinstance(data, dict):
                # Données JSON
                self.draw_json_data(draw, data, 20, y_position, width-40, font_small)
            elif isinstance(data, str):
                # Données texte
                lines = data.split('\n')
                for line in lines[:30]:  # Limiter à 30 lignes
                    if y_position > height - 50:
                        break
                    draw.text((20, y_position), line[:100], fill='#d4d4d4', font=font_small)
                    y_position += 20
            else:
                # Autres types
                draw.text((20, y_position), str(data)[:200], fill='#d4d4d4', font=font_small)
            
            # Pied de page
            footer_bg = '#2d2d30'
            draw.rectangle([0, height-40, width, height], fill=footer_bg)
            draw.text((20, height-30), f"API Test Result | InnovSurf", fill='#cccccc', font=font_small)
            
            # Sauvegarder
            filename = f"{method.lower()}_{endpoint.replace('/', '_').replace('api_', '')}_{int(time.time())}.png"
            filename = filename.replace('__', '_').replace('_.png', '.png')
            filepath = os.path.join(self.screenshots_dir, filename)
            
            img.save(filepath, dpi=(300, 300))
            print(f"📸 Capture sauvegardée: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur création capture: {e}")
            return None
    
    def draw_json_data(self, draw, data, x, y, max_width, font, indent=0):
        """Dessiner les données JSON de manière lisible"""
        if y > 750:  # Limite de hauteur
            return y
        
        for key, value in data.items():
            if y > 750:
                break
                
            # Clé
            key_text = f"{'  ' * indent}🔑 {key}:"
            draw.text((x, y), key_text, fill='#569cd6', font=font)
            y += 20
            
            # Valeur
            if isinstance(value, dict):
                y = self.draw_json_data(draw, value, x, y, max_width, font, indent + 1)
            elif isinstance(value, list):
                for i, item in enumerate(value[:5]):  # Limiter à 5 éléments
                    if y > 750:
                        break
                    if isinstance(item, dict):
                        y = self.draw_json_data(draw, item, x, y, max_width, font, indent + 1)
                    else:
                        item_text = f"{'  ' * (indent + 1)}📋 [{i}]: {str(item)[:80]}"
                        draw.text((x, y), item_text, fill='#ce9178', font=font)
                        y += 20
            else:
                value_text = f"{'  ' * (indent + 1)}💾 {str(value)[:80]}"
                draw.text((x, y), value_text, fill='#9cdcfe', font=font)
                y += 20
        
        return y
    
    def test_get_endpoints(self):
        """Tester tous les endpoints GET"""
        print("\n🔍 Test des endpoints GET...")
        
        for endpoint, description in self.endpoints["GET"]:
            try:
                print(f"\n📡 Test: {description}")
                print(f"   URL: {endpoint}")
                
                response = self.session.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès - {len(str(data))} caractères")
                    
                    # Créer capture d'écran
                    self.create_screenshot(
                        description,
                        data,
                        endpoint,
                        "GET",
                        response.status_code
                    )
                else:
                    print(f"   ❌ Échec - Status: {response.status_code}")
                    if response.text:
                        print(f"   Erreur: {response.text[:100]}")
                    
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
    
    def test_post_endpoints(self):
        """Tester tous les endpoints POST"""
        print("\n📝 Test des endpoints POST...")
        
        for endpoint, description, data in self.endpoints["POST"]:
            try:
                print(f"\n📡 Test: {description}")
                print(f"   URL: {endpoint}")
                print(f"   Données: {data}")
                
                response = self.session.post(f"{self.base_url}{endpoint}", json=data)
                
                if response.status_code in [200, 201]:
                    try:
                        response_data = response.json()
                        print(f"   ✅ Succès - {len(str(response_data))} caractères")
                    except:
                        response_data = response.text
                        print(f"   ✅ Succès - Réponse texte")
                    
                    # Créer capture d'écran
                    self.create_screenshot(
                        description,
                        response_data,
                        endpoint,
                        "POST",
                        response.status_code
                    )
                else:
                    print(f"   ❌ Échec - Status: {response.status_code}")
                    if response.text:
                        print(f"   Erreur: {response.text[:100]}")
                    
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
    
    def create_summary_screenshot(self):
        """Créer une capture d'ensemble de tous les résultats"""
        try:
            print("\n📊 Création de la capture d'ensemble...")
            
            # Dimensions
            width = 1400
            height = 1000
            
            # Créer l'image
            img = Image.new('RGB', (width, height), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 24)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Titre
            title = "📊 Résultats des Tests d'APIs InnovSurf"
            draw.text((width//2 - len(title)*8, 30), title, fill='#ffffff', font=font_large)
            
            # Ligne de séparation
            draw.line([(50, 80), (width-50, 80)], fill='#404040', width=3)
            
            # Description
            description = "Captures d'écran des résultats réels des APIs (GET, POST)"
            draw.text((width//2 - len(description)*6, 110), description, fill='#cccccc', font=font_medium)
            
            # Résumé des tests
            y_position = 160
            
            # Tests GET
            draw.text((50, y_position), "🔍 Tests GET (Lecture de données)", fill='#4ec9b0', font=font_medium)
            y_position += 40
            
            for endpoint, description in self.endpoints["GET"]:
                test_info = f"  📡 {description}"
                draw.text((70, y_position), test_info, fill='#d4d4d4', font=font_small)
                y_position += 25
            
            y_position += 20
            
            # Tests POST
            draw.text((50, y_position), "📝 Tests POST (Création de données)", fill='#4ec9b0', font=font_medium)
            y_position += 40
            
            for endpoint, description, data in self.endpoints["POST"]:
                test_info = f"  📡 {description}"
                draw.text((70, y_position), test_info, fill='#d4d4d4', font=font_small)
                y_position += 25
            
            # Instructions
            y_position += 40
            draw.line([(50, y_position), (width-50, y_position)], fill='#404040', width=2)
            y_position += 30
            
            instructions = [
                "🎯 Utilisation:",
                "  • Les captures sont dans: api_result_screenshots/",
                "  • Chaque test génère une image PNG",
                "  • Format: METHODE_ENDPOINT_TIMESTAMP.png",
                "",
                "🔑 Authentification:",
                "  • Email: test@innovsurf.com",
                "  • Password: testpass123",
                "",
                "📱 Visualisation:",
                "  • Ouvrir le dossier: open api_result_screenshots/"
            ]
            
            for instruction in instructions:
                if instruction.strip():
                    if instruction.startswith("🎯") or instruction.startswith("🔑") or instruction.startswith("📱"):
                        color = '#4ec9b0'
                        font = font_medium
                    elif instruction.startswith("  •"):
                        color = '#d4d4d4'
                        font = font_small
                    else:
                        color = '#cccccc'
                        font = font_small
                    
                    draw.text((50, y_position), instruction, fill=color, font=font)
                    y_position += 25
            
            # Pied de page
            footer_bg = '#2d2d30'
            draw.rectangle([0, height-60, width, height], fill=footer_bg)
            draw.text((50, height-40), f"Généré le {time.strftime('%Y-%m-%d %H:%M:%S')} | Tests APIs InnovSurf", 
                     fill='#cccccc', font=font_small)
            
            # Sauvegarder
            output_filename = os.path.join(self.screenshots_dir, "OVERVIEW_api_results.png")
            img.save(output_filename, dpi=(300, 300))
            
            print(f"✅ Capture d'ensemble sauvegardée: OVERVIEW_api_results.png")
            return output_filename
            
        except Exception as e:
            print(f"❌ Erreur création capture d'ensemble: {e}")
            return None
    
    def run_all_tests(self):
        """Exécuter tous les tests et créer les captures"""
        print("🚀 Démarrage des tests d'APIs avec captures d'écran...")
        print("=" * 60)
        
        # Créer la capture d'ensemble
        self.create_summary_screenshot()
        
        # Tester les endpoints GET
        self.test_get_endpoints()
        
        # Tester les endpoints POST
        self.test_post_endpoints()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 TESTS TERMINÉS - CAPTURES CRÉÉES")
        print("=" * 60)
        
        # Compter les captures
        screenshots = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
        print(f"Total des captures: {len(screenshots)}")
        
        for screenshot in screenshots:
            print(f"✅ {screenshot}")
        
        print(f"\n📁 Toutes les captures sont dans: {self.screenshots_dir}/")
        print("🔍 Pour les visualiser: open api_result_screenshots/")
        
        return screenshots

def main():
    """Fonction principale"""
    print("📸 Générateur de Captures d'Écran des Résultats d'APIs")
    print("=" * 70)
    
    # Créer le testeur
    tester = SimpleAPIScreenshots()
    
    # Exécuter tous les tests
    screenshots = tester.run_all_tests()
    
    print(f"\n🎉 Terminé ! {len(screenshots)} captures générées")

if __name__ == "__main__":
    main()
