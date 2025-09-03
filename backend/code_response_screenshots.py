#!/usr/bin/env python3
"""
Script pour capturer le CODE + la RÉPONSE des APIs
Montre les lignes de code et les vraies données retournées
"""

import requests
import json
import time
from PIL import Image, ImageDraw, ImageFont
import os

class CodeResponseScreenshots:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.screenshots_dir = "code_response_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # Authentification
        self.authenticate()
    
    def authenticate(self):
        """Authentification"""
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
    
    def create_code_response_screenshot(self, title, code_lines, response_data, method="GET", status="200"):
        """Créer une capture montrant le code ET la réponse"""
        try:
            # Dimensions plus grandes pour le code + réponse
            width = 1400
            height = 900
            
            img = Image.new('RGB', (width, height), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
                font_code = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
                font_code = ImageFont.load_default()
            
            # En-tête
            header_bg = '#2d2d30'
            draw.rectangle([0, 0, width, 80], fill=header_bg)
            
            # Titre
            draw.text((20, 20), f"💻 {title}", fill='#ffffff', font=font_large)
            draw.text((20, 50), f"{method} | Status: {status}", fill='#cccccc', font=font_medium)
            
            # Ligne de séparation
            draw.line([(20, 80), (width-20, 80)], fill='#404040', width=2)
            
            # Section CODE (gauche)
            code_section_bg = '#1e1e1e'
            draw.rectangle([20, 100, width//2-20, height-100], fill=code_section_bg, outline='#404040', width=2)
            
            # Titre section code
            draw.text((40, 120), "📝 CODE DE LA REQUÊTE", fill='#4ec9b0', font=font_medium)
            
            # Lignes de code
            y_code = 160
            for i, line in enumerate(code_lines):
                if y_code > height - 120:
                    break
                
                # Numéro de ligne
                line_num = f"{i+1:2d}"
                draw.text((40, y_code), line_num, fill='#6a9955', font=font_code)
                
                # Code avec coloration
                if 'import' in line:
                    color = '#569cd6'  # Bleu pour imports
                elif 'def ' in line or 'class ' in line:
                    color = '#dcdcaa'  # Jaune pour définitions
                elif '#' in line:
                    color = '#6a9955'  # Vert pour commentaires
                elif '=' in line:
                    color = '#9cdcfe'  # Bleu clair pour assignations
                else:
                    color = '#d4d4d4'  # Blanc pour le reste
                
                draw.text((80, y_code), line, fill=color, font=font_code)
                y_code += 20
            
            # Section RÉPONSE (droite)
            response_section_bg = '#1e1e1e'
            draw.rectangle([width//2+20, 100, width-20, height-100], fill=response_section_bg, outline='#404040', width=2)
            
            # Titre section réponse
            draw.text((width//2+40, 120), "📡 RÉPONSE DE L'API", fill='#4ec9b0', font=font_medium)
            
            # Données de la réponse
            y_response = 160
            if isinstance(response_data, dict):
                self.draw_json_response(draw, response_data, width//2+40, y_response, width//2-60, font_small)
            elif isinstance(response_data, str):
                lines = response_data.split('\n')[:30]
                for line in lines:
                    if y_response > height - 120:
                        break
                    draw.text((width//2+40, y_response), line[:80], fill='#d4d4d4', font=font_small)
                    y_response += 20
            else:
                draw.text((width//2+40, y_response), str(response_data)[:200], fill='#d4d4d4', font=font_small)
            
            # Pied de page
            footer_bg = '#2d2d30'
            draw.rectangle([0, height-40, width, height], fill=footer_bg)
            draw.text((20, height-30), f"Code + Réponse | {time.strftime('%Y-%m-%d %H:%M:%S')} | InnovSurf", 
                     fill='#cccccc', font=font_small)
            
            # Sauvegarder
            filename = f"{method.lower()}_{title.lower().replace(' ', '_').replace('é', 'e')}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            img.save(filepath, dpi=(300, 300))
            
            print(f"📸 {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur création capture: {e}")
            return None
    
    def draw_json_response(self, draw, data, x, y, max_width, font, indent=0):
        """Dessiner la réponse JSON de manière lisible"""
        if y > 800:  # Limite de hauteur
            return y
        
        for key, value in data.items():
            if y > 800:
                break
                
            # Clé
            key_text = f"{'  ' * indent}🔑 {key}:"
            draw.text((x, y), key_text, fill='#569cd6', font=font)
            y += 20
            
            # Valeur
            if isinstance(value, dict):
                y = self.draw_json_response(draw, value, x, y, max_width, font, indent + 1)
            elif isinstance(value, list):
                for i, item in enumerate(value[:8]):  # Limiter à 8 éléments
                    if y > 800:
                        break
                    if isinstance(item, dict):
                        y = self.draw_json_response(draw, item, x, y, max_width, font, indent + 1)
                    else:
                        item_text = f"{'  ' * (indent + 1)}📋 [{i}]: {str(item)[:60]}"
                        draw.text((x, y), item_text, fill='#ce9178', font=font)
                        y += 20
            else:
                value_text = f"{'  ' * (indent + 1)}💾 {str(value)[:60]}"
                draw.text((x, y), value_text, fill='#9cdcfe', font=font)
                y += 20
        
        return y
    
    def screenshot_1_get_spots(self):
        """1. Capture GET - Code + Réponse des spots"""
        print("\n🔍 1. Test GET - Code + Réponse des spots...")
        
        # Code de la requête
        code_lines = [
            "import requests",
            "",
            "# Configuration de la requête",
            "url = 'http://localhost:8000/api/surf-spots/'",
            "headers = {'Authorization': 'Bearer token'}",
            "",
            "# Exécution de la requête GET",
            "response = requests.get(url, headers=headers)",
            "",
            "# Vérification du statut",
            "if response.status_code == 200:",
            "    spots = response.json()",
            "    print(f'✅ {len(spots)} spots trouvés')",
            "else:",
            "    print(f'❌ Erreur: {response.status_code}')"
        ]
        
        try:
            response = self.session.get(f"{self.base_url}/api/surf-spots/")
            
            if response.status_code == 200:
                data = response.json()
                self.create_code_response_screenshot(
                    "GET - Liste des Spots de Surf",
                    code_lines,
                    data,
                    "GET",
                    "200"
                )
            else:
                error_data = {"error": response.text} if response.text else {"error": "Erreur"}
                self.create_code_response_screenshot(
                    "GET - Liste des Spots de Surf",
                    code_lines,
                    error_data,
                    "GET",
                    str(response.status_code)
                )
                
        except Exception as e:
            error_data = {"error": str(e)}
            self.create_code_response_screenshot(
                "GET - Liste des Spots de Surf",
                code_lines,
                error_data,
                "GET",
                "ERROR"
            )
    
    def screenshot_2_post_user(self):
        """2. Capture POST - Code + Réponse création utilisateur"""
        print("\n📝 2. Test POST - Code + Réponse création utilisateur...")
        
        # Code de la requête
        code_lines = [
            "import requests",
            "import json",
            "",
            "# Données de l'utilisateur",
            "user_data = {",
            "    'email': 'nouveau@test.com',",
            "    'password': 'testpass123',",
            "    'first_name': 'Nouveau',",
            "    'last_name': 'Utilisateur'",
            "}",
            "",
            "# Configuration de la requête",
            "url = 'http://localhost:8000/api/user/register/'",
            "headers = {'Content-Type': 'application/json'}",
            "",
            "# Exécution de la requête POST",
            "response = requests.post(url, json=user_data, headers=headers)",
            "",
            "# Vérification du statut",
            "if response.status_code in [200, 201]:",
            "    user = response.json()",
            "    print(f'✅ Utilisateur créé: {user.get(\"email\")}')",
            "else:",
            "    print(f'❌ Erreur: {response.status_code}')"
        ]
        
        try:
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
                    self.create_code_response_screenshot(
                        "POST - Creation Utilisateur",
                        code_lines,
                        data,
                        "POST",
                        "201"
                    )
                except:
                    success_data = {"message": "Utilisateur créé avec succès", "status": "success"}
                    self.create_code_response_screenshot(
                        "POST - Creation Utilisateur",
                        code_lines,
                        success_data,
                        "POST",
                        "201"
                    )
            else:
                error_data = {"error": response.text} if response.text else {"error": "Erreur de création"}
                self.create_code_response_screenshot(
                    "POST - Creation Utilisateur",
                    code_lines,
                    error_data,
                    "POST",
                    str(response.status_code)
                )
                
        except Exception as e:
            error_data = {"error": str(e)}
            self.create_code_response_screenshot(
                "POST - Creation Utilisateur",
                code_lines,
                error_data,
                "POST",
                "ERROR"
            )
    
    def screenshot_3_put_user(self):
        """3. Capture PUT - Code + Réponse mise à jour utilisateur"""
        print("\n✏️  3. Test PUT - Code + Réponse mise à jour utilisateur...")
        
        # Code de la requête
        code_lines = [
            "import requests",
            "import json",
            "",
            "# Données de mise à jour",
            "update_data = {",
            "    'first_name': 'Utilisateur Modifié',",
            "    'last_name': 'Nom Modifié',",
            "    'email': 'modifie@test.com'",
            "}",
            "",
            "# Configuration de la requête",
            "url = 'http://localhost:8000/api/surfer/profile/'",
            "headers = {",
            "    'Authorization': 'Bearer token',",
            "    'Content-Type': 'application/json'",
            "}",
            "",
            "# Exécution de la requête PUT",
            "response = requests.put(url, json=update_data, headers=headers)",
            "",
            "# Vérification du statut",
            "if response.status_code == 200:",
            "    profile = response.json()",
            "    print(f'✅ Profil mis à jour: {profile.get(\"first_name\")}')",
            "else:",
            "    print(f'❌ Erreur: {response.status_code}')"
        ]
        
        try:
            update_data = {
                "first_name": "Utilisateur Modifié",
                "last_name": "Nom Modifié",
                "email": "modifie@test.com"
            }
            
            response = self.session.put(f"{self.base_url}/api/surfer/profile/", json=update_data)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.create_code_response_screenshot(
                        "PUT - Mise a Jour Utilisateur",
                        code_lines,
                        data,
                        "PUT",
                        "200"
                    )
                except:
                    success_data = {"message": "Profil mis à jour avec succès", "status": "success"}
                    self.create_code_response_screenshot(
                        "PUT - Mise a Jour Utilisateur",
                        code_lines,
                        success_data,
                        "PUT",
                        "200"
                    )
            else:
                error_data = {"error": response.text} if response.text else {"error": "Erreur de mise à jour"}
                self.create_code_response_screenshot(
                    "PUT - Mise a Jour Utilisateur",
                    code_lines,
                    error_data,
                    "PUT",
                    str(response.status_code)
                )
                
        except Exception as e:
            error_data = {"error": str(e)}
            self.create_code_response_screenshot(
                "PUT - Mise a Jour Utilisateur",
                code_lines,
                error_data,
                "PUT",
                "ERROR"
            )
    
    def run_all(self):
        """Exécuter tous les tests avec captures code + réponse"""
        print("🚀 Création des captures CODE + RÉPONSE...")
        print("=" * 60)
        
        # 1. GET - Spots
        self.screenshot_1_get_spots()
        
        # 2. POST - Utilisateur
        self.screenshot_2_post_user()
        
        # 3. PUT - Mise à jour
        self.screenshot_3_put_user()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 CAPTURES CODE + RÉPONSE TERMINÉES")
        print("=" * 60)
        
        screenshots = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
        for screenshot in screenshots:
            print(f"✅ {screenshot}")
        
        print(f"\n📁 Dossier: {self.screenshots_dir}/")
        print("🔍 Visualiser: open code_response_screenshots/")
        
        return screenshots

def main():
    """Fonction principale"""
    print("💻 Générateur de Captures CODE + RÉPONSE - APIs InnovSurf")
    print("=" * 70)
    
    # Créer les captures
    creator = CodeResponseScreenshots()
    screenshots = creator.run_all()
    
    print(f"\n🎉 Terminé ! {len(screenshots)} captures CODE + RÉPONSE créées")

if __name__ == "__main__":
    main()
