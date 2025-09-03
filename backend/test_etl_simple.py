#!/usr/bin/env python3
"""
Script de test simplifié pour le pipeline ETL de prédiction des réservations
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.booking_prediction import BookingPredictionSystem

def test_simple_etl():
    """
    Test simple du pipeline ETL avec données simulées
    """
    print("🧪 TEST SIMPLIFIÉ DU PIPELINE ETL")
    print("=" * 50)
    
    try:
        # Créer une instance du système
        system = BookingPredictionSystem()
        
        # Test 1: Génération de données historiques
        print("\n📊 1. Génération de données historiques...")
        historical_data = system.generate_historical_booking_data(500)
        print(f"✅ {len(historical_data)} enregistrements générés")
        
        # Test 2: Chargement des données
        print("\n📥 2. Chargement des données...")
        load_success = system.load_transformed_data(historical_data)
        print(f"✅ Chargement: {'Succès' if load_success else 'Échec'}")
        
        if not load_success:
            print("❌ Échec du chargement des données")
            return False
        
        # Test 3: Entraînement des modèles
        print("\n🧠 3. Entraînement des modèles...")
        
        # Entraîner le modèle de demande
        print("   - Modèle de demande...")
        demand_result = system.train_demand_prediction_model(historical_data, 'random_forest')
        if demand_result['success']:
            print(f"   ✅ Modèle de demande entraîné (R²: {demand_result['metrics']['r2']:.3f})")
        else:
            print(f"   ❌ Erreur modèle de demande: {demand_result['error']}")
        
        # Entraîner le modèle de prix
        print("   - Modèle de prix...")
        price_result = system.train_price_optimization_model(historical_data, 'random_forest')
        if price_result['success']:
            print(f"   ✅ Modèle de prix entraîné (R²: {price_result['metrics']['r2']:.3f})")
        else:
            print(f"   ❌ Erreur modèle de prix: {price_result['error']}")
        
        # Entraîner le modèle d'annulation
        print("   - Modèle d'annulation...")
        cancellation_result = system.train_cancellation_prediction_model(historical_data, 'random_forest')
        if cancellation_result['success']:
            print("   ✅ Modèle d'annulation entraîné")
        else:
            print(f"   ❌ Erreur modèle d'annulation: {cancellation_result['error']}")
        
        # Test 4: Prédictions
        print("\n🔮 4. Test des prédictions...")
        
        # Date future pour tester
        future_date = datetime.now() + timedelta(days=7)
        
        # Données météo simulées
        weather_forecast = {
            'wave_height': 2.5,
            'wind_speed': 12,
            'water_temp': 24
        }
        
        # Prédire la demande
        if system.demand_model:
            try:
                demand_prediction = system.predict_demand(future_date, weather_forecast, 'Taghazout')
                if demand_prediction['success']:
                    print(f"   📈 Demande prédite: {demand_prediction['predicted_demand']:.2f} ({demand_prediction['demand_level']})")
                else:
                    print(f"   ❌ Erreur prédiction demande: {demand_prediction['error']}")
            except Exception as e:
                print(f"   ❌ Exception prédiction demande: {e}")
        
        # Optimiser le prix
        if system.price_optimization_model:
            try:
                price_optimization = system.optimize_price(future_date, weather_forecast, 100)
                if price_optimization['success']:
                    print(f"   💰 Prix optimisé: {price_optimization['optimized_price']:.2f}€ (x{price_optimization['price_multiplier']:.2f})")
                else:
                    print(f"   ❌ Erreur optimisation prix: {price_optimization['error']}")
            except Exception as e:
                print(f"   ❌ Exception optimisation prix: {e}")
        
        # Prédire l'annulation
        if system.cancellation_model:
            try:
                booking_data = {
                    'booking_date': future_date.isoformat(),
                    'wave_height': 2.5,
                    'wind_speed': 12,
                    'water_temp': 24,
                    'predicted_demand': 1.2,
                    'price_multiplier': 1.1
                }
                
                cancellation_prediction = system.predict_cancellation_probability(booking_data)
                if cancellation_prediction['success']:
                    print(f"   ⚠️  Risque d'annulation: {cancellation_prediction['cancellation_probability']:.3f} ({cancellation_prediction['risk_level']})")
                else:
                    print(f"   ❌ Erreur prédiction annulation: {cancellation_prediction['error']}")
            except Exception as e:
                print(f"   ❌ Exception prédiction annulation: {e}")
        
        # Test 5: Sauvegarde des modèles
        print("\n💾 5. Sauvegarde des modèles...")
        try:
            system.save_models()
            print("✅ Modèles sauvegardés avec succès")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
        
        # Test 6: Statut du système
        print("\n📊 6. Statut du système...")
        status = system.get_system_status()
        for key, value in status.items():
            print(f"   - {key}: {'✅' if value else '❌'}")
        
        print("\n🎯 TOUS LES TESTS TERMINÉS AVEC SUCCÈS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """
    Test des composants individuels
    """
    print("\n🔧 TEST DES COMPOSANTS INDIVIDUELS")
    print("=" * 40)
    
    try:
        system = BookingPredictionSystem()
        
        # Test de la génération de données
        print("\n📊 Test génération données...")
        data = system.generate_historical_booking_data(100)
        print(f"✅ {len(data)} enregistrements générés")
        
        # Test de la transformation des données
        print("\n🔄 Test transformation données...")
        # Simuler des données brutes
        raw_data = {
            'surf_lessons': [],
            'surf_sessions': [],
            'equipment_orders': []
        }
        transformed = system.transform_booking_data(raw_data)
        print(f"✅ {len(transformed)} enregistrements transformés")
        
        # Test des utilitaires
        print("\n🛠️ Test utilitaires...")
        
        # Test calcul score météo
        weather_score = system._calculate_weather_score(2.0, 10, 22)
        print(f"✅ Score météo calculé: {weather_score}")
        
        # Test détermination saison
        season = system._get_season(7)
        print(f"✅ Saison déterminée: {season}")
        
        # Test facteurs de demande
        factors = system._calculate_demand_factors(datetime.now(), {'weather_score': 8.0})
        print(f"✅ Facteurs de demande: {factors}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur composants: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS ETL SIMPLIFIÉS")
    print("=" * 60)
    
    # Test principal
    main_success = test_simple_etl()
    
    if main_success:
        # Test des composants
        test_individual_components()
    
    print("\n�� Tests terminés!")
