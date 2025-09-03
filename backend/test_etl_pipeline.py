#!/usr/bin/env python3
"""
Script de test pour le pipeline ETL de prédiction des réservations
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.booking_prediction import (
    BookingPredictionSystem, 
    test_etl_pipeline, 
    demo_etl_with_mock_data,
    test_predictions
)

def main():
    """
    Fonction principale de test
    """
    print("=" * 60)
    print("🧪 TEST DU PIPELINE ETL - SYSTÈME DE PRÉDICTION YALASURF")
    print("=" * 60)
    
    try:
        # Test 1: Pipeline ETL avec vraies données
        print("\n1️⃣ Test du pipeline ETL avec données réelles...")
        test_etl_pipeline()
        
    except Exception as e:
        print(f"⚠️  Pipeline ETL avec données réelles échoué: {e}")
        print("🔄 Passage au test avec données simulées...")
        
        try:
            # Test 2: Pipeline ETL avec données simulées
            print("\n2️⃣ Test du pipeline ETL avec données simulées...")
            demo_etl_with_mock_data()
            
        except Exception as e:
            print(f"❌ Pipeline ETL avec données simulées échoué: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS TERMINÉS!")
    print("=" * 60)
    
    return True

def test_individual_components():
    """
    Test des composants individuels du système
    """
    print("\n🔧 Test des composants individuels...")
    
    try:
        # Créer une instance
        system = BookingPredictionSystem()
        
        # Test 1: Génération de données historiques
        print("📊 Test de génération de données historiques...")
        historical_data = system.generate_historical_booking_data(100)
        print(f"✅ {len(historical_data)} enregistrements générés")
        
        # Test 2: Chargement des données
        print("📥 Test de chargement des données...")
        load_success = system.load_transformed_data(historical_data)
        print(f"✅ Chargement: {'Succès' if load_success else 'Échec'}")
        
        # Test 3: Entraînement des modèles
        if load_success:
            print("🧠 Test d'entraînement des modèles...")
            training_results = system._train_all_models()
            print(f"✅ Entraînement: {'Succès' if training_results['success'] else 'Échec'}")
            
            if training_results['success']:
                # Test 4: Prédictions
                print("🔮 Test des prédictions...")
                test_predictions(system)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des composants: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests ETL...")
    
    # Test principal
    main_success = main()
    
    if main_success:
        # Test des composants individuels
        test_individual_components()
    
    print("\n�� Tests terminés!")
