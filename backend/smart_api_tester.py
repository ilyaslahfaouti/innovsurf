#!/usr/bin/env python3
"""
Testeur Intelligent des APIs InnovSurf
Gère l'authentification et les erreurs de manière intelligente
"""

import requests
import json
import time
import os
from datetime import datetime

class SmartAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        self.access_token = None
        
        # Configuration des headers
        self.session.headers.update({
            'User-Agent': 'InnovSurf-Smart-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def authenticate(self, username="test@innovsurf.com", password="testpass123"):
        """Authentification intelligente"""
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
                print(f"⚠️  Authentification échouée: {response.status_code}")
                print("   Tests sans authentification (certains endpoints peuvent échouer)")
                return False
                
        except Exception as e:
            print(f"⚠️  Erreur d'authentification: {e}")
            print("   Tests sans authentification")
            return False
    
    def test_endpoint_smart(self, name, url, method="GET", data=None, requires_auth=False):
        """Test intelligent d'un endpoint avec gestion des erreurs"""
        full_url = f"{self.base_url}{url}"
        
        try:
            print(f"🔍 Test de {name}...")
            
            # Vérifier si l'authentification est requise
            if requires_auth and not self.access_token:
                result = {
                    "name": name,
                    "url": full_url,
                    "method": method,
                    "status_code": 401,
                    "success": False,
                    "response_time": 0,
                    "error": "Authentification requise",
                    "data": None,
                    "data_size": 0,
                    "skipped": True
                }
                print(f"⏭️  {name}: Authentification requise (ignoré)")
                self.results.append(result)
                return result
            
            # Effectuer la requête
            start_time = time.time()
            
            if method == "GET":
                response = self.session.get(full_url)
            elif method == "POST":
                response = self.session.post(full_url, json=data)
            
            response_time = time.time() - start_time
            
            # Analyser la réponse
            result = {
                "name": name,
                "url": full_url,
                "method": method,
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 300,
                "response_time": response_time,
                "error": None,
                "data": None,
                "data_size": 0,
                "skipped": False
            }
            
            # Traiter le contenu de la réponse
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
            
            # Gérer les erreurs communes
            if response.status_code == 401:
                result["error"] = "Non autorisé - authentification requise"
            elif response.status_code == 403:
                result["error"] = "Accès interdit - permissions insuffisantes"
            elif response.status_code == 404:
                result["error"] = "Endpoint non trouvé - vérifier l'URL"
            elif response.status_code == 500:
                result["error"] = "Erreur serveur interne"
            elif response.status_code >= 400:
                result["error"] = f"Erreur client: {response.status_code}"
            
            # Afficher le résultat
            if result["success"]:
                icon = "✅"
                print(f"{icon} {name}: {response.status_code} ({result['response_time']:.2f}s)")
            else:
                icon = "❌"
                error_msg = result["error"] or f"HTTP {response.status_code}"
                print(f"{icon} {name}: {error_msg} ({result['response_time']:.2f}s)")
            
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
                "data_size": 0,
                "skipped": False
            }
            print(f"❌ {name}: Erreur - {e}")
            self.results.append(error_result)
            return error_result
    
    def run_smart_tests(self):
        """Exécuter les tests de manière intelligente"""
        print("🧠 Tests Intelligents des APIs InnovSurf")
        print("=" * 50)
        
        # Authentification
        self.authenticate()
        
        # Tests GET - Endpoints publics
        print("\n🌐 Tests des endpoints publics:")
        public_endpoints = [
            ("Spots de surf", "/api/surf-spots/", False),
            ("Détail spot", "/api/surf-spots/1/", False),
            ("Prévisions", "/api/surf-spots/prevision/1/", False),
            ("Contact", "/api/contact/", False),
        ]
        
        for name, url, requires_auth in public_endpoints:
            self.test_endpoint_smart(name, url, requires_auth=requires_auth)
            time.sleep(0.2)
        
        # Tests GET - Endpoints avec authentification
        print("\n🔐 Tests des endpoints avec authentification:")
        auth_endpoints = [
            ("Profil club", "/api/surf-club/profile/", True),
            ("Moniteurs", "/api/surf-club/monitors/", True),
            ("Équipements", "/api/surf-club/equipments/", True),
            ("Horaires leçons", "/api/surf-club/lesson-schedules/", True),
            ("Leçons surf", "/api/surf-club/surf-lessons/", True),
            ("Sessions surf", "/api/surf-club/surf-sessions/", True),
            ("Commandes", "/api/surf-club/orders/", True),
            ("Statistiques", "/api/surf-club/statistics/", True),
            ("Profil surfeur", "/api/surfer/profile/", True),
        ]
        
        for name, url, requires_auth in auth_endpoints:
            self.test_endpoint_smart(name, url, requires_auth=requires_auth)
            time.sleep(0.2)
        
        # Tests GET - Endpoints spéciaux
        print("\n🤖 Tests des endpoints spéciaux:")
        special_endpoints = [
            ("Chatbot", "/api/chatbot/", False),
            ("Chatbot FAQ", "/api/chatbot/faq/", False),
            ("Chatbot Analytics", "/api/chatbot/analytics/", False),
            ("Windy Forecast", "/api/windy/forecast/", False),
            ("Windy Optimal Times", "/api/windy/optimal-times/", False),
            ("Windy Conditions", "/api/windy/conditions-summary/", False),
            ("IA Forecast", "/api/ai/demand-forecast/", False),
        ]
        
        for name, url, requires_auth in special_endpoints:
            self.test_endpoint_smart(name, url, requires_auth=requires_auth)
            time.sleep(0.2)
        
        # Tests POST
        print("\n📝 Tests des endpoints POST:")
        post_tests = [
            ("Ajouter moniteur", "/api/surf-club/add-monitor/", {
                "name": "Test Monitor",
                "email": "test@example.com",
                "phone": "123456789",
                "experience_years": 5
            }, True),
            ("Ajouter équipement", "/api/surf-club/add-equipment/", {
                "name": "Test Board",
                "type": "surfboard",
                "quantity": 1,
                "price": 100.0
            }, True),
            ("Réserver leçon", "/api/surfers/book_surf_lesson/", {
                "lesson_schedule_id": 1,
                "surfer_id": 1,
                "date": "2024-12-25"
            }, True),
            ("Créer commande", "/api/surfers/add-order/", {
                "surfer_id": 1,
                "total_amount": 150.0,
                "items": []
            }, True),
        ]
        
        for name, url, data, requires_auth in post_tests:
            self.test_endpoint_smart(name, url, "POST", data, requires_auth)
            time.sleep(0.2)
    
    def generate_smart_report(self):
        """Générer un rapport intelligent"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"smart_api_report_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Rapport Intelligent des Tests d'API InnovSurf\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Statistiques globales
            total = len(self.results)
            success = sum(1 for r in self.results if r["success"])
            failed = sum(1 for r in self.results if r["success"] == False and not r.get("skipped"))
            skipped = sum(1 for r in self.results if r.get("skipped"))
            
            f.write(f"## 📊 Résumé Global\n\n")
            f.write(f"- **Total des tests:** {total}\n")
            f.write(f"- **Tests réussis:** {success} ✅\n")
            f.write(f"- **Tests échoués:** {failed} ❌\n")
            f.write(f"- **Tests ignorés:** {skipped} ⏭️\n")
            f.write(f"- **Taux de succès:** {(success/(total-skipped)*100):.1f}% (hors ignorés)\n\n")
            
            # Analyse par catégorie
            f.write(f"## 🏷️ Analyse par Catégorie\n\n")
            
            categories = {
                "Endpoints Publics": [r for r in self.results if "spots" in r["name"].lower() or "contact" in r["name"].lower()],
                "Endpoints Club": [r for r in self.results if "club" in r["name"].lower()],
                "Endpoints Surfeur": [r for r in self.results if "surfer" in r["name"].lower()],
                "Endpoints Spéciaux": [r for r in self.results if "chatbot" in r["name"].lower() or "windy" in r["name"].lower() or "ia" in r["name"].lower()],
                "Tests POST": [r for r in self.results if r["method"] == "POST"]
            }
            
            for category, results in categories.items():
                if results:
                    cat_success = sum(1 for r in results if r["success"])
                    cat_total = len(results)
                    cat_skipped = sum(1 for r in results if r.get("skipped"))
                    cat_rate = (cat_success/(cat_total-cat_skipped)*100) if (cat_total-cat_skipped) > 0 else 0
                    
                    f.write(f"### {category}\n")
                    f.write(f"- **Tests:** {cat_total} (dont {cat_skipped} ignorés)\n")
                    f.write(f"- **Succès:** {cat_success} ✅\n")
                    f.write(f"- **Taux:** {cat_rate:.1f}%\n\n")
            
            # Détails des tests
            f.write(f"## 📋 Détails des Tests\n\n")
            
            for result in self.results:
                if result.get("skipped"):
                    icon = "⏭️"
                    status = "Ignoré"
                elif result["success"]:
                    icon = "✅"
                    status = "Succès"
                else:
                    icon = "❌"
                    status = "Échec"
                
                f.write(f"### {icon} {result['name']}\n\n")
                f.write(f"- **Statut:** {status}\n")
                f.write(f"- **URL:** `{result['url']}`\n")
                f.write(f"- **Méthode:** {result['method']}\n")
                f.write(f"- **Code HTTP:** {result['status_code']}\n")
                f.write(f"- **Temps:** {result['response_time']:.2f}s\n")
                f.write(f"- **Taille:** {result['data_size']} caractères\n\n")
                
                if result["error"]:
                    f.write(f"**Erreur:** {result['error']}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Rapport intelligent généré: {report_file}")
        return report_file
    
    def save_results_json(self):
        """Sauvegarder les résultats en JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"smart_api_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résultats JSON sauvegardés: {filename}")
        return filename
    
    def print_summary(self):
        """Afficher un résumé des résultats"""
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        total = len(self.results)
        success = sum(1 for r in self.results if r["success"])
        failed = sum(1 for r in self.results if r["success"] == False and not r.get("skipped"))
        skipped = sum(1 for r in self.results if r.get("skipped"))
        
        print(f"Total des tests: {total}")
        print(f"Tests réussis: {success} ✅")
        print(f"Tests échoués: {failed} ❌")
        print(f"Tests ignorés: {skipped} ⏭️")
        
        if (total - skipped) > 0:
            success_rate = (success / (total - skipped)) * 100
            print(f"Taux de succès: {success_rate:.1f}% (hors ignorés)")
        
        # Suggestions d'amélioration
        if failed > 0:
            print(f"\n💡 Suggestions d'amélioration:")
            if failed > success:
                print("   - Vérifiez la configuration de votre serveur Django")
                print("   - Assurez-vous que toutes les migrations sont appliquées")
                print("   - Vérifiez les permissions des utilisateurs")
            else:
                print("   - La plupart des APIs fonctionnent correctement")
                print("   - Quelques endpoints nécessitent une configuration")

def main():
    """Fonction principale"""
    print("🧠 Testeur Intelligent des APIs InnovSurf")
    print("=" * 60)
    
    # Vérifier le serveur
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        print("✅ Serveur accessible")
    except:
        print("❌ Serveur non accessible")
        print("Démarrez votre serveur Django d'abord")
        return
    
    # Créer et exécuter le testeur
    tester = SmartAPITester()
    tester.run_smart_tests()
    
    # Générer les rapports
    tester.generate_smart_report()
    tester.save_results_json()
    
    # Afficher le résumé
    tester.print_summary()
    
    print("\n🎉 Tests terminés !")
    print("Consultez les rapports générés pour plus de détails")

if __name__ == "__main__":
    main()
