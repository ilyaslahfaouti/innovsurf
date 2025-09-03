# recommendation_system.py
"""
Système de recommandation intelligent pour YalaSurf
Utilise l'IA pour recommander spots, équipements et moniteurs
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
from .models import SurfSpot, Equipment, SurfClub, Surfer, SurfLesson
from .surf_prediction_model import surf_prediction_model

logger = logging.getLogger(__name__)

class SurfRecommendationSystem:
    """
    Système de recommandation IA pour le surf
    """
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.scaler = StandardScaler()
        self.is_initialized = False
        
    def initialize_system(self):
        """
        Initialise le système de recommandation
        """
        try:
            # Charger et préparer les données
            self._prepare_recommendation_data()
            self.is_initialized = True
            logger.info("Système de recommandation initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            self.is_initialized = False
    
    def _prepare_recommendation_data(self):
        """
        Prépare les données pour le système de recommandation
        """
        # Charger les données depuis la base
        self.spots_data = self._get_spots_data()
        self.equipment_data = self._get_equipment_data()
        self.monitors_data = self._get_monitors_data()
        
        # Créer les matrices de similarité
        self._create_similarity_matrices()
    
    def _get_spots_data(self) -> pd.DataFrame:
        """
        Récupère et prépare les données des spots
        """
        try:
            spots = SurfSpot.objects.all()
            spots_list = []
            
            for spot in spots:
                spot_data = {
                    'id': spot.id,
                    'name': spot.name,
                    'location': spot.location,
                    'difficulty_level': spot.difficulty_level,
                    'wave_type': spot.wave_type,
                    'best_season': spot.best_season,
                    'crowd_level': getattr(spot, 'crowd_level', 'medium'),
                    'accessibility': getattr(spot, 'accessibility', 'medium'),
                    'features': f"{spot.name} {spot.location} {spot.difficulty_level} {spot.wave_type} {spot.best_season}"
                }
                spots_list.append(spot_data)
            
            return pd.DataFrame(spots_list)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des spots: {e}")
            return pd.DataFrame()
    
    def _get_equipment_data(self) -> pd.DataFrame:
        """
        Récupère et prépare les données d'équipement
        """
        try:
            equipment = Equipment.objects.all()
            equipment_list = []
            
            for eq in equipment:
                eq_data = {
                    'id': eq.id,
                    'name': eq.name,
                    'description': eq.description,
                    'size': eq.size,
                    'state': eq.state,
                    'equipment_type': eq.equipment_type.type,
                    'features': f"{eq.name} {eq.description} {eq.size} {eq.state} {eq.equipment_type.type}"
                }
                equipment_list.append(eq_data)
            
            return pd.DataFrame(equipment_list)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'équipement: {e}")
            return pd.DataFrame()
    
    def _get_monitors_data(self) -> pd.DataFrame:
        """
        Récupère et prépare les données des moniteurs
        """
        try:
            # Récupérer les moniteurs depuis les clubs
            monitors_list = []
            
            # Simulation de données de moniteurs (à adapter selon tes modèles)
            sample_monitors = [
                {
                    'id': 1,
                    'name': 'Ahmed Benali',
                    'experience_years': 8,
                    'specialties': ['débutants', 'longboard'],
                    'languages': ['arabe', 'français', 'anglais'],
                    'rating': 4.8,
                    'location': 'Taghazout'
                },
                {
                    'id': 2,
                    'name': 'Sarah Martin',
                    'experience_years': 5,
                    'specialties': ['intermédiaire', 'shortboard'],
                    'languages': ['français', 'anglais'],
                    'rating': 4.6,
                    'location': 'Essaouira'
                },
                {
                    'id': 3,
                    'name': 'Mohammed El Amrani',
                    'experience_years': 12,
                    'specialties': ['tous niveaux', 'big waves'],
                    'languages': ['arabe', 'français', 'anglais', 'espagnol'],
                    'rating': 4.9,
                    'location': 'Agadir'
                }
            ]
            
            for monitor in sample_monitors:
                monitor_data = {
                    'id': monitor['id'],
                    'name': monitor['name'],
                    'experience_years': monitor['experience_years'],
                    'specialties': ', '.join(monitor['specialties']),
                    'languages': ', '.join(monitor['languages']),
                    'rating': monitor['rating'],
                    'location': monitor['location'],
                    'features': f"{monitor['name']} {monitor['specialties']} {monitor['languages']} {monitor['location']}"
                }
                monitors_list.append(monitor_data)
            
            return pd.DataFrame(monitors_list)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des moniteurs: {e}")
            return pd.DataFrame()
    
    def _create_similarity_matrices(self):
        """
        Crée les matrices de similarité pour les recommandations
        """
        try:
            # Matrice de similarité pour les spots
            if not self.spots_data.empty:
                spot_features = self.tfidf_vectorizer.fit_transform(self.spots_data['features'])
                self.spots_similarity = cosine_similarity(spot_features)
            
            # Matrice de similarité pour l'équipement
            if not self.equipment_data.empty:
                equipment_features = self.tfidf_vectorizer.transform(self.equipment_data['features'])
                self.equipment_similarity = cosine_similarity(equipment_features)
            
            # Matrice de similarité pour les moniteurs
            if not self.monitors_data.empty:
                monitor_features = self.tfidf_vectorizer.transform(self.monitors_data['features'])
                self.monitors_similarity = cosine_similarity(monitor_features)
                
        except Exception as e:
            logger.error(f"Erreur lors de la création des matrices de similarité: {e}")
    
    def recommend_spots(self, user_preferences: Dict, num_recommendations: int = 5) -> List[Dict]:
        """
        Recommande des spots de surf basés sur les préférences utilisateur
        """
        if not self.is_initialized:
            return []
        
        try:
            # Calculer le score de similarité pour chaque spot
            spot_scores = []
            
            for idx, spot in self.spots_data.iterrows():
                score = self._calculate_spot_score(spot, user_preferences)
                spot_scores.append({
                    'spot': spot.to_dict(),
                    'score': score
                })
            
            # Trier par score et retourner les meilleurs
            spot_scores.sort(key=lambda x: x['score'], reverse=True)
            
            recommendations = []
            for item in spot_scores[:num_recommendations]:
                spot_info = item['spot']
                spot_info['recommendation_score'] = round(item['score'], 2)
                spot_info['why_recommended'] = self._explain_spot_recommendation(spot_info, user_preferences)
                recommendations.append(spot_info)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur lors de la recommandation de spots: {e}")
            return []
    
    def _calculate_spot_score(self, spot: pd.Series, user_preferences: Dict) -> float:
        """
        Calcule un score de recommandation pour un spot
        """
        score = 0.0
        
        # Score basé sur le niveau de difficulté
        user_level = user_preferences.get('surf_level', 'beginner')
        spot_difficulty = spot['difficulty_level']
        
        if user_level == 'beginner' and spot_difficulty == 'beginner':
            score += 10
        elif user_level == 'intermediate' and spot_difficulty in ['beginner', 'intermediate']:
            score += 8
        elif user_level == 'advanced':
            score += 6  # Tous les niveaux sont OK pour les avancés
        
        # Score basé sur la localisation
        preferred_location = user_preferences.get('preferred_location', '')
        if preferred_location and preferred_location.lower() in spot['location'].lower():
            score += 5
        
        # Score basé sur la saison
        current_month = datetime.now().month
        best_season = spot['best_season']
        if self._is_good_season(current_month, best_season):
            score += 3
        
        # Score basé sur le type de vague
        preferred_wave_type = user_preferences.get('preferred_wave_type', '')
        if preferred_wave_type and preferred_wave_type.lower() in spot['wave_type'].lower():
            score += 4
        
        # Score basé sur l'affluence
        crowd_preference = user_preferences.get('crowd_preference', 'medium')
        if crowd_preference == spot['crowd_level']:
            score += 2
        
        return score
    
    def _is_good_season(self, current_month: int, best_season: str) -> bool:
        """
        Vérifie si la saison actuelle est bonne pour le spot
        """
        season_mapping = {
            'spring': [3, 4, 5],
            'summer': [6, 7, 8],
            'autumn': [9, 10, 11],
            'winter': [12, 1, 2],
            'all_year': list(range(1, 13))
        }
        
        if best_season.lower() in season_mapping:
            return current_month in season_mapping[best_season.lower()]
        
        return True  # Par défaut, toujours OK
    
    def _explain_spot_recommendation(self, spot: Dict, user_preferences: Dict) -> str:
        """
        Explique pourquoi ce spot est recommandé
        """
        reasons = []
        
        user_level = user_preferences.get('surf_level', 'beginner')
        if spot['difficulty_level'] == user_level:
            reasons.append(f"Niveau parfait pour votre expérience ({user_level})")
        
        if spot['difficulty_level'] == 'beginner' and user_level == 'beginner':
            reasons.append("Idéal pour débuter en toute sécurité")
        
        if 'Taghazout' in spot['name'] or 'Taghazout' in spot['location']:
            reasons.append("Spot légendaire du Maroc")
        
        if 'Essaouira' in spot['name'] or 'Essaouira' in spot['location']:
            reasons.append("Villes des alizés, conditions constantes")
        
        return " et ".join(reasons) if reasons else "Spot de qualité recommandé par notre IA"
    
    def recommend_equipment(self, user_profile: Dict, spot_conditions: Dict, num_recommendations: int = 3) -> List[Dict]:
        """
        Recommande de l'équipement basé sur le profil utilisateur et les conditions
        """
        if not self.is_initialized:
            return []
        
        try:
            equipment_scores = []
            
            for idx, eq in self.equipment_data.iterrows():
                score = self._calculate_equipment_score(eq, user_profile, spot_conditions)
                equipment_scores.append({
                    'equipment': eq.to_dict(),
                    'score': score
                })
            
            # Trier par score
            equipment_scores.sort(key=lambda x: x['score'], reverse=True)
            
            recommendations = []
            for item in equipment_scores[:num_recommendations]:
                eq_info = item['equipment']
                eq_info['recommendation_score'] = round(item['score'], 2)
                eq_info['why_recommended'] = self._explain_equipment_recommendation(eq_info, user_profile, spot_conditions)
                recommendations.append(eq_info)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur lors de la recommandation d'équipement: {e}")
            return []
    
    def _calculate_equipment_score(self, equipment: pd.Series, user_profile: Dict, spot_conditions: Dict) -> float:
        """
        Calcule un score de recommandation pour l'équipement
        """
        score = 0.0
        
        # Score basé sur le type d'équipement
        user_level = user_profile.get('surf_level', 'beginner')
        equipment_type = equipment['equipment_type']
        
        if equipment_type == 'surfboard':
            if user_level == 'beginner':
                score += 8  # Les débutants ont besoin de planches
            else:
                score += 6
        elif equipment_type == 'surfsuit':
            water_temp = spot_conditions.get('water_temp', 20)
            if water_temp < 20:  # Besoin de combinaison
                score += 10
            else:
                score += 5
        elif equipment_type == 'leash':
            score += 7  # Toujours important
        
        # Score basé sur la taille
        user_size = user_profile.get('size', 'medium')
        if equipment['size'] == user_size:
            score += 5
        
        # Score basé sur l'état
        if equipment['state'] == 'excellent':
            score += 3
        elif equipment['state'] == 'good':
            score += 2
        
        return score
    
    def _explain_equipment_recommendation(self, equipment: Dict, user_profile: Dict, spot_conditions: Dict) -> str:
        """
        Explique pourquoi cet équipement est recommandé
        """
        reasons = []
        
        if equipment['equipment_type'] == 'surfboard':
            reasons.append("Planche essentielle pour surfer")
        elif equipment['equipment_type'] == 'surfsuit':
            water_temp = spot_conditions.get('water_temp', 20)
            if water_temp < 20:
                reasons.append(f"Combinaison nécessaire (eau à {water_temp}°C)")
            else:
                reasons.append("Combinaison pour plus de confort")
        elif equipment['equipment_type'] == 'leash':
            reasons.append("Leash de sécurité obligatoire")
        
        if equipment['state'] == 'excellent':
            reasons.append("État parfait")
        
        return " et ".join(reasons) if reasons else "Équipement de qualité recommandé"
    
    def recommend_monitors(self, user_profile: Dict, spot_name: str, num_recommendations: int = 3) -> List[Dict]:
        """
        Recommande des moniteurs basés sur le profil utilisateur et le spot
        """
        if not self.is_initialized:
            return []
        
        try:
            monitor_scores = []
            
            for idx, monitor in self.monitors_data.iterrows():
                score = self._calculate_monitor_score(monitor, user_profile, spot_name)
                monitor_scores.append({
                    'monitor': monitor.to_dict(),
                    'score': score
                })
            
            # Trier par score
            monitor_scores.sort(key=lambda x: x['score'], reverse=True)
            
            recommendations = []
            for item in monitor_scores[:num_recommendations]:
                monitor_info = item['monitor']
                monitor_info['recommendation_score'] = round(item['score'], 2)
                monitor_info['why_recommended'] = self._explain_monitor_recommendation(monitor_info, user_profile, spot_name)
                recommendations.append(monitor_info)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur lors de la recommandation de moniteurs: {e}")
            return []
    
    def _calculate_monitor_score(self, monitor: pd.Series, user_profile: Dict, spot_name: str) -> float:
        """
        Calcule un score de recommandation pour un moniteur
        """
        score = 0.0
        
        # Score basé sur l'expérience
        experience_years = monitor['experience_years']
        if experience_years >= 10:
            score += 10
        elif experience_years >= 5:
            score += 7
        else:
            score += 4
        
        # Score basé sur la localisation
        if monitor['location'].lower() in spot_name.lower():
            score += 8  # Moniteur local au spot
        
        # Score basé sur les spécialités
        user_level = user_profile.get('surf_level', 'beginner')
        specialties = monitor['specialties'].lower()
        if user_level in specialties:
            score += 6
        
        # Score basé sur la note
        rating = monitor['rating']
        score += rating * 2  # Note sur 10, donc max 20 points
        
        # Score basé sur les langues
        user_language = user_profile.get('preferred_language', 'français')
        if user_language.lower() in monitor['languages'].lower():
            score += 5
        
        return score
    
    def _explain_monitor_recommendation(self, monitor: Dict, user_profile: Dict, spot_name: str) -> str:
        """
        Explique pourquoi ce moniteur est recommandé
        """
        reasons = []
        
        if monitor['experience_years'] >= 10:
            reasons.append(f"Moniteur expérimenté ({monitor['experience_years']} ans)")
        
        if monitor['location'].lower() in spot_name.lower():
            reasons.append("Moniteur local, connaît parfaitement le spot")
        
        if monitor['rating'] >= 4.5:
            reasons.append(f"Excellent moniteur (note: {monitor['rating']})")
        
        user_language = user_profile.get('preferred_language', 'français')
        if user_language.lower() in monitor['languages'].lower():
            reasons.append(f"Parle votre langue ({user_language})")
        
        return " et ".join(reasons) if reasons else "Moniteur qualifié recommandé par notre IA"
    
    def get_personalized_recommendations(self, user_id: int, num_recommendations: int = 5) -> Dict:
        """
        Génère des recommandations personnalisées complètes pour un utilisateur
        """
        try:
            # Récupérer le profil utilisateur
            user_profile = self._get_user_profile(user_id)
            
            # Récupérer les conditions météo actuelles
            current_conditions = self._get_current_weather_conditions()
            
            # Recommandations de spots
            spot_recommendations = self.recommend_spots(user_profile, num_recommendations)
            
            # Recommandations d'équipement
            equipment_recommendations = self.recommend_equipment(user_profile, current_conditions, 3)
            
            # Recommandations de moniteurs
            preferred_spot = spot_recommendations[0]['name'] if spot_recommendations else 'Taghazout'
            monitor_recommendations = self.recommend_monitors(user_profile, preferred_spot, 3)
            
            return {
                'success': True,
                'user_profile': user_profile,
                'current_conditions': current_conditions,
                'recommendations': {
                    'spots': spot_recommendations,
                    'equipment': equipment_recommendations,
                    'monitors': monitor_recommendations
                },
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des recommandations personnalisées: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_user_profile(self, user_id: int) -> Dict:
        """
        Récupère le profil utilisateur
        """
        try:
            # Simulation d'un profil utilisateur (à adapter selon tes modèles)
            return {
                'surf_level': 'intermediate',
                'preferred_location': 'Taghazout',
                'preferred_wave_type': 'right',
                'crowd_preference': 'medium',
                'size': 'medium',
                'preferred_language': 'français'
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du profil utilisateur: {e}")
            return {}
    
    def _get_current_weather_conditions(self) -> Dict:
        """
        Récupère les conditions météo actuelles
        """
        try:
            # Simulation des conditions actuelles (à adapter selon ton API Windy)
            return {
                'water_temp': 22,
                'wave_height': 1.5,
                'wind_speed': 12,
                'wind_direction': 180
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des conditions météo: {e}")
            return {}

# Instance globale du système de recommandation
recommendation_system = SurfRecommendationSystem()
