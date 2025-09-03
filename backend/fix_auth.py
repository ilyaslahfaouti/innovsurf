#!/usr/bin/env python3
"""
Script de correction de l'authentification et test des APIs
Corrige le problème d'authentification avec CustomUser
"""

import requests
import json
import time
from datetime import datetime

class FixedAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        
        # Configuration des headers
        self.session.headers.update({
            'User-Agent': 'InnovSurf-Fixed-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def authenticate_with_email(self, email, password):
        """Authentification en utilisant l'email"""
        try:
            # Essayer d'abord avec email
            auth_url = f"{self.base_url}/api/token/"
            auth_data = {
                "email": email,
                "password": password
            }
            
            print(f"🔐 Tentative d'authentification avec email: {email}")
            response = self.session.post(auth_url, json=auth_data)
            
            if response.status_code == 200:
                self.access_token = response.json().get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                print(f"✅ Authentification réussie avec email")
                return True
            else:
                print(f"❌ Authentification avec email échouée: {response.status_code}")
                print(f"   Réponse: {response.text}")
                
                # Essayer avec username (fallback)
                auth_data = {
                    "username": email,
                    "password": password
                }
                
                print(f"🔄 Tentative avec username: {email}")
                response = self.session.post(auth_url, json=auth_data)
                
                if response.status_code == 200:
                    self.access_token = response.json().get('access')
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.access_token}'
                    })
                    print(f"✅ Authentification réussie avec username")
                    return True
                else:
                    print(f"❌ Authentification avec username échouée: {response.status_code}")
                    print(f"   Réponse: {response.text}")
                    return False
                
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
            return False
    
    def test_endpoint_with_auth(self, name, url, method="GET", data=None):
        """Tester un endpoint avec authentification"""
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
                "response_time": response.elapsed.total_seconds(),
                "authenticated": bool(self.access_token)
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
            if result["success"]:
                icon = "✅"
                print(f"{icon} {name}: {response.status_code} ({result['response_time']:.2f}s)")
            else:
                icon = "❌"
                error_msg = f"HTTP {response.status_code}"
                if response.status_code == 401:
                    error_msg = "Non autorisé"
                elif response.status_code == 403:
                    error_msg = "Accès interdit"
                elif response.status_code == 404:
                    error_msg = "Non trouvé"
                elif response.status_code == 405:
                    error_msg = "Méthode non autorisée"
                
                print(f"{icon} {name}: {error_msg} ({result['response_time']:.2f}s)")
            
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
                "authenticated": bool(self.access_token)
            }
            print(f"❌ {name}: Erreur - {e}")
            return error_result
    
    def run_fixed_tests(self):
        """Exécuter les tests avec authentification corrigée"""
        print("🔧 Tests des APIs avec Authentification Corrigée")
        print("=" * 60)
        
        # Authentification
        if not self.authenticate_with_email("test@innovsurf.com", "testpass123"):
            print("❌ Impossible de s'authentifier")
            return
        
        print(f"\n🔑 Token d'accès obtenu: {self.access_token[:20]}...")
        
        # Tests des endpoints protégés
        print("\n🔐 Tests des endpoints avec authentification:")
        protected_endpoints = [
            ("Profil club", "/api/surf-club/profile/"),
            ("Moniteurs", "/api/surf-club/monitors/"),
            ("Équipements", "/api/surf-club/equipments/"),
            ("Horaires leçons", "/api/surf-club/lesson-schedules/"),
            ("Leçons surf", "/api/surf-club/surf-lessons/"),
            ("Sessions surf", "/api/surf-club/surf-sessions/"),
            ("Commandes", "/api/surf-club/orders/"),
            ("Statistiques", "/api/surf-club/statistics/"),
            ("Profil surfeur", "/api/surfer/profile/"),
        ]
        
        results = []
        for name, url in protected_endpoints:
            result = self.test_endpoint_with_auth(name, url)
            results.append(result)
            time.sleep(0.2)
        
        # Tests des endpoints publics
        print("\n🌐 Tests des endpoints publics:")
        public_endpoints = [
            ("Spots de surf", "/api/surf-spots/"),
            ("Détail spot", "/api/surf-spots/1/"),
            ("Prévisions", "/api/surf-spots/prevision/1/"),
            ("Contact", "/api/contact/"),
        ]
        
        for name, url in public_endpoints:
            result = self.test_endpoint_with_auth(name, url)
            results.append(result)
            time.sleep(0.2)
        
        # Tests des endpoints spéciaux
        print("\n🤖 Tests des endpoints spéciaux:")
        special_endpoints = [
            ("Chatbot", "/api/chatbot/"),
            ("Chatbot FAQ", "/api/chatbot/faq/"),
            ("Chatbot Analytics", "/api/chatbot/analytics/"),
            ("Windy Forecast", "/api/windy/forecast/"),
            ("Windy Optimal Times", "/api/windy/optimal-times/"),
            ("Windy Conditions", "/api/windy/conditions-summary/"),
            ("IA Forecast", "/api/ai/demand-forecast/"),
        ]
        
        for name, url in special_endpoints:
            result = self.test_endpoint_with_auth(name, url)
            results.append(result)
            time.sleep(0.2)
        
        # Tests POST
        print("\n📝 Tests des endpoints POST:")
        post_tests = [
            ("Ajouter moniteur", "/api/surf-club/add-monitor/", {
                "first_name": "Test",
                "last_name": "Monitor",
                "birthday": "1985-01-01",
                "active": True
            }),
            ("Ajouter équipement", "/api/surf-club/add-equipment/", {
                "name": "Test Board",
                "description": "Test Description",
                "size": "6'0",
                "state": "good",
                "material_type": "rent",
                "equipment_type_id": 1,
                "surf_club_id": 1,
                "rent_price": 50.0,
                "quantity": 1
            }),
        ]
        
        for name, url, data in post_tests:
            result = self.test_endpoint_with_auth(name, url, "POST", data)
            results.append(result)
            time.sleep(0.2)
        
        # Résumé
        self.print_summary(results)
        
        return results
    
    def print_summary(self, results):
        """Afficher un résumé des résultats"""
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS CORRIGÉS")
        print("=" * 50)
        
        total = len(results)
        success = sum(1 for r in results if r["success"])
        failed = total - success
        authenticated = sum(1 for r in results if r.get("authenticated"))
        
        print(f"Total des tests: {total}")
        print(f"Tests réussis: {success} ✅")
        print(f"Tests échoués: {failed} ❌")
        print(f"Tests authentifiés: {authenticated} 🔐")
        print(f"Taux de succès: {(success/total)*100:.1f}%")
        
        if success > failed:
            print(f"\n🎉 Excellent ! La plupart des APIs fonctionnent")
        elif success == failed:
            print(f"\n⚠️  Résultats mitigés, quelques APIs nécessitent une configuration")
        else:
            print(f"\n❌ Beaucoup d'APIs échouent, vérifiez la configuration")

def main():
    """Fonction principale"""
    print("🔧 Testeur d'APIs avec Authentification Corrigée")
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
    tester = FixedAPITester()
    results = tester.run_fixed_tests()
    
    print("\n🎉 Tests terminés !")
    print("Consultez les résultats ci-dessus pour l'état de vos APIs")

if __name__ == "__main__":
    main()
