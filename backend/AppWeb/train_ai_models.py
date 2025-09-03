# train_ai_models.py
"""
Script d'entraînement et de test des modèles IA pour YalaSurf
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.surf_prediction_model import surf_prediction_model
from AppWeb.recommendation_system import recommendation_system
from AppWeb.booking_prediction import booking_prediction_system
from AppWeb.analytics_dashboard import analytics_dashboard

def train_all_models():
    """
    Entraîne tous les modèles IA
    """
    print("🚀 Démarrage de l'entraînement des modèles IA...")
    
    # 1. Modèle de prédiction des conditions de surf
    print("\n📊 Entraînement du modèle de prédiction des conditions de surf...")
    try:
        # Générer des données d'exemple
        sample_data = surf_prediction_model.generate_sample_data(1000)
        
        # Entraîner le modèle
        result = surf_prediction_model.train_model(sample_data, 'random_forest')
        
        if result['success']:
            print(f"✅ Modèle entraîné avec succès!")
            print(f"   R² Score: {result['metrics']['r2']:.3f}")
            print(f"   RMSE: {result['metrics']['rmse']:.3f}")
        else:
            print(f"❌ Erreur: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'entraînement: {e}")
    
    # 2. Système de recommandation
    print("\n🎯 Initialisation du système de recommandation...")
    try:
        recommendation_system.initialize_system()
        if recommendation_system.is_initialized:
            print("✅ Système de recommandation initialisé!")
        else:
            print("❌ Échec de l'initialisation")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Système de prédiction des réservations
    print("\n📈 Entraînement du système de prédiction des réservations...")
    try:
        # Générer des données historiques
        historical_data = booking_prediction_system.generate_historical_booking_data(1000)
        
        # Entraîner le modèle de demande
        demand_result = booking_prediction_system.train_demand_prediction_model(historical_data, 'random_forest')
        if demand_result['success']:
            print(f"✅ Modèle de demande entraîné (R²: {demand_result['metrics']['r2']:.3f})")
        
        # Entraîner le modèle d'optimisation des prix
        price_result = booking_prediction_system.train_price_optimization_model(historical_data, 'random_forest')
        if price_result['success']:
            print(f"✅ Modèle de prix entraîné (R²: {price_result['metrics']['r2']:.3f})")
        
        # Entraîner le modèle de prédiction d'annulation
        cancellation_result = booking_prediction_system.train_cancellation_prediction_model(historical_data, 'random_forest')
        if cancellation_result['success']:
            print(f"✅ Modèle d'annulation entraîné")
        
        # Sauvegarder tous les modèles
        booking_prediction_system.save_models()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Dashboard analytics
    print("\n📊 Initialisation du dashboard analytics...")
    try:
        analytics_dashboard.initialize_dashboard()
        if analytics_dashboard.is_initialized:
            print("✅ Dashboard analytics initialisé!")
        else:
            print("❌ Échec de l'initialisation")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n🎉 Entraînement terminé!")

def test_all_models():
    """
    Teste tous les modèles entraînés
    """
    print("\n🧪 Test des modèles IA...")
    
    # 1. Test du modèle de prédiction des conditions
    print("\n📊 Test du modèle de prédiction des conditions...")
    try:
        test_weather = {
            'wave_height': 2.0,
            'wind_speed': 12,
            'wind_direction': 180,
            'water_temp': 22,
            'tide': 0.5,
            'pressure': 1013,
            'precipitation': 0,
            'spot_name': 'Taghazout',
            'surfer_level': 'intermediate'
        }
        
        prediction = surf_prediction_model.predict_surf_conditions(test_weather)
        if prediction['success']:
            print(f"✅ Prédiction: Score {prediction['predicted_score']}/10")
            print(f"   Interprétation: {prediction['interpretation']}")
            print(f"   Confiance: {prediction['confidence']}")
        else:
            print(f"❌ Erreur: {prediction['error']}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 2. Test du système de recommandation
    print("\n🎯 Test du système de recommandation...")
    try:
        user_preferences = {
            'surf_level': 'intermediate',
            'preferred_location': 'Taghazout',
            'preferred_wave_type': 'right',
            'crowd_preference': 'medium'
        }
        
        spot_recommendations = recommendation_system.recommend_spots(user_preferences, 3)
        if spot_recommendations:
            print(f"✅ {len(spot_recommendations)} spots recommandés")
            for spot in spot_recommendations[:2]:
                print(f"   - {spot['name']} (Score: {spot['recommendation_score']})")
        else:
            print("❌ Aucune recommandation générée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Test du système de prédiction des réservations
    print("\n📈 Test du système de prédiction des réservations...")
    try:
        future_date = datetime.now() + timedelta(days=7)
        weather_forecast = {
            'wave_height': 1.8,
            'wind_speed': 15,
            'water_temp': 23
        }
        
        # Prédiction de demande
        demand_prediction = booking_prediction_system.predict_demand(future_date, weather_forecast)
        if demand_prediction['success']:
            print(f"✅ Demande prédite: {demand_prediction['demand_level']}")
        
        # Optimisation des prix
        price_optimization = booking_prediction_system.optimize_price(future_date, weather_forecast, 100)
        if price_optimization['success']:
            print(f"✅ Prix optimisé: {price_optimization['optimized_price']}€ (Base: {price_optimization['base_price']}€)")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n✅ Tests terminés!")

def generate_sample_analytics():
    """
    Génère des analytics d'exemple
    """
    print("\n📊 Génération d'analytics d'exemple...")
    
    try:
        # Analytics météo
        weather_analytics = analytics_dashboard.generate_weather_analytics('Taghazout', 7)
        if weather_analytics['success']:
            print("✅ Analytics météo générés")
            print(f"   Résumé: {len(weather_analytics['charts'])} graphiques créés")
            
            # Afficher les statistiques
            summary = weather_analytics['summary_stats']
            if 'vagues' in summary:
                print(f"   Vagues moyennes: {summary['vagues']['moyenne']}m")
                print(f"   Vent moyen: {summary['vent']['moyenne']} km/h")
        else:
            print(f"❌ Erreur analytics: {weather_analytics['error']}")
        
        # Métriques IA
        ai_metrics = analytics_dashboard.generate_ai_performance_metrics()
        if ai_metrics['success']:
            print("✅ Métriques IA générées")
            performance = ai_metrics['metrics']['overall_performance']
            print(f"   Performance globale: {performance['score']}% ({performance['level']})")
        else:
            print(f"❌ Erreur métriques: {ai_metrics['error']}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n✅ Analytics générés!")

def main():
    """
    Fonction principale
    """
    print("🤖 YalaSurf - Entraînement des Modèles IA")
    print("=" * 50)
    
    # Vérifier que Django est configuré
    try:
        from django.conf import settings
        print(f"✅ Django configuré: {settings.DEBUG}")
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return
    
    # Menu principal
    while True:
        print("\nOptions disponibles:")
        print("1. Entraîner tous les modèles")
        print("2. Tester les modèles")
        print("3. Générer des analytics")
        print("4. Tout faire")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            train_all_models()
        elif choice == '2':
            test_all_models()
        elif choice == '3':
            generate_sample_analytics()
        elif choice == '4':
            train_all_models()
            test_all_models()
            generate_sample_analytics()
        elif choice == '5':
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
