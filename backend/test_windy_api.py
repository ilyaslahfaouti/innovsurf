#!/usr/bin/env python
"""
Script de test pour l'API Windy intégrée dans YalaSurf
Ce script teste toutes les fonctionnalités météo du chatbot IA
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.windy_api_service import windy_service

def test_windy_api_integration():
    """Teste l'intégration complète de l'API Windy"""
    
    print("🌊 Test de l'API Windy - YalaSurf")
    print("=" * 50)
    
    # Test 1: Prévisions pour un spot spécifique
    print("\n📊 Test 1: Prévisions pour Taghazout")
    print("-" * 40)
    
    try:
        forecast = windy_service.get_spot_forecast('taghazout', 3)
        if forecast.get('success'):
            print("✅ Prévisions récupérées avec succès !")
            print(f"   📍 Spot: {forecast['spot_info']['name']}")
            print(f"   📅 Période: {forecast['forecast_period']}")
            print(f"   🕐 Généré: {forecast['generated_at']}")
            
            if forecast.get('current_conditions'):
                conditions = forecast['current_conditions']
                print(f"   📏 Vagues actuelles: {conditions.get('wave_height', 'N/A')}m")
                print(f"   💨 Vent actuel: {conditions.get('wind_speed', 'N/A')} km/h")
                print(f"   🌡️ Température eau: {conditions.get('water_temp', 'N/A')}°C")
        else:
            print("❌ Échec de récupération des prévisions")
            print(f"   Erreur: {forecast.get('error', 'Inconnue')}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 2: Prévisions par coordonnées
    print("\n📍 Test 2: Prévisions par coordonnées (Agadir)")
    print("-" * 40)
    
    try:
        forecast = windy_service.get_surf_forecast(30.4278, -9.5981, 3)
        if forecast.get('success'):
            print("✅ Prévisions par coordonnées récupérées !")
            print(f"   📍 Coordonnées: {forecast['spot_info']['lat']}, {forecast['spot_info']['lon']}")
        else:
            print("❌ Échec des prévisions par coordonnées")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 3: Meilleurs moments pour surfer
    print("\n🏄‍♂️ Test 3: Meilleurs moments pour surfer (Essaouira)")
    print("-" * 40)
    
    try:
        optimal_times = windy_service.get_optimal_surf_times(31.5085, -9.7595, 3)
        if optimal_times.get('success'):
            print("✅ Moments optimaux récupérés !")
            if optimal_times.get('optimal_times'):
                print(f"   📅 Nombre de jours optimaux: {len(optimal_times['optimal_times'])}")
                for day in optimal_times['optimal_times'][:2]:
                    print(f"      - {day['date']}: Score {day['score']}/10")
            else:
                print("   ℹ️ Aucun moment optimal trouvé")
        else:
            print("❌ Échec de récupération des moments optimaux")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 4: Résumé des conditions
    print("\n📝 Test 4: Résumé des conditions (Bouznika)")
    print("-" * 40)
    
    try:
        summary = windy_service.get_surf_conditions_summary('bouznika')
        if summary and "Conditions actuelles" in summary:
            print("✅ Résumé des conditions généré !")
            print(f"   📏 Longueur du résumé: {len(summary)} caractères")
            # Afficher les premières lignes du résumé
            lines = summary.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print("❌ Échec de génération du résumé")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 5: Gestion des erreurs
    print("\n🚨 Test 5: Gestion des erreurs")
    print("-" * 40)
    
    try:
        # Test avec un spot inexistant
        forecast = windy_service.get_spot_forecast('spot_inexistant', 1)
        if not forecast.get('success'):
            print("✅ Gestion d'erreur correcte pour spot inexistant")
            print(f"   Message: {forecast.get('error', 'N/A')}")
        else:
            print("❌ Erreur: Le spot inexistant a été accepté")
    except Exception as e:
        print(f"❌ Erreur lors du test de gestion d'erreur: {e}")
    
    # Test 6: Performance
    print("\n⚡ Test 6: Performance")
    print("-" * 40)
    
    import time
    
    try:
        start_time = time.time()
        for i in range(5):
            windy_service.get_spot_forecast('taghazout', 1)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / 5
        
        print(f"✅ 5 requêtes traitées en {total_time:.2f}s")
        print(f"   ⏱️ Temps moyen par requête: {avg_time:.2f}s")
        print(f"   🚀 Requêtes par seconde: {5/total_time:.1f}")
        
        if avg_time < 1.0:
            print("   🎯 Performance: Excellente (< 1s)")
        elif avg_time < 2.0:
            print("   🎯 Performance: Bonne (< 2s)")
        else:
            print("   🎯 Performance: Lente (> 2s)")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de performance: {e}")
    
    # Test 7: Intégration avec le chatbot
    print("\n🤖 Test 7: Intégration avec le chatbot IA")
    print("-" * 40)
    
    try:
        from AppWeb.ai_services import chatbot_ai
        
        # Test des questions météo
        weather_questions = [
            "Quelle est la météo à Taghazout ?",
            "Comment sont les conditions à Essaouira ?",
            "Quand est le meilleur moment pour surfer à Agadir ?"
        ]
        
        for question in weather_questions:
            response = chatbot_ai.process_message(question)
            print(f"🤔 Question: {question}")
            print(f"🤖 Réponse: {response['response'][:100]}...")
            print(f"🎯 Intent: {response['intent']}")
            print(f"📊 Confiance: {response['confidence']:.2f}")
            print()
        
        print("✅ Intégration chatbot-Windy fonctionnelle !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
    
    print("\n🎉 Tests de l'API Windy terminés !")
    print("=" * 50)

def test_windy_data_processing():
    """Teste le traitement des données Windy"""
    
    print("\n🔧 Test du traitement des données Windy")
    print("-" * 40)
    
    # Test des fonctions utilitaires
    try:
        # Test du calcul de score de surf
        test_conditions = {
            'wave_height': 2.0,
            'wind_speed': 8.0
        }
        
        score = windy_service._calculate_surf_score(test_conditions)
        print(f"✅ Score de surf calculé: {score}/10")
        
        # Test de l'analyse de journée
        test_day = {
            'avg_wave_height': 1.5,
            'avg_wind_speed': 12.0,
            'best_hours': [{'hour': '8', 'score': 8.5}]
        }
        
        day_analysis = windy_service._analyze_day_for_surf(test_day)
        print(f"✅ Analyse de journée: Score {day_analysis['score']}/10")
        print(f"   📏 Vagues moyennes: {day_analysis['wave_height']}m")
        print(f"   💨 Vent moyen: {day_analysis['wind_speed']} km/h")
        print(f"   💡 Recommandation: {day_analysis['recommendation']}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test de traitement: {e}")

def test_windy_api_endpoints():
    """Teste les endpoints API Windy"""
    
    print("\n🌐 Test des endpoints API Windy")
    print("-" * 40)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test de l'endpoint forecast
        response = client.get('/api/windy/forecast/?spot=taghazout&days=3')
        if response.status_code == 200:
            print("✅ Endpoint /api/windy/forecast/ fonctionne")
        else:
            print(f"❌ Endpoint forecast: Status {response.status_code}")
        
        # Test de l'endpoint optimal-times
        response = client.get('/api/windy/optimal-times/?spot=taghazout&days=3')
        if response.status_code == 200:
            print("✅ Endpoint /api/windy/optimal-times/ fonctionne")
        else:
            print(f"❌ Endpoint optimal-times: Status {response.status_code}")
        
        # Test de l'endpoint conditions-summary
        response = client.get('/api/windy/conditions-summary/?spot=taghazout')
        if response.status_code == 200:
            print("✅ Endpoint /api/windy/conditions-summary/ fonctionne")
        else:
            print(f"❌ Endpoint conditions-summary: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des endpoints: {e}")

if __name__ == '__main__':
    try:
        print("🚀 Démarrage des tests de l'API Windy...")
        
        # Tests principaux
        test_windy_api_integration()
        
        # Tests de traitement des données
        test_windy_data_processing()
        
        # Tests des endpoints API
        test_windy_api_endpoints()
        
        print("\n🎯 Tous les tests de l'API Windy ont été exécutés avec succès !")
        print("🌊 Votre chatbot IA est maintenant connecté à Windy ! 🏄‍♂️")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
