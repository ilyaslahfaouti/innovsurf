#!/usr/bin/env python3
"""
Script de diagnostic pour identifier le problème de features
"""

import os
import sys
import django
from datetime import datetime, timedelta
import pandas as pd

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.booking_prediction import BookingPredictionSystem

def debug_features():
    """
    Diagnostique le problème de features
    """
    print("🔍 DIAGNOSTIC DES FEATURES")
    print("=" * 40)
    
    try:
        system = BookingPredictionSystem()
        
        # 1. Générer des données
        print("\n📊 1. Génération de données...")
        historical_data = system.generate_historical_booking_data(100)
        print(f"✅ {len(historical_data)} enregistrements générés")
        
        # 2. Examiner la structure des données
        print("\n🔍 2. Structure des données...")
        if historical_data:
            sample = historical_data[0]
            print(f"Colonnes disponibles: {list(sample.keys())}")
            print(f"Nombre de colonnes: {len(sample.keys())}")
            
            # Vérifier les features standard
            standard_features = system._get_standard_features()
            print(f"\nFeatures standard attendues: {standard_features}")
            print(f"Nombre de features standard: {len(standard_features)}")
            
            # Vérifier la correspondance
            missing_features = [col for col in standard_features if col not in sample.keys()]
            extra_features = [col for col in sample.keys() if col not in standard_features]
            
            print(f"\nFeatures manquantes: {missing_features}")
            print(f"Features en trop: {extra_features}")
        
        # 3. Tester l'encodage
        print("\n🔄 3. Test d'encodage...")
        df = pd.DataFrame(historical_data)
        print(f"DataFrame shape: {df.shape}")
        
        # Sélectionner les features standard
        standard_features = system._get_standard_features()
        available_features = [col for col in standard_features if col in df.columns]
        print(f"Features disponibles pour l'encodage: {available_features}")
        
        if available_features:
            X = df[available_features]
            print(f"X shape: {X.shape}")
            
            # Encoder
            X_encoded = system._encode_features(X)
            print(f"X_encoded shape: {X_encoded.shape}")
            print(f"X_encoded columns: {list(X_encoded.columns)}")
            
            # Standardiser
            X_scaled = system.scaler.fit_transform(X_encoded)
            print(f"X_scaled shape: {X_scaled.shape}")
        
        # 4. Tester la prédiction
        print("\n🔮 4. Test de prédiction...")
        future_date = datetime.now() + timedelta(days=7)
        weather_forecast = {'wave_height': 2.5, 'wind_speed': 12, 'water_temp': 24}
        
        # Préparer les features
        features = system._prepare_prediction_features(future_date, weather_forecast)
        print(f"Features préparées: {list(features.keys())}")
        print(f"Nombre de features: {len(features)}")
        
        # Vérifier l'ordre
        standard_features = system._get_standard_features()
        features_ordered = {col: features.get(col, 0) for col in standard_features}
        print(f"Features ordonnées: {list(features_ordered.keys())}")
        
        # Créer DataFrame
        features_df = pd.DataFrame([features_ordered])
        print(f"Features DataFrame shape: {features_df.shape}")
        print(f"Features DataFrame columns: {list(features_df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_features()
