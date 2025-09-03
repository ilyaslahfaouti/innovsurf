#!/usr/bin/env python3
"""
Testeur simple des APIs InnovSurf avec captures d'écran
Version simplifiée pour tests rapides
"""

import requests
import json
import time
import os
from datetime import datetime

class SimpleAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
        # Configuration des headers
        self.session.headers.update({
            'User-Agent': 'InnovSurf-Simple-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def test_endpoint(self, name, url, method="GET", data=None):
        """Tester un endpoint simple"""
        full_url = f"{self.base_url}{url}"
        
        try:
            print(f"🔍 Test de {name}...")
            
            if method == "GET":
                response = self.session.get(full_url)
            elif method == "POST":
                response = self.session.post(full_url, json=data)
            
            result = {
                "name": name,
                "url": full_url,
                "method": method,
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 300,
                "response_time": response.elapsed.total_seconds()
            }
            
            # Analyser la réponse
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    result["data"] = response.json()
                    result["data_size"] = len(json.dumps(response.json()))
                else:
                    result["data"] = response.text[:200]
                    result["data_size"] = len(response.text)
            except:
                result["data"] = "Erreur de parsing"
                result["data_size"] = 0
            
            # Afficher le résultat
            icon = "✅" if result["success"] else "❌"
            print(f"{icon} {name}: {response.status_code} ({result['response_time']:.2f}s)")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "name": name,
                "url": full_url,
                "method": method,
                "status_code": None,
                "success": False,
                "response_time": 0,
                "error": str(e),
                "data": None,
                "data_size": 0
            }
            print(f"❌ {name}: Erreur - {e}")
            self.results.append(error_result)
            return error_result
    
    def run_basic_tests(self):
        """Exécuter les tests de base"""
        print("🚀 Tests de base des APIs InnovSurf")
        print("=" * 40)
        
        # Tests GET
        endpoints = [
            ("Spots de surf", "/api/surf-spots/"),
            ("Détail spot", "/api/surf-spots/1/"),
            ("Prévisions", "/api/surf-spots/prevision/1/"),
            ("Profil club", "/api/surf-club/profile/"),
            ("Moniteurs", "/api/surf-club/monitors/"),
            ("Équipements", "/api/surf-club/equipments/"),
            ("Horaires leçons", "/api/surf-club/lesson-schedules/"),
            ("Leçons surf", "/api/surf-club/surf-lessons/"),
            ("Sessions surf", "/api/surf-club/surf-sessions/"),
            ("Commandes", "/api/surf-club/orders/"),
            ("Statistiques", "/api/surf-club/statistics/"),
            ("Profil surfeur", "/api/surfer/profile/"),
            ("Chatbot", "/api/chatbot/"),
            ("Chatbot FAQ", "/api/chatbot/faq/"),
            ("Chatbot Analytics", "/api/chatbot/analytics/"),
            ("Windy Forecast", "/api/windy/forecast/"),
            ("Windy Optimal Times", "/api/windy/optimal-times/"),
            ("Windy Conditions", "/api/windy/conditions-summary/"),
            ("IA Forecast", "/api/ai/demand-forecast/"),
            ("Contact", "/api/contact/"),
        ]
        
        for name, url in endpoints:
            self.test_endpoint(name, url)
            time.sleep(0.3)  # Pause courte
        
        # Tests POST
        post_tests = [
            ("Ajouter moniteur", "/api/surf-club/add-monitor/", {
                "name": "Test Monitor",
                "email": "test@example.com",
                "phone": "123456789",
                "experience_years": 5
            }),
            ("Ajouter équipement", "/api/surf-club/add-equipment/", {
                "name": "Test Board",
                "type": "surfboard",
                "quantity": 1,
                "price": 100.0
            }),
            ("Réserver leçon", "/api/surfers/book_surf_lesson/", {
                "lesson_schedule_id": 1,
                "surfer_id": 1,
                "date": "2024-12-25"
            }),
            ("Créer commande", "/api/surfers/add-order/", {
                "surfer_id": 1,
                "total_amount": 150.0,
                "items": []
            })
        ]
        
        for name, url, data in post_tests:
            self.test_endpoint(name, url, "POST", data)
            time.sleep(0.3)
    
    def generate_simple_report(self):
        """Générer un rapport simple"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"simple_api_report_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Rapport Simple des Tests d'API\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Résumé
            total = len(self.results)
            success = sum(1 for r in self.results if r["success"])
            failed = total - success
            
            f.write(f"## Résumé\n\n")
            f.write(f"- **Total:** {total}\n")
            f.write(f"- **Succès:** {success} ✅\n")
            f.write(f"- **Échecs:** {failed} ❌\n")
            f.write(f"- **Taux:** {(success/total)*100:.1f}%\n\n")
            
            # Détails
            f.write(f"## Détails\n\n")
            for result in self.results:
                icon = "✅" if result["success"] else "❌"
                f.write(f"### {icon} {result['name']}\n\n")
                f.write(f"- **URL:** `{result['url']}`\n")
                f.write(f"- **Méthode:** {result['method']}\n")
                f.write(f"- **Statut:** {result['status_code']}\n")
                f.write(f"- **Temps:** {result['response_time']:.2f}s\n")
                f.write(f"- **Taille:** {result['data_size']} caractères\n\n")
                
                if not result["success"] and "error" in result:
                    f.write(f"**Erreur:** {result['error']}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Rapport simple généré: {report_file}")
        return report_file
    
    def save_results_json(self):
        """Sauvegarder les résultats en JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"simple_api_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats JSON sauvegardés: {filename}")
        return filename

def main():
    """Fonction principale"""
    print("🖼️  Testeur Simple des APIs InnovSurf")
    print("=" * 50)
    
    # Vérifier le serveur
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        print("✅ Serveur accessible")
    except:
        print("❌ Serveur non accessible")
        print("Démarrez votre serveur Django d'abord")
        return
    
    # Créer et exécuter le testeur
    tester = SimpleAPITester()
    tester.run_basic_tests()
    
    # Générer les rapports
    tester.generate_simple_report()
    tester.save_results_json()
    
    print("\n🎉 Tests terminés !")
    
    # Afficher le résumé
    total = len(tester.results)
    success = sum(1 for r in tester.results if r["success"])
    print(f"\n📊 Résumé: {success}/{total} APIs fonctionnent ✅")

if __name__ == "__main__":
    main()
