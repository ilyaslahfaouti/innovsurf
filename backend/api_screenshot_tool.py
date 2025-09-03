#!/usr/bin/env python3
"""
Outil de capture d'écran pour les APIs InnovSurf
Permet de tester et documenter visuellement toutes les APIs
"""

import requests
import json
import time
import os
from datetime import datetime
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "surf_spots": "/api/surf-spots/",
    "surf_spot_detail": "/api/surf-spots/1/",
    "forecast": "/api/surf-spots/prevision/1/",
    "surf_clubs": "/api/surf-clubs/1/lessons/",
    "surf_club_equipments": "/api/surf-clubs/1/equipments/",
    "surf_club_profile": "/api/surf-club/profile/",
    "surf_club_monitors": "/api/surf-club/monitors/",
    "surf_club_equipments": "/api/surf-club/equipments/",
    "surf_club_lesson_schedules": "/api/surf-club/lesson-schedules/",
    "surf_club_surf_lessons": "/api/surf-club/surf-lessons/",
    "surf_club_surf_sessions": "/api/surf-club/surf-sessions/",
    "surf_club_orders": "/api/surf-club/orders/",
    "surf_club_statistics": "/api/surf-club/statistics/",
    "surfer_profile": "/api/surfer/profile/",
    "surfer_book_lesson": "/api/surfers/book_surf_lesson/",
    "surfer_create_order": "/api/surfers/add-order/",
    "chatbot": "/api/chatbot/",
    "chatbot_faq": "/api/chatbot/faq/",
    "chatbot_analytics": "/api/chatbot/analytics/",
    "windy_forecast": "/api/windy/forecast/",
    "windy_optimal_times": "/api/windy/optimal-times/",
    "windy_conditions_summary": "/api/windy/conditions-summary/",
    "ai_demand_forecast": "/api/ai/demand-forecast/",
    "contact": "/api/contact/",
}

class APIScreenshotTool:
    def __init__(self, base_url=BASE_URL, output_dir="api_screenshots"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.access_token = None
        
        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # Configuration des headers
        self.session.headers.update({
            'User-Agent': 'InnovSurf-API-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def authenticate(self, username="test@innovsurf.com", password="testpass123"):
        """Authentification pour obtenir un token"""
        try:
            auth_url = f"{self.base_url}/api/token/"
            auth_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(auth_url, json=auth_data)
            
            if response.status_code == 200:
                self.access_token = response.json().get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                print(f"✅ Authentification réussie pour {username}")
                return True
            else:
                print(f"❌ Échec de l'authentification: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
            return False
    
    def test_endpoint(self, endpoint_name, endpoint_url, method="GET", data=None):
        """Tester un endpoint et retourner les résultats"""
        full_url = f"{self.base_url}{endpoint_url}"
        
        try:
            print(f"\n🔍 Test de {endpoint_name}: {full_url}")
            
            if method == "GET":
                response = self.session.get(full_url)
            elif method == "POST":
                response = self.session.post(full_url, json=data)
            elif method == "PUT":
                response = self.session.put(full_url, json=data)
            elif method == "DELETE":
                response = self.session.delete(full_url)
            
            # Analyser la réponse
            result = {
                "endpoint": endpoint_name,
                "url": full_url,
                "method": method,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "headers": dict(response.headers),
                "success": 200 <= response.status_code < 300
            }
            
            # Traiter le contenu de la réponse
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    result["data"] = response.json()
                    result["data_size"] = len(json.dumps(response.json()))
                else:
                    result["data"] = response.text[:1000]  # Limiter la taille
                    result["data_size"] = len(response.text)
            except:
                result["data"] = "Impossible de parser la réponse"
                result["data_size"] = 0
            
            # Afficher le résultat
            status_icon = "✅" if result["success"] else "❌"
            print(f"{status_icon} {endpoint_name}: {response.status_code} ({result['response_time']:.2f}s)")
            
            return result
            
        except Exception as e:
            error_result = {
                "endpoint": endpoint_name,
                "url": full_url,
                "method": method,
                "status_code": None,
                "response_time": 0,
                "headers": {},
                "success": False,
                "error": str(e),
                "data": None,
                "data_size": 0
            }
            print(f"❌ Erreur pour {endpoint_name}: {e}")
            return error_result
    
    def create_screenshot_image(self, test_results):
        """Créer une image de capture d'écran des résultats des tests"""
        # Dimensions de l'image
        width = 1200
        height = 800 + (len(test_results) * 100)
        
        # Créer l'image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Essayer de charger une police
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
            font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
        except:
            # Fallback vers la police par défaut
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Titre
        title = f"Test des APIs InnovSurf - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        draw.text((20, 20), title, fill='black', font=font_large)
        
        # Ligne de séparation
        draw.line([(20, 60), (width-20, 60)], fill='gray', width=2)
        
        y_position = 80
        
        # Résultats des tests
        for result in test_results:
            # En-tête de l'endpoint
            status_color = 'green' if result["success"] else 'red'
            status_icon = "✅" if result["success"] else "❌"
            
            endpoint_text = f"{status_icon} {result['endpoint']}"
            draw.text((20, y_position), endpoint_text, fill=status_color, font=font_medium)
            
            # Détails
            details = [
                f"URL: {result['url']}",
                f"Méthode: {result['method']}",
                f"Statut: {result['status_code']}",
                f"Temps: {result['response_time']:.2f}s",
                f"Taille: {result['data_size']} caractères"
            ]
            
            y_detail = y_position + 30
            for detail in details:
                draw.text((40, y_detail), detail, fill='black', font=font_small)
                y_detail += 20
            
            # Ligne de séparation
            y_position = y_detail + 10
            draw.line([(20, y_position), (width-20, y_position)], fill='lightgray', width=1)
            y_position += 20
        
        return img
    
    def save_results_json(self, test_results):
        """Sauvegarder les résultats au format JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/api_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats sauvegardés dans {filename}")
        return filename
    
    def save_screenshot(self, test_results):
        """Sauvegarder la capture d'écran"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/api_screenshot_{timestamp}.png"
        
        img = self.create_screenshot_image(test_results)
        img.save(filename)
        
        print(f"📸 Capture d'écran sauvegardée dans {filename}")
        return filename
    
    def generate_report(self, test_results):
        """Générer un rapport complet"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"{self.output_dir}/api_report_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Rapport de Test des APIs InnovSurf\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Résumé
            total_tests = len(test_results)
            successful_tests = sum(1 for r in test_results if r["success"])
            failed_tests = total_tests - successful_tests
            
            f.write(f"## Résumé\n\n")
            f.write(f"- **Total des tests:** {total_tests}\n")
            f.write(f"- **Tests réussis:** {successful_tests} ✅\n")
            f.write(f"- **Tests échoués:** {failed_tests} ❌\n")
            f.write(f"- **Taux de succès:** {(successful_tests/total_tests)*100:.1f}%\n\n")
            
            # Détails des tests
            f.write(f"## Détails des Tests\n\n")
            
            for result in test_results:
                status_icon = "✅" if result["success"] else "❌"
                f.write(f"### {status_icon} {result['endpoint']}\n\n")
                f.write(f"- **URL:** `{result['url']}`\n")
                f.write(f"- **Méthode:** {result['method']}\n")
                f.write(f"- **Statut:** {result['status_code']}\n")
                f.write(f"- **Temps de réponse:** {result['response_time']:.2f}s\n")
                f.write(f"- **Taille des données:** {result['data_size']} caractères\n\n")
                
                if not result["success"] and "error" in result:
                    f.write(f"**Erreur:** {result['error']}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Rapport généré dans {report_file}")
        return report_file
    
    def run_all_tests(self):
        """Exécuter tous les tests d'API"""
        print("🚀 Démarrage des tests des APIs InnovSurf")
        print("=" * 50)
        
        # Authentification
        if not self.authenticate():
            print("⚠️  Authentification échouée, tests sans authentification")
        
        # Tests des endpoints
        test_results = []
        
        for endpoint_name, endpoint_url in API_ENDPOINTS.items():
            result = self.test_endpoint(endpoint_name, endpoint_url)
            test_results.append(result)
            time.sleep(0.5)  # Pause entre les tests
        
        # Tests POST pour les endpoints qui le supportent
        post_tests = [
            ("add_monitor", "/api/surf-club/add-monitor/", {
                "name": "Test Monitor",
                "email": "test@example.com",
                "phone": "123456789",
                "experience_years": 5
            }),
            ("add_equipment", "/api/surf-club/add-equipment/", {
                "name": "Test Board",
                "type": "surfboard",
                "quantity": 1,
                "price": 100.0
            }),
            ("add_lesson_schedule", "/api/surf-club/add-lesson-schedule/", {
                "day": "monday",
                "start_time": "09:00",
                "end_time": "10:00",
                "max_students": 5
            }),
            ("book_surf_lesson", "/api/surfers/book_surf_lesson/", {
                "lesson_schedule_id": 1,
                "surfer_id": 1,
                "date": "2024-12-25"
            }),
            ("create_order", "/api/surfers/add-order/", {
                "surfer_id": 1,
                "total_amount": 150.0,
                "items": []
            }),
            ("create_message", "/api/forums/1/messages/create/", {
                "content": "Test message",
                "author_id": 1
            })
        ]
        
        for test_name, test_url, test_data in post_tests:
            result = self.test_endpoint(test_name, test_url, "POST", test_data)
            test_results.append(result)
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print("📊 Résultats des tests")
        print("=" * 50)
        
        # Statistiques
        total_tests = len(test_results)
        successful_tests = sum(1 for r in test_results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"Total des tests: {total_tests}")
        print(f"Tests réussis: {successful_tests} ✅")
        print(f"Tests échoués: {failed_tests} ❌")
        print(f"Taux de succès: {(successful_tests/total_tests)*100:.1f}%")
        
        # Sauvegarder les résultats
        self.save_results_json(test_results)
        self.save_screenshot(test_results)
        self.generate_report(test_results)
        
        return test_results

def main():
    """Fonction principale"""
    print("🖼️  Outil de Capture d'Écran des APIs InnovSurf")
    print("=" * 60)
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=5)
        print(f"✅ Serveur accessible à {BASE_URL}")
    except:
        print(f"❌ Serveur non accessible à {BASE_URL}")
        print("Assurez-vous que votre serveur Django est démarré")
        return
    
    # Créer et exécuter l'outil
    tool = APIScreenshotTool()
    results = tool.run_all_tests()
    
    print("\n🎉 Tests terminés !")
    print(f"Consultez le dossier '{tool.output_dir}' pour les résultats")

if __name__ == "__main__":
    main()
