#!/usr/bin/env python3
"""
Test spécifique de l'API Forecast avec captures d'écran
Teste l'endpoint de prévisions météorologiques
"""

import requests
import json
import time
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class ForecastAPITester:
    def __init__(self, base_url="http://localhost:8000", output_dir="forecast_screenshots"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.access_token = None
        
        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # Configuration des headers
        self.session.headers.update({
            'User-Agent': 'InnovSurf-Forecast-Tester/1.0',
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
    
    def get_surf_spots(self):
        """Récupérer la liste des spots de surf"""
        try:
            response = self.session.get(f"{self.base_url}/api/surf-spots/")
            if response.status_code == 200:
                spots = response.json()
                print(f"✅ {len(spots)} spots de surf trouvés")
                return spots
            else:
                print(f"❌ Erreur lors de la récupération des spots: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
    
    def test_forecast_endpoint(self, spot_id):
        """Tester l'endpoint de prévisions pour un spot spécifique"""
        endpoint_url = f"/api/surf-spots/prevision/{spot_id}/"
        full_url = f"{self.base_url}{endpoint_url}"
        
        print(f"\n🔍 Test de l'endpoint forecast pour le spot {spot_id}")
        print(f"URL: {full_url}")
        
        try:
            start_time = time.time()
            response = self.session.get(full_url)
            response_time = time.time() - start_time
            
            print(f"⏱️  Temps de réponse: {response_time:.2f}s")
            print(f"📊 Statut HTTP: {response.status_code}")
            
            # Analyser la réponse
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Données reçues avec succès")
                    
                    # Analyser la structure des données
                    self.analyze_forecast_data(data, spot_id)
                    
                    return {
                        "success": True,
                        "data": data,
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
                    
                except json.JSONDecodeError:
                    print(f"❌ Erreur de décodage JSON")
                    return {
                        "success": False,
                        "error": "Erreur de décodage JSON",
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Message d'erreur: {error_data}")
                except:
                    print(f"Message d'erreur: {response.text}")
                
                return {
                    "success": False,
                    "error": f"Erreur HTTP {response.status_code}",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête: {e}")
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "status_code": None
            }
    
    def analyze_forecast_data(self, data, spot_id):
        """Analyser la structure des données de prévisions"""
        print(f"\n📋 Analyse des données de prévisions pour le spot {spot_id}")
        
        # Vérifier la structure générale
        if "forecast" in data:
            forecast = data["forecast"]
            print(f"✅ Données de prévisions trouvées")
            
            # Vérifier les métadonnées
            if "meta" in forecast:
                meta = forecast["meta"]
                print(f"📊 Métadonnées:")
                print(f"   - Quota quotidien: {meta.get('dailyQuota', 'N/A')}")
                print(f"   - Requêtes utilisées: {meta.get('requestCount', 'N/A')}")
                print(f"   - Requêtes restantes: {meta.get('dailyQuota', 0) - meta.get('requestCount', 0)}")
            
            # Vérifier les erreurs
            if "errors" in forecast:
                errors = forecast["errors"]
                print(f"⚠️  Erreurs détectées:")
                for key, value in errors.items():
                    print(f"   - {key}: {value}")
            
            # Vérifier les données météorologiques
            if "data" in forecast:
                weather_data = forecast["data"]
                print(f"🌤️  Données météorologiques:")
                
                for param_name, param_data in weather_data.items():
                    if isinstance(param_data, list):
                        print(f"   - {param_name}: {len(param_data)} points de données")
                        if param_data:
                            first_point = param_data[0]
                            print(f"     Premier point: {first_point}")
                    else:
                        print(f"   - {param_name}: {type(param_data)}")
            
            # Vérifier le format alternatif
            elif "hours" in forecast:
                hours = forecast["hours"]
                print(f"⏰ Données par heure: {len(hours)} heures")
                if hours:
                    print(f"   Premier point: {hours[0]}")
        
        # Informations du spot
        if "name" in data:
            print(f"🏄 Spot: {data['name']}")
        if "address" in data:
            print(f"📍 Adresse: {data['address']}")
        if "latitude" in data and "longitude" in data:
            print(f"🌍 Coordonnées: {data['latitude']}, {data['longitude']}")
    
    def create_forecast_chart(self, data, spot_id):
        """Créer un graphique des prévisions météorologiques"""
        try:
            if "forecast" not in data or "data" not in data["forecast"]:
                print("⚠️  Données insuffisantes pour créer le graphique")
                return None
            
            forecast = data["forecast"]
            weather_data = forecast["data"]
            
            # Extraire les données de vagues
            if "waveHeight" in weather_data and weather_data["waveHeight"]:
                wave_data = weather_data["waveHeight"]
                
                # Préparer les données pour le graphique
                times = []
                heights = []
                
                for point in wave_data:
                    if "time" in point and "waveHeight" in point:
                        time_str = point["time"]
                        height = point["waveHeight"].get("meteo") or point["waveHeight"].get("noaa")
                        
                        if height is not None:
                            times.append(datetime.fromisoformat(time_str.replace('Z', '+00:00')))
                            heights.append(height)
                
                if times and heights:
                    # Créer le graphique
                    plt.figure(figsize=(12, 8))
                    
                    # Graphique principal des vagues
                    plt.subplot(2, 1, 1)
                    plt.plot(times, heights, 'b-', linewidth=2, marker='o')
                    plt.title(f'Prévisions de hauteur des vagues - Spot {spot_id}')
                    plt.ylabel('Hauteur des vagues (m)')
                    plt.grid(True, alpha=0.3)
                    
                    # Formater l'axe des temps
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
                    plt.xticks(rotation=45)
                    
                    # Ajouter des informations sur le spot
                    if "name" in data:
                        plt.suptitle(f'Prévisions météorologiques - {data["name"]}', fontsize=16)
                    
                    # Graphique de la température de l'air si disponible
                    if "airTemperature" in weather_data and weather_data["airTemperature"]:
                        temp_data = weather_data["airTemperature"]
                        temp_times = []
                        temps = []
                        
                        for point in temp_data:
                            if "time" in point and "airTemperature" in point:
                                time_str = point["time"]
                                temp = point["airTemperature"].get("meteo") or point["airTemperature"].get("noaa")
                                
                                if temp is not None:
                                    temp_times.append(datetime.fromisoformat(time_str.replace('Z', '+00:00')))
                                    temps.append(temp)
                        
                        if temp_times and temps:
                            plt.subplot(2, 1, 2)
                            plt.plot(temp_times, temps, 'r-', linewidth=2, marker='s')
                            plt.title('Prévisions de température de l\'air')
                            plt.ylabel('Température (°C)')
                            plt.xlabel('Heure')
                            plt.grid(True, alpha=0.3)
                            
                            # Formater l'axe des temps
                            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
                            plt.xticks(rotation=45)
                    
                    plt.tight_layout()
                    
                    # Sauvegarder le graphique
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    chart_filename = f"{self.output_dir}/forecast_chart_spot_{spot_id}_{timestamp}.png"
                    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    
                    print(f"📊 Graphique sauvegardé: {chart_filename}")
                    return chart_filename
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du graphique: {e}")
            return None
    
    def create_data_screenshot(self, data, spot_id):
        """Créer une capture d'écran des données JSON"""
        try:
            # Créer une image avec les données
            width = 1200
            height = 800
            
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Essayer de charger une police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
                font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Titre
            title = f"Données de prévisions - Spot {spot_id} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            draw.text((20, 20), title, fill='black', font=font_large)
            
            # Ligne de séparation
            draw.line([(20, 60), (width-20, 60)], fill='gray', width=2)
            
            # Afficher les données JSON formatées
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Diviser en lignes et afficher
            lines = json_str.split('\n')
            y_position = 80
            
            for i, line in enumerate(lines[:50]):  # Limiter à 50 lignes
                if y_position > height - 50:
                    break
                
                # Couper les lignes trop longues
                if len(line) > 100:
                    line = line[:97] + "..."
                
                draw.text((20, y_position), line, fill='black', font=font_small)
                y_position += 18
            
            if len(lines) > 50:
                draw.text((20, y_position), "... (données tronquées)", fill='gray', font=font_small)
            
            # Sauvegarder l'image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_filename = f"{self.output_dir}/forecast_data_spot_{spot_id}_{timestamp}.png"
            img.save(screenshot_filename)
            
            print(f"📸 Capture d'écran des données sauvegardée: {screenshot_filename}")
            return screenshot_filename
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la capture d'écran: {e}")
            return None
    
    def run_complete_test(self):
        """Exécuter un test complet de l'API forecast"""
        print("🌊 Test complet de l'API Forecast InnovSurf")
        print("=" * 60)
        
        # Authentification
        if not self.authenticate():
            print("⚠️  Authentification échouée, tests sans authentification")
        
        # Récupérer la liste des spots
        spots = self.get_surf_spots()
        
        if not spots:
            print("❌ Aucun spot disponible pour les tests")
            return
        
        # Tester l'API forecast pour chaque spot
        test_results = []
        
        for spot in spots[:3]:  # Limiter à 3 spots pour éviter la surcharge
            spot_id = spot.get('id')
            spot_name = spot.get('name', f'Spot {spot_id}')
            
            print(f"\n🏄 Test du spot: {spot_name} (ID: {spot_id})")
            
            # Test de l'endpoint forecast
            result = self.test_forecast_endpoint(spot_id)
            result['spot_id'] = spot_id
            result['spot_name'] = spot_name
            
            test_results.append(result)
            
            # Créer des visualisations si les données sont disponibles
            if result['success'] and 'data' in result:
                # Créer un graphique
                self.create_forecast_chart(result['data'], spot_id)
                
                # Créer une capture d'écran des données
                self.create_data_screenshot(result['data'], spot_id)
            
            # Pause entre les tests
            time.sleep(1)
        
        # Générer un rapport
        self.generate_test_report(test_results)
        
        return test_results
    
    def generate_test_report(self, test_results):
        """Générer un rapport de test"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"{self.output_dir}/forecast_test_report_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Rapport de Test de l'API Forecast\n\n")
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
                f.write(f"### {status_icon} {result['spot_name']} (ID: {result['spot_id']})\n\n")
                f.write(f"- **Statut:** {'Succès' if result['success'] else 'Échec'}\n")
                f.write(f"- **Temps de réponse:** {result['response_time']:.2f}s\n")
                f.write(f"- **Code de statut:** {result['status_code']}\n\n")
                
                if not result["success"] and "error" in result:
                    f.write(f"**Erreur:** {result['error']}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Rapport généré dans {report_file}")

def main():
    """Fonction principale"""
    print("🌊 Testeur de l'API Forecast InnovSurf")
    print("=" * 50)
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        print("✅ Serveur accessible")
    except:
        print("❌ Serveur non accessible")
        print("Assurez-vous que votre serveur Django est démarré")
        return
    
    # Créer et exécuter le testeur
    tester = ForecastAPITester()
    results = tester.run_complete_test()
    
    print("\n🎉 Tests terminés !")
    print(f"Consultez le dossier '{tester.output_dir}' pour les résultats")

if __name__ == "__main__":
    main()
