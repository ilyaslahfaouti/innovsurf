import json
import os
import arrow
import requests
import sys
import os.path

# Ajouter le répertoire parent au path pour importer config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import STORMGLASS_API_KEY, API_TIMEOUT
    print(f"✅ Configuration chargée - Clé API: {STORMGLASS_API_KEY[:20]}...")
except ImportError:
    # Fallback si config.py n'existe pas
    STORMGLASS_API_KEY = 'f2a0d83a-82c6-11f0-a59f-0242ac130006-f2a0d8da-82c6-11f0-a59f-0242ac130006'
    API_TIMEOUT = 10
    print(f"⚠️ Configuration par défaut - Clé API: {STORMGLASS_API_KEY[:20]}...")

def fetch_forecast(latitude, longitude):
    """
    Récupère les prévisions météorologiques depuis StormGlass API
    """
    print(f"🔍 Tentative de récupération des prévisions pour lat: {latitude}, lng: {longitude}")
    print(f"🔑 Utilisation de la clé API: {STORMGLASS_API_KEY[:20]}...")
    
    # Get first hour of today
    start = arrow.now().floor('day')
    
    # Get last hour of today
    end = arrow.now().ceil('day')
    
    try:
        print("📡 Envoi de la requête à StormGlass API...")
        
        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': latitude,
                'lng': longitude,
                'params': ','.join(['waveHeight', 'airTemperature', 'swellPeriod', 'windSpeed', 'waterTemperature']),
                'start': start.to('UTC').timestamp(),
                'end': end.to('UTC').timestamp()
            },
            headers={
                'Authorization': STORMGLASS_API_KEY
            },
            timeout=API_TIMEOUT
        )
        
        print(f"📊 Réponse reçue - Status: {response.status_code}")
        
        # Vérifier le statut de la réponse
        if response.status_code == 200:
            json_data = response.json()
            print("✅ Données météo récupérées avec succès")
            print(f"   - Structure des données: {list(json_data.keys())}")
            if 'data' in json_data:
                print(f"   - Paramètres disponibles: {list(json_data['data'].keys())}")
            return json_data
        elif response.status_code == 429:
            # Quota dépassé
            print("⚠️ Quota API dépassé")
            return {
                "errors": {"key": "API quota exceeded"},
                "meta": {"dailyQuota": 50, "requestCount": 51}
            }
        elif response.status_code == 401:
            # Clé API invalide
            print("❌ Clé API invalide")
            return {
                "errors": {"key": "Invalid API key"},
                "meta": {"dailyQuota": 0, "requestCount": 0}
            }
        else:
            # Autre erreur
            print(f"❌ Erreur HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   - Détails de l'erreur: {error_data}")
            except:
                print(f"   - Réponse brute: {response.text[:200]}")
            return {
                "errors": {"key": f"HTTP {response.status_code}"},
                "meta": {"dailyQuota": 0, "requestCount": 0}
            }
            
    except requests.exceptions.RequestException as e:
        # Erreur de connexion
        print(f"❌ Erreur de connexion: {str(e)}")
        return {
            "errors": {"key": f"Connection error: {str(e)}"},
            "meta": {"dailyQuota": 0, "requestCount": 0}
        }
    except Exception as e:
        # Erreur générale
        print(f"❌ Erreur générale: {str(e)}")
        return {
            "errors": {"key": f"General error: {str(e)}"},
            "meta": {"dailyQuota": 0, "requestCount": 0}
        }

