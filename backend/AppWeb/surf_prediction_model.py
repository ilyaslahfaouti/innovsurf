# surf_prediction_model.py
"""
Modèle prédictif IA pour les conditions de surf
Utilise le machine learning pour prédire la qualité des vagues
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import joblib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
import json

logger = logging.getLogger(__name__)

class SurfPredictionModel:
    """
    Modèle IA pour prédire la qualité des conditions de surf
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or 'surf_prediction_model.pkl'
        self.scaler_path = 'surf_scaler.pkl'
        self.label_encoders = {}
        
        # Modèles ML
        self.models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100, 
                max_depth=10, 
                random_state=42
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100, 
                max_depth=5, 
                random_state=42
            ),
            'linear_regression': LinearRegression(),
            'svr': SVR(kernel='rbf', C=100, gamma='scale')
        }
        
        self.current_model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
        
        # Charger le modèle si il existe
        self.load_model()
    
    def prepare_training_data(self, historical_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prépare les données d'entraînement à partir de l'historique météo
        """
        if not historical_data:
            raise ValueError("Aucune donnée historique fournie")
        
        # Convertir en DataFrame
        df = pd.DataFrame(historical_data)
        
        # Nettoyer les données
        df = df.dropna()
        
        # Créer les features
        features = self._create_features(df)
        
        # Créer la target (score de surf)
        targets = self._create_surf_score(df)
        
        # Encoder les variables catégorielles
        features_encoded = self._encode_categorical_features(features)
        
        # Sauvegarder les colonnes de features
        self.feature_columns = features_encoded.columns.tolist()
        
        return features_encoded.values, targets.values
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crée les features pour le modèle ML
        """
        features = pd.DataFrame()
        
        # Features météo de base
        features['wave_height'] = df['wave_height']
        features['wind_speed'] = df['wind_speed']
        features['wind_direction'] = df['wind_direction']
        features['water_temp'] = df['water_temp']
        features['tide'] = df['tide']
        features['pressure'] = df.get('pressure', 1013.25)  # Valeur par défaut
        features['precipitation'] = df.get('precipitation', 0)
        
        # Features dérivées
        features['wave_wind_ratio'] = features['wave_height'] / (features['wind_speed'] + 1)
        features['wind_direction_sin'] = np.sin(np.radians(features['wind_direction']))
        features['wind_direction_cos'] = np.cos(np.radians(features['wind_direction']))
        
        # Features temporelles
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            features['hour'] = df['timestamp'].dt.hour
            features['day_of_week'] = df['timestamp'].dt.dayofweek
            features['month'] = df['timestamp'].dt.month
            features['season'] = df['timestamp'].dt.month % 12 // 3
        
        # Features de spot (si disponible)
        if 'spot_name' in df.columns:
            features['spot_name'] = df['spot_name']
        
        # Features de niveau de surfeur (si disponible)
        if 'surfer_level' in df.columns:
            features['surfer_level'] = df['surfer_level']
        
        return features
    
    def _create_surf_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Crée le score de surf comme target pour l'entraînement
        """
        scores = []
        
        for _, row in df.iterrows():
            score = self._calculate_surf_score_from_features(row)
            scores.append(score)
        
        return pd.Series(scores)
    
    def _calculate_surf_score_from_features(self, row: pd.Series) -> float:
        """
        Calcule un score de surf basé sur les features
        """
        wave_height = row.get('wave_height', 0)
        wind_speed = row.get('wind_speed', 0)
        water_temp = row.get('water_temp', 20)
        
        # Score vagues (optimal 1-3m)
        if 1 <= wave_height <= 3:
            wave_score = 10
        elif 0.5 <= wave_height < 1:
            wave_score = 7
        elif 3 < wave_height <= 4:
            wave_score = 6
        else:
            wave_score = 3
        
        # Score vent (optimal < 15 km/h)
        if wind_speed < 10:
            wind_score = 10
        elif wind_speed < 15:
            wind_score = 8
        elif wind_speed < 20:
            wind_score = 5
        else:
            wind_score = 2
        
        # Score température (optimal 18-25°C)
        if 18 <= water_temp <= 25:
            temp_score = 10
        elif 15 <= water_temp < 18 or 25 < water_temp <= 28:
            temp_score = 7
        else:
            temp_score = 4
        
        # Score final pondéré
        final_score = (wave_score * 0.5 + wind_score * 0.3 + temp_score * 0.2)
        
        return round(final_score, 1)
    
    def _encode_categorical_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Encode les variables catégorielles
        """
        features_encoded = features.copy()
        
        for column in features_encoded.columns:
            if features_encoded[column].dtype == 'object':
                if column not in self.label_encoders:
                    self.label_encoders[column] = LabelEncoder()
                    features_encoded[column] = self.label_encoders[column].fit_transform(features_encoded[column])
                else:
                    # Gérer les nouvelles valeurs
                    try:
                        features_encoded[column] = self.label_encoders[column].transform(features_encoded[column])
                    except ValueError:
                        # Valeur inconnue, utiliser -1
                        features_encoded[column] = -1
        
        return features_encoded
    
    def train_model(self, historical_data: List[Dict], model_type: str = 'random_forest') -> Dict:
        """
        Entraîne le modèle avec les données historiques
        """
        try:
            # Préparer les données
            X, y = self.prepare_training_data(historical_data)
            
            # Diviser en train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Standardiser les features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Sélectionner le modèle
            if model_type not in self.models:
                raise ValueError(f"Type de modèle non supporté: {model_type}")
            
            self.current_model = self.models[model_type]
            
            # Entraîner le modèle
            self.current_model.fit(X_train_scaled, y_train)
            
            # Évaluer le modèle
            y_pred = self.current_model.predict(X_test_scaled)
            
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
                'model_type': model_type,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Validation croisée
            cv_scores = cross_val_score(
                self.current_model, X_train_scaled, y_train, 
                cv=5, scoring='r2'
            )
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
            
            self.is_trained = True
            
            # Sauvegarder le modèle
            self.save_model()
            
            logger.info(f"Modèle entraîné avec succès. R²: {metrics['r2']:.3f}")
            
            return {
                'success': True,
                'metrics': metrics,
                'message': f"Modèle {model_type} entraîné avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_surf_conditions(self, weather_data: Dict) -> Dict:
        """
        Prédit la qualité des conditions de surf
        """
        if not self.is_trained or self.current_model is None:
            return {
                'success': False,
                'error': 'Modèle non entraîné'
            }
        
        try:
            # Préparer les features
            features = self._create_features(pd.DataFrame([weather_data]))
            features_encoded = self._encode_categorical_features(features)
            
            # Standardiser
            features_scaled = self.scaler.transform(features_encoded.values)
            
            # Prédiction
            prediction = self.current_model.predict(features_scaled)[0]
            
            # Interprétation de la prédiction
            interpretation = self._interpret_prediction(prediction, weather_data)
            
            return {
                'success': True,
                'predicted_score': round(prediction, 1),
                'interpretation': interpretation,
                'confidence': self._calculate_prediction_confidence(prediction),
                'recommendations': self._generate_recommendations(prediction, weather_data)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _interpret_prediction(self, score: float, weather_data: Dict) -> str:
        """
        Interprète le score prédit
        """
        if score >= 8:
            return "Conditions EXCELLENTES pour le surf !"
        elif score >= 6:
            return "Bonnes conditions pour surfer"
        elif score >= 4:
            return "Conditions moyennes, surfez avec précaution"
        else:
            return "Conditions difficiles, attendez un meilleur moment"
    
    def _calculate_prediction_confidence(self, score: float) -> str:
        """
        Calcule la confiance de la prédiction
        """
        if score >= 8 or score <= 2:
            return "Élevée"  # Scores extrêmes = plus de confiance
        elif score >= 6 or score <= 4:
            return "Moyenne"
        else:
            return "Faible"  # Scores intermédiaires = moins de confiance
    
    def _generate_recommendations(self, score: float, weather_data: Dict) -> List[str]:
        """
        Génère des recommandations basées sur la prédiction
        """
        recommendations = []
        
        if score >= 8:
            recommendations.extend([
                "C'est le moment parfait pour surfer !",
                "Préparez votre équipement et partez !",
                "Idéal pour tous les niveaux"
            ])
        elif score >= 6:
            recommendations.extend([
                "Bon moment pour une session",
                "Vérifiez votre équipement",
                "Surfez avec un ami pour plus de sécurité"
            ])
        elif score >= 4:
            recommendations.extend([
                "Conditions acceptables mais soyez prudent",
                "Évitez les spots difficiles",
                "Vérifiez les conditions en temps réel"
            ])
        else:
            recommendations.extend([
                "Pas recommandé de surfer aujourd'hui",
                "Attendez une amélioration des conditions",
                "Consultez les prévisions pour demain"
            ])
        
        return recommendations
    
    def save_model(self):
        """
        Sauvegarde le modèle entraîné
        """
        try:
            # Sauvegarder le modèle
            joblib.dump(self.current_model, self.model_path)
            
            # Sauvegarder le scaler
            joblib.dump(self.scaler, self.scaler_path)
            
            # Sauvegarder les encoders
            encoders_path = 'surf_label_encoders.pkl'
            joblib.dump(self.label_encoders, encoders_path)
            
            logger.info("Modèle sauvegardé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
    
    def load_model(self):
        """
        Charge un modèle sauvegardé
        """
        try:
            if os.path.exists(self.model_path):
                self.current_model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                
                # Charger les encoders
                encoders_path = 'surf_label_encoders.pkl'
                if os.path.exists(encoders_path):
                    self.label_encoders = joblib.load(encoders_path)
                
                self.is_trained = True
                logger.info("Modèle chargé avec succès")
                
        except Exception as e:
            logger.warning(f"Impossible de charger le modèle: {e}")
            self.is_trained = False
    
    def get_model_info(self) -> Dict:
        """
        Retourne les informations sur le modèle
        """
        return {
            'is_trained': self.is_trained,
            'model_type': type(self.current_model).__name__ if self.current_model else None,
            'feature_count': len(self.feature_columns),
            'features': self.feature_columns,
            'model_path': self.model_path
        }
    
    def generate_sample_data(self, num_samples: int = 1000) -> List[Dict]:
        """
        Génère des données d'exemple pour tester le modèle
        """
        sample_data = []
        
        for i in range(num_samples):
            # Données météo réalistes
            sample = {
                'wave_height': np.random.uniform(0.5, 4.0),
                'wind_speed': np.random.uniform(5, 35),
                'wind_direction': np.random.uniform(0, 360),
                'water_temp': np.random.uniform(15, 28),
                'tide': np.random.uniform(-2, 2),
                'pressure': np.random.uniform(1000, 1030),
                'precipitation': np.random.uniform(0, 10),
                'timestamp': (datetime.now() - timedelta(days=np.random.randint(0, 30))).isoformat(),
                'spot_name': np.random.choice(['Taghazout', 'Essaouira', 'Agadir', 'Bouznika']),
                'surfer_level': np.random.choice(['beginner', 'intermediate', 'advanced'])
            }
            sample_data.append(sample)
        
        return sample_data

# Instance globale du modèle
surf_prediction_model = SurfPredictionModel()
