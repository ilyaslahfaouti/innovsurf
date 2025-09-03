#!/usr/bin/env python3
"""
Test rapide de la nouvelle clé API StormGlass
"""

import sys
import os

# Ajouter le répertoire AppWeb au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'AppWeb'))

def test_new_api():
    """Test de la nouvelle clé API"""
    
    try:
        # Importer le service
        from services import fetch_forecast
        
        print("🧪 Test de la nouvelle clé API StormGlass")
        print("=" * 50)
        
        # Coordonnées de Taghazout
        lat, lng = 30.542, -9.71
        
        print(f"📍 Test pour Taghazout (lat: {lat}, lng: {lng})")
        print("📡 Appel de l'API...")
        
        # Appeler l'API
        result = fetch_forecast(lat, lng)
        
        print("\n📊 Résultat:")
        print(f"   - Type: {type(result)}")
        print(f"   - Clés: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
        
        if isinstance(result, dict):
            if 'errors' in result:
                print(f"   ❌ Erreur: {result['errors']}")
                if 'meta' in result:
                    print(f"   📋 Métadonnées: {result['meta']}")
            elif 'data' in result:
                print(f"   ✅ Succès! Données reçues")
                print(f"   📊 Paramètres: {list(result['data'].keys())}")
                
                # Afficher un exemple de données
                for param, data in result['data'].items():
                    if isinstance(data, list) and len(data) > 0:
                        print(f"   📈 {param}: {len(data)} points de données")
                        if len(data) > 0:
                            print(f"      Exemple: {data[0]}")
        
        print("\n" + "=" * 50)
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que le fichier services.py existe")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

if __name__ == "__main__":
    test_new_api()
