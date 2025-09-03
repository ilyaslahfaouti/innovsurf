# booking_prediction.py
"""
Système d'analyse prédictive des réservations pour YalaSurf
Prédit la demande et optimise les prix dynamiquement
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, classification_report, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import joblib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Import Django models
from django.db import models
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# ==================== MÉTHODES ETL ====================

def extract_booking_data(self, days_back: int = 730) -> List[Dict]:
    """
    EXTRACT: Récupère les vraies données de réservation depuis la base Django
    """
    try:
        from .models import SurfLesson, SurfSession, Equipment, SurfClub, Monitor, LessonSchedule, Order
        
        # Date de début
        start_date = timezone.now() - timedelta(days=days_back)
        
        # Récupérer les leçons de surf via les sessions
        surf_lessons = SurfLesson.objects.filter(
            surf_session__lesson_schedule__day__gte=start_date
        ).select_related('surfer', 'surf_session__lesson_schedule', 'surf_session__surf_club', 'surf_session__monitor')
        
        # Récupérer les sessions de surf
        surf_sessions = SurfSession.objects.filter(
            lesson_schedule__day__gte=start_date
        ).select_related('surf_club', 'monitor', 'lesson_schedule')
        
        # Récupérer les commandes d'équipement
        equipment_orders = Order.objects.filter(
            order_date__gte=start_date
        ).select_related('surfer', 'surf_club')
        
        # Récupérer les équipements disponibles
        available_equipment = Equipment.objects.filter(
            material_type='rent',
            quantity__gt=0
        ).select_related('surf_club', 'equipment_type')
        
        logger.info(f"Données extraites: {surf_lessons.count()} leçons, {surf_sessions.count()} sessions, {equipment_orders.count()} commandes, {available_equipment.count()} équipements")
        
        return {
            'surf_lessons': surf_lessons,
            'surf_sessions': surf_sessions,
            'equipment_orders': equipment_orders,
            'available_equipment': available_equipment
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données: {e}")
        return {}

def transform_booking_data(self, raw_data: Dict) -> List[Dict]:
    """
    TRANSFORM: Transforme les données brutes en format adapté pour l'IA
    """
    try:
        transformed_data = []
        
        # Transformer les leçons de surf
        for lesson in raw_data.get('surf_lessons', []):
            lesson_data = self._transform_surf_lesson(lesson)
            if lesson_data:
                transformed_data.append(lesson_data)
        
        # Transformer les sessions de surf
        for session in raw_data.get('surf_sessions', []):
            session_data = self._transform_surf_session(session)
            if session_data:
                transformed_data.append(session_data)
        
        # Transformer les commandes d'équipement
        for order in raw_data.get('equipment_orders', []):
            order_data = self._transform_equipment_order(order)
            if order_data:
                transformed_data.append(order_data)
        
        logger.info(f"Données transformées: {len(transformed_data)} enregistrements")
        return transformed_data
        
    except Exception as e:
        logger.error(f"Erreur lors de la transformation des données: {e}")
        return []

def _transform_surf_lesson(self, lesson) -> Optional[Dict]:
    """
    Transforme une leçon de surf en données structurées
    """
    try:
        # Récupérer la date depuis la session
        lesson_date = lesson.surf_session.lesson_schedule.day
        
        # Récupérer les données météo si disponibles
        spot_location = lesson.surf_session.surf_club.surf_spot.name if lesson.surf_session.surf_club.surf_spot else 'Unknown'
        weather_data = self._get_weather_data_for_date(lesson_date, spot_location)
        
        # Calculer les facteurs de demande
        demand_factors = self._calculate_demand_factors(lesson_date, weather_data)
        
        # Données transformées
        lesson_data = {
            'id': lesson.id,
            'booking_date': lesson_date.isoformat(),
            'month': lesson_date.month,
            'season': self._get_season(lesson_date.month),
            'day_of_week': lesson_date.weekday(),
            'is_weekend': 1 if lesson_date.weekday() >= 5 else 0,
            'is_holiday': 1 if lesson_date.month in [7, 8, 12] else 0,
            
            # Conditions météo
            'wave_height': weather_data.get('wave_height', 1.5),
            'wind_speed': weather_data.get('wind_speed', 15),
            'water_temp': weather_data.get('water_temp', 22),
            'weather_score': weather_data.get('weather_score', 7.0),
            
            # Facteurs de demande
            'weekend_factor': demand_factors['weekend_factor'],
            'holiday_factor': demand_factors['holiday_factor'],
            'weather_factor': demand_factors['weather_factor'],
            
            # Résultats
            'predicted_demand': demand_factors['predicted_demand'],
            'actual_bookings': 1,  # Chaque leçon = 1 réservation
            'base_price': float(lesson.total_price or 100),
            'optimized_price': float(lesson.total_price or 100),
            'price_multiplier': 1.0,
            'cancellation_probability': 0.1,
            'was_cancelled': 0,  # Pas de statut d'annulation dans le modèle actuel
            
            # Informations supplémentaires
            'spot_name': spot_location,
            'surf_level': lesson.surfer.level if lesson.surfer else 'beginner',
            'lesson_duration': 60,  # Durée par défaut
            'monitor_experience': 2  # Expérience par défaut
        }
        
        return lesson_data
        
    except Exception as e:
        logger.warning(f"Impossible de transformer la leçon {lesson.id}: {e}")
        return None

def _transform_surf_session(self, session) -> Optional[Dict]:
    """
    Transforme une session de surf en données structurées
    """
    try:
        # Récupérer la date depuis le planning
        session_date = session.lesson_schedule.day
        
        # Récupérer les données météo
        spot_location = session.surf_club.surf_spot.name if session.surf_club.surf_spot else 'Unknown'
        weather_data = self._get_weather_data_for_date(session_date, spot_location)
        
        # Calculer les facteurs de demande
        demand_factors = self._calculate_demand_factors(session_date, weather_data)
        
        # Données transformées
        session_data = {
            'id': session.id,
            'booking_date': session_date.isoformat(),
            'month': session_date.month,
            'season': self._get_season(session_date.month),
            'day_of_week': session_date.weekday(),
            'is_weekend': 1 if session_date.weekday() >= 5 else 0,
            'is_holiday': 1 if session_date.month in [7, 8, 12] else 0,
            
            # Conditions météo
            'wave_height': weather_data.get('wave_height', 1.5),
            'wind_speed': weather_data.get('wind_speed', 15),
            'water_temp': weather_data.get('water_temp', 22),
            'weather_score': weather_data.get('weather_score', 7.0),
            
            # Facteurs de demande
            'weekend_factor': demand_factors['weekend_factor'],
            'holiday_factor': demand_factors['holiday_factor'],
            'weather_factor': demand_factors['weather_factor'],
            
            # Résultats
            'predicted_demand': demand_factors['predicted_demand'],
            'actual_bookings': 1,
            'base_price': 50.0,  # Prix par défaut pour les sessions
            'optimized_price': 50.0,
            'price_multiplier': 1.0,
            'cancellation_probability': 0.1,
            'was_cancelled': 0,  # Pas de statut d'annulation dans le modèle actuel
            
            # Informations supplémentaires
            'spot_name': spot_location,
            'surf_level': 'intermediate',  # Niveau par défaut pour les sessions
            'session_type': 'surf_session'
        }
        
        return session_data
        
    except Exception as e:
        logger.warning(f"Impossible de transformer la session {session.id}: {e}")
        return None

def _transform_equipment_order(self, order) -> Optional[Dict]:
    """
    Transforme une commande d'équipement en données structurées
    """
    try:
        # Récupérer les données météo
        spot_location = order.surf_club.surf_spot.name if order.surf_club.surf_spot else 'Unknown'
        weather_data = self._get_weather_data_for_date(order.order_date, spot_location)
        
        # Calculer les facteurs de demande
        demand_factors = self._calculate_demand_factors(order.order_date, weather_data)
        
        # Données transformées
        order_data = {
            'id': order.id,
            'booking_date': order.order_date.isoformat(),
            'month': order.order_date.month,
            'season': self._get_season(order.order_date.month),
            'day_of_week': order.order_date.weekday(),
            'is_weekend': 1 if order.order_date.weekday() >= 5 else 0,
            'is_holiday': 1 if order.order_date.month in [7, 8, 12] else 0,
            
            # Conditions météo
            'wave_height': weather_data.get('wave_height', 1.5),
            'wind_speed': weather_data.get('wind_speed', 15),
            'water_temp': weather_data.get('water_temp', 22),
            'weather_score': weather_data.get('weather_score', 7.0),
            
            # Facteurs de demande
            'weekend_factor': demand_factors['weekend_factor'],
            'holiday_factor': demand_factors['holiday_factor'],
            'weather_factor': demand_factors['weather_factor'],
            
            # Résultats
            'predicted_demand': demand_factors['predicted_demand'],
            'actual_bookings': 1,
            'base_price': float(order.total_price or 30),
            'optimized_price': float(order.total_price or 30),
            'price_multiplier': 1.0,
            'cancellation_probability': 0.05,
            'was_cancelled': 0,  # Les commandes sont rarement annulées
            
            # Informations supplémentaires
            'spot_name': spot_location,
            'equipment_type': 'surfboard',  # Type par défaut
            'order_type': 'equipment_order'
        }
        
        return order_data
        
    except Exception as e:
        logger.warning(f"Impossible de transformer la commande {order.id}: {e}")
        return None

def _get_weather_data_for_date(self, date: datetime, location: str) -> Dict:
    """
    Récupère les données météo pour une date et un lieu donnés
    """
    try:
        # Essayer de récupérer depuis l'API Windy ou la base de données
        from .windy_api_service import WindyAPIService
        
        windy_service = WindyAPIService()
        weather_data = windy_service.get_historical_weather(date, location)
        
        if weather_data:
            return {
                'wave_height': weather_data.get('wave_height', 1.5),
                'wind_speed': weather_data.get('wind_speed', 15),
                'water_temp': weather_data.get('water_temp', 22),
                'weather_score': self._calculate_weather_score(
                    weather_data.get('wave_height', 1.5),
                    weather_data.get('wind_speed', 15),
                    weather_data.get('water_temp', 22)
                )
            }
        
    except Exception as e:
        logger.warning(f"Impossible de récupérer les données météo pour {date}: {e}")
    
    # Données par défaut si pas de données météo
    return {
        'wave_height': 1.5,
        'wind_speed': 15,
        'water_temp': 22,
        'weather_score': 7.0
    }

def _get_season(self, month: int) -> str:
    """
    Détermine la saison à partir du mois
    """
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'

def _calculate_demand_factors(self, date: datetime, weather_data: Dict) -> Dict:
    """
    Calcule les facteurs de demande pour une date donnée
    """
    month = date.month
    day_of_week = date.weekday()
    
    # Facteur weekend
    weekend_factor = 1.3 if day_of_week >= 5 else 1.0
    
    # Facteur vacances
    holiday_factor = 1.2 if month in [7, 8, 12] else 1.0
    
    # Facteur météo
    weather_score = weather_data.get('weather_score', 7.0)
    weather_factor = 1.0 + (weather_score - 5) * 0.1
    
    # Demande prédite de base
    base_demand = 1.0
    if month in [12, 1, 2]:  # Hiver
        base_demand = 0.6
    elif month in [6, 7, 8]:  # Été
        base_demand = 1.2
    
    predicted_demand = base_demand * weekend_factor * holiday_factor * weather_factor
    
    return {
        'weekend_factor': round(weekend_factor, 2),
        'holiday_factor': round(holiday_factor, 2),
        'weather_factor': round(weather_factor, 2),
        'predicted_demand': round(predicted_demand, 2)
    }

def load_transformed_data(self, transformed_data: List[Dict]) -> bool:
    """
    LOAD: Charge les données transformées dans le système de prédiction
    """
    try:
        if not transformed_data:
            logger.warning("Aucune donnée transformée à charger")
            return False
        
        # Convertir en DataFrame
        self.training_data = pd.DataFrame(transformed_data)
        
        # Vérifier la qualité des données
        data_quality = self._check_data_quality(self.training_data)
        
        if not data_quality['is_valid']:
            logger.warning(f"Problèmes de qualité des données: {data_quality['issues']}")
        
        logger.info(f"Données chargées: {len(self.training_data)} enregistrements")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données: {e}")
        return False

def _check_data_quality(self, df: pd.DataFrame) -> Dict:
    """
    Vérifie la qualité des données d'entraînement
    """
    issues = []
    
    # Vérifier les valeurs manquantes
    missing_values = df.isnull().sum()
    if missing_values.any():
        issues.append(f"Valeurs manquantes: {missing_values[missing_values > 0].to_dict()}")
    
    # Vérifier les types de données
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_values = df[col].nunique()
            if unique_values > 100:
                issues.append(f"Colonne {col} a trop de valeurs uniques: {unique_values}")
    
    # Vérifier la cohérence des données
    if 'actual_bookings' in df.columns:
        if (df['actual_bookings'] < 0).any():
            issues.append("Valeurs négatives dans actual_bookings")
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues,
        'total_records': len(df),
        'columns': list(df.columns)
    }

def run_full_etl_pipeline(self, days_back: int = 730) -> Dict:
    """
    Exécute le pipeline ETL complet
    """
    try:
        logger.info("Démarrage du pipeline ETL complet...")
        
        # 1. EXTRACT
        logger.info("Étape 1: Extraction des données...")
        raw_data = self.extract_booking_data(days_back)
        
        if not raw_data:
            return {
                'success': False,
                'error': 'Aucune donnée extraite de la base'
            }
        
        # 2. TRANSFORM
        logger.info("Étape 2: Transformation des données...")
        transformed_data = self.transform_booking_data(raw_data)
        
        if not transformed_data:
            return {
                'success': False,
                'error': 'Aucune donnée transformée'
            }
        
        # 3. LOAD
        logger.info("Étape 3: Chargement des données...")
        load_success = self.load_transformed_data(transformed_data)
        
        if not load_success:
            return {
                'success': False,
                'error': 'Échec du chargement des données'
            }
        
        # 4. Entraînement automatique des modèles
        logger.info("Étape 4: Entraînement des modèles...")
        training_results = self._train_all_models()
        
        logger.info("Pipeline ETL terminé avec succès!")
        
        return {
            'success': True,
            'etl_stats': {
                'raw_records': sum(len(data) for data in raw_data.values()),
                'transformed_records': len(transformed_data),
                'days_covered': days_back
            },
            'training_results': training_results,
            'message': 'Pipeline ETL et entraînement terminés avec succès'
        }
        
    except Exception as e:
        logger.error(f"Erreur dans le pipeline ETL: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def _train_all_models(self) -> Dict:
    """
    Entraîne tous les modèles avec les données chargées
    """
    try:
        if not hasattr(self, 'training_data') or self.training_data.empty:
            return {
                'success': False,
                'error': 'Aucune donnée d\'entraînement disponible'
            }
        
        results = {}
        
        # Entraîner le modèle de demande
        demand_result = self.train_demand_prediction_model(
            self.training_data.to_dict('records'),
            'random_forest'
        )
        results['demand'] = demand_result
        
        # Entraîner le modèle de prix
        price_result = self.train_price_optimization_model(
            self.training_data.to_dict('records'),
            'random_forest'
        )
        results['price'] = price_result
        
        # Entraîner le modèle d'annulation
        cancellation_result = self.train_cancellation_prediction_model(
            self.training_data.to_dict('records'),
            'random_forest'
        )
        results['cancellation'] = cancellation_result
        
        # Sauvegarder les modèles
        self.save_models()
        
        return {
            'success': True,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement des modèles: {e}")
        return {
            'success': False,
            'error': str(e)
        }

class BookingPredictionSystem:
    """
    Système IA pour prédire la demande de réservations et optimiser les prix
    """
    
    def __init__(self):
        self.demand_model = None
        self.price_optimization_model = None
        self.cancellation_model = None
        # Scaler séparé pour chaque modèle
        self.demand_scaler = StandardScaler()
        self.price_scaler = StandardScaler()
        self.cancellation_scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        
        # Modèles disponibles
        self.models = {
            'demand': {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'linear': LinearRegression()
            },
            'price': {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'linear': LinearRegression()
            },
            'cancellation': {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'logistic': LogisticRegression(random_state=42)
            }
        }
        
        # Charger les modèles si ils existent
        self.load_models()
    
    # ==================== MÉTHODES ETL ====================
    
    def extract_booking_data(self, days_back: int = 730) -> Dict:
        """
        EXTRACT: Récupère les vraies données de réservation depuis la base Django
        """
        try:
            from .models import SurfLesson, SurfSession, Equipment, SurfClub, Monitor
            
            # Date de début
            start_date = timezone.now() - timedelta(days=days_back)
            
            # Récupérer les leçons de surf
            surf_lessons = SurfLesson.objects.filter(
                date__gte=start_date
            ).select_related('surf_club', 'monitor', 'surfer')
            
            # Récupérer les sessions de surf
            surf_sessions = SurfSession.objects.filter(
                date__gte=start_date
            ).select_related('surf_club', 'surfer')
            
            # Récupérer les équipements loués
            equipment_rentals = Equipment.objects.filter(
                is_rent=True,
                created_at__gte=start_date
            ).select_related('surf_club')
            
            logger.info(f"Données extraites: {surf_lessons.count()} leçons, {surf_sessions.count()} sessions, {equipment_rentals.count()} locations")
            
            return {
                'surf_lessons': surf_lessons,
                'surf_sessions': surf_sessions,
                'equipment_rentals': equipment_rentals
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des données: {e}")
            return {}
    
    def transform_booking_data(self, raw_data: Dict) -> List[Dict]:
        """
        TRANSFORM: Transforme les données brutes en format adapté pour l'IA
        """
        try:
            transformed_data = []
            
            # Transformer les leçons de surf
            for lesson in raw_data.get('surf_lessons', []):
                lesson_data = self._transform_surf_lesson(lesson)
                if lesson_data:
                    transformed_data.append(lesson_data)
            
            # Transformer les sessions de surf
            for session in raw_data.get('surf_sessions', []):
                session_data = self._transform_surf_session(session)
                if session_data:
                    transformed_data.append(session_data)
            
            # Transformer les locations d'équipement
            for rental in raw_data.get('equipment_rentals', []):
                rental_data = self._transform_equipment_rental(rental)
                if rental_data:
                    transformed_data.append(rental_data)
            
            logger.info(f"Données transformées: {len(transformed_data)} enregistrements")
            return transformed_data
            
        except Exception as e:
            logger.error(f"Erreur lors de la transformation des données: {e}")
            return []
    
    def _transform_surf_lesson(self, lesson) -> Optional[Dict]:
        """
        Transforme une leçon de surf en données structurées
        """
        try:
            # Récupérer les données météo si disponibles
            weather_data = self._get_weather_data_for_date(lesson.date, lesson.surf_club.location)
            
            # Calculer les facteurs de demande
            demand_factors = self._calculate_demand_factors(lesson.date, weather_data)
            
            # Données transformées
            lesson_data = {
                'id': lesson.id,
                'booking_date': lesson.date.isoformat(),
                'month': lesson.date.month,
                'season': self._get_season(lesson.date.month),
                'day_of_week': lesson.date.weekday(),
                'is_weekend': 1 if lesson.date.weekday() >= 5 else 0,
                'is_holiday': 1 if lesson.date.month in [7, 8, 12] else 0,
                
                # Conditions météo
                'wave_height': weather_data.get('wave_height', 1.5),
                'wind_speed': weather_data.get('wind_speed', 15),
                'water_temp': weather_data.get('water_temp', 22),
                'weather_score': weather_data.get('weather_score', 7.0),
                
                # Facteurs de demande
                'weekend_factor': demand_factors['weekend_factor'],
                'holiday_factor': demand_factors['holiday_factor'],
                'weather_factor': demand_factors['weather_factor'],
                
                # Résultats
                'predicted_demand': demand_factors['predicted_demand'],
                'actual_bookings': 1,  # Chaque leçon = 1 réservation
                'base_price': float(lesson.total_price or 100),
                'optimized_price': float(lesson.total_price or 100),
                'price_multiplier': 1.0,
                'cancellation_probability': 0.1,
                'was_cancelled': 1 if lesson.status == 'cancelled' else 0,
                
                # Informations supplémentaires
                'spot_name': lesson.surf_club.location if lesson.surf_club else 'Unknown',
                'surf_level': lesson.surfer.surf_level if lesson.surfer else 'beginner',
                'lesson_duration': lesson.duration if hasattr(lesson, 'duration') else 60,
                'monitor_experience': lesson.monitor.years_experience if lesson.monitor and hasattr(lesson.monitor, 'years_experience') else 2
            }
            
            return lesson_data
            
        except Exception as e:
            logger.warning(f"Impossible de transformer la leçon {lesson.id}: {e}")
            return None
    
    def _transform_surf_session(self, session) -> Optional[Dict]:
        """
        Transforme une session de surf en données structurées
        """
        try:
            # Récupérer les données météo
            weather_data = self._get_weather_data_for_date(session.date, session.surf_club.location)
            
            # Calculer les facteurs de demande
            demand_factors = self._calculate_demand_factors(session.date, weather_data)
            
            # Données transformées
            session_data = {
                'id': session.id,
                'booking_date': session.date.isoformat(),
                'month': session.date.month,
                'season': self._get_season(session.date.month),
                'day_of_week': session.date.weekday(),
                'is_weekend': 1 if session.date.weekday() >= 5 else 0,
                'is_holiday': 1 if session.date.month in [7, 8, 12] else 0,
                
                # Conditions météo
                'wave_height': weather_data.get('wave_height', 1.5),
                'wind_speed': weather_data.get('wind_speed', 15),
                'water_temp': weather_data.get('water_temp', 22),
                'weather_score': weather_data.get('weather_score', 7.0),
                
                # Facteurs de demande
                'weekend_factor': demand_factors['weekend_factor'],
                'holiday_factor': demand_factors['holiday_factor'],
                'weather_factor': demand_factors['weather_factor'],
                
                # Résultats
                'predicted_demand': demand_factors['predicted_demand'],
                'actual_bookings': 1,
                'base_price': float(session.price or 50),
                'optimized_price': float(session.price or 50),
                'price_multiplier': 1.0,
                'cancellation_probability': 0.1,
                'was_cancelled': 1 if session.status == 'cancelled' else 0,
                
                # Informations supplémentaires
                'spot_name': session.surf_club.location if session.surf_club else 'Unknown',
                'surf_level': session.surfer.surf_level if session.surfer else 'beginner',
                'session_type': 'surf_session'
            }
            
            return session_data
            
        except Exception as e:
            logger.warning(f"Impossible de transformer la session {session.id}: {e}")
            return None
    
    def _transform_equipment_rental(self, rental) -> Optional[Dict]:
        """
        Transforme une location d'équipement en données structurées
        """
        try:
            # Récupérer les données météo
            weather_data = self._get_weather_data_for_date(rental.created_at.date(), rental.surf_club.location)
            
            # Calculer les facteurs de demande
            demand_factors = self._calculate_demand_factors(rental.created_at.date(), weather_data)
            
            # Données transformées
            rental_data = {
                'id': rental.id,
                'booking_date': rental.created_at.isoformat(),
                'month': rental.created_at.month,
                'season': self._get_season(rental.created_at.month),
                'day_of_week': rental.created_at.weekday(),
                'is_weekend': 1 if rental.created_at.weekday() >= 5 else 0,
                'is_holiday': 1 if rental.created_at.month in [7, 8, 12] else 0,
                
                # Conditions météo
                'wave_height': weather_data.get('wave_height', 1.5),
                'wind_speed': weather_data.get('wind_speed', 15),
                'water_temp': weather_data.get('water_temp', 22),
                'weather_score': weather_data.get('weather_score', 7.0),
                
                # Facteurs de demande
                'weekend_factor': demand_factors['weekend_factor'],
                'holiday_factor': demand_factors['holiday_factor'],
                'weather_factor': demand_factors['weather_factor'],
                
                # Résultats
                'predicted_demand': demand_factors['predicted_demand'],
                'actual_bookings': 1,
                'base_price': float(rental.price or 30),
                'optimized_price': float(rental.price or 30),
                'price_multiplier': 1.0,
                'cancellation_probability': 0.05,
                'was_cancelled': 0,  # Les locations sont rarement annulées
                
                # Informations supplémentaires
                'spot_name': rental.surf_club.location if rental.surf_club else 'Unknown',
                'equipment_type': rental.equipment_type if hasattr(rental, 'equipment_type') else 'surfboard',
                'rental_type': 'equipment_rental'
            }
            
            return rental_data
            
        except Exception as e:
            logger.warning(f"Impossible de transformer la location {rental.id}: {e}")
            return None
    
    def _get_weather_data_for_date(self, date: datetime, location: str) -> Dict:
        """
        Récupère les données météo pour une date et un lieu donnés
        """
        try:
            # Essayer de récupérer depuis l'API Windy ou la base de données
            from .windy_api_service import WindyAPIService
            
            windy_service = WindyAPIService()
            weather_data = windy_service.get_historical_weather(date, location)
            
            if weather_data:
                return {
                    'wave_height': weather_data.get('wave_height', 1.5),
                    'wind_speed': weather_data.get('wind_speed', 15),
                    'water_temp': weather_data.get('water_temp', 22),
                    'weather_score': self._calculate_weather_score(
                        weather_data.get('wave_height', 1.5),
                        weather_data.get('wind_speed', 15),
                        weather_data.get('water_temp', 22)
                    )
                }
            
        except Exception as e:
            logger.warning(f"Impossible de récupérer les données météo pour {date}: {e}")
        
        # Données par défaut si pas de données météo
        return {
            'wave_height': 1.5,
            'wind_speed': 15,
            'water_temp': 22,
            'weather_score': 7.0
        }
    
    def _get_season(self, month: int) -> str:
        """
        Détermine la saison à partir du mois
        """
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def _calculate_demand_factors(self, date: datetime, weather_data: Dict) -> Dict:
        """
        Calcule les facteurs de demande pour une date donnée
        """
        month = date.month
        day_of_week = date.weekday()
        
        # Facteur weekend
        weekend_factor = 1.3 if day_of_week >= 5 else 1.0
        
        # Facteur vacances
        holiday_factor = 1.2 if month in [7, 8, 12] else 1.0
        
        # Facteur météo
        weather_score = weather_data.get('weather_score', 7.0)
        weather_factor = 1.0 + (weather_score - 5) * 0.1
        
        # Demande prédite de base
        base_demand = 1.0
        if month in [12, 1, 2]:  # Hiver
            base_demand = 0.6
        elif month in [6, 7, 8]:  # Été
            base_demand = 1.2
        
        predicted_demand = base_demand * weekend_factor * holiday_factor * weather_factor
        
        return {
            'weekend_factor': round(weekend_factor, 2),
            'holiday_factor': round(holiday_factor, 2),
            'weather_factor': round(weather_factor, 2),
            'predicted_demand': round(predicted_demand, 2)
        }
    
    def load_transformed_data(self, transformed_data: List[Dict]) -> bool:
        """
        LOAD: Charge les données transformées dans le système de prédiction
        """
        try:
            if not transformed_data:
                logger.warning("Aucune donnée transformée à charger")
                return False
            
            # Convertir en DataFrame
            self.training_data = pd.DataFrame(transformed_data)
            
            # Vérifier la qualité des données
            data_quality = self._check_data_quality(self.training_data)
            
            if not data_quality['is_valid']:
                logger.warning(f"Problèmes de qualité des données: {data_quality['issues']}")
            
            logger.info(f"Données chargées: {len(self.training_data)} enregistrements")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
            return False
    
    def _check_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        Vérifie la qualité des données d'entraînement
        """
        issues = []
        
        # Vérifier les valeurs manquantes
        missing_values = df.isnull().sum()
        if missing_values.any():
            issues.append(f"Valeurs manquantes: {missing_values[missing_values > 0].to_dict()}")
        
        # Vérifier les types de données
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_values = df[col].nunique()
                if unique_values > 100:
                    issues.append(f"Colonne {col} a trop de valeurs uniques: {unique_values}")
        
        # Vérifier la cohérence des données
        if 'actual_bookings' in df.columns:
            if (df['actual_bookings'] < 0).any():
                issues.append("Valeurs négatives dans actual_bookings")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'total_records': len(df),
            'columns': list(df.columns)
        }
    
    def run_full_etl_pipeline(self, days_back: int = 730) -> Dict:
        """
        Exécute le pipeline ETL complet
        """
        try:
            logger.info("Démarrage du pipeline ETL complet...")
            
            # 1. EXTRACT
            logger.info("Étape 1: Extraction des données...")
            raw_data = self.extract_booking_data(days_back)
            
            if not raw_data:
                return {
                    'success': False,
                    'error': 'Aucune donnée extraite de la base'
                }
            
            # 2. TRANSFORM
            logger.info("Étape 2: Transformation des données...")
            transformed_data = self.transform_booking_data(raw_data)
            
            if not transformed_data:
                return {
                    'success': False,
                    'error': 'Aucune donnée transformée'
                }
            
            # 3. LOAD
            logger.info("Étape 3: Chargement des données...")
            load_success = self.load_transformed_data(transformed_data)
            
            if not load_success:
                return {
                    'success': False,
                    'error': 'Échec du chargement des données'
                }
            
            # 4. Entraînement automatique des modèles
            logger.info("Étape 4: Entraînement des modèles...")
            training_results = self._train_all_models()
            
            logger.info("Pipeline ETL terminé avec succès!")
            
            return {
                'success': True,
                'etl_stats': {
                    'raw_records': sum(len(data) for data in raw_data.values()),
                    'transformed_records': len(transformed_data),
                    'days_covered': days_back
                },
                'training_results': training_results,
                'message': 'Pipeline ETL et entraînement terminés avec succès'
            }
            
        except Exception as e:
            logger.error(f"Erreur dans le pipeline ETL: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _train_all_models(self) -> Dict:
        """
        Entraîne tous les modèles avec les données chargées
        """
        try:
            if not hasattr(self, 'training_data') or self.training_data.empty:
                return {
                    'success': False,
                    'error': 'Aucune donnée d\'entraînement disponible'
                }
            
            results = {}
            
            # Entraîner le modèle de demande
            demand_result = self.train_demand_prediction_model(
                self.training_data.to_dict('records'),
                'random_forest'
            )
            results['demand'] = demand_result
            
            # Entraîner le modèle de prix
            price_result = self.train_price_optimization_model(
                self.training_data.to_dict('records'),
                'random_forest'
            )
            results['price'] = price_result
            
            # Entraîner le modèle d'annulation
            cancellation_result = self.train_cancellation_prediction_model(
                self.training_data.to_dict('records'),
                'random_forest'
            )
            results['cancellation'] = cancellation_result
            
            # Sauvegarder les modèles
            self.save_models()
            
            return {
                'success': True,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement des modèles: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_historical_booking_data(self, num_records: int = 1000) -> List[Dict]:
        """
        Génère des données historiques de réservations pour l'entraînement
        """
        historical_data = []
        
        # Période de 2 ans
        start_date = datetime.now() - timedelta(days=730)
        
        for i in range(num_records):
            # Date aléatoire
            random_days = np.random.randint(0, 730)
            booking_date = start_date + timedelta(days=random_days)
            
            # Saison
            month = booking_date.month
            if month in [12, 1, 2]:
                season = 'winter'
                base_demand = 0.6
                base_price = 80
            elif month in [3, 4, 5]:
                season = 'spring'
                base_demand = 0.8
                base_price = 90
            elif month in [6, 7, 8]:
                season = 'summer'
                base_demand = 1.2
                base_price = 100
            else:
                season = 'autumn'
                base_demand = 0.9
                base_price = 95
            
            # Conditions météo simulées
            wave_height = np.random.uniform(0.5, 4.0)
            wind_speed = np.random.uniform(5, 35)
            water_temp = np.random.uniform(15, 28)
            
            # Score météo (0-10)
            weather_score = self._calculate_weather_score(wave_height, wind_speed, water_temp)
            
            # Facteurs de demande
            weekend_factor = 1.3 if booking_date.weekday() >= 5 else 1.0
            holiday_factor = 1.2 if month in [7, 8, 12] else 1.0
            weather_factor = 1.0 + (weather_score - 5) * 0.1
            
            # Demande prédite
            predicted_demand = base_demand * weekend_factor * holiday_factor * weather_factor
            actual_bookings = int(np.random.poisson(predicted_demand * 10))
            
            # Prix optimisé
            demand_factor = min(2.0, max(0.5, predicted_demand))
            price_multiplier = 1.0 + (demand_factor - 1.0) * 0.3
            optimized_price = base_price * price_multiplier
            
            # Probabilité d'annulation
            cancellation_prob = 0.1 + (1 - weather_score / 10) * 0.2
            was_cancelled = np.random.random() < cancellation_prob
            
            # Données de réservation
            booking_data = {
                'id': i + 1,
                'booking_date': booking_date.isoformat(),
                'month': month,
                'season': season,
                'day_of_week': booking_date.weekday(),
                'is_weekend': 1 if booking_date.weekday() >= 5 else 0,
                'is_holiday': 1 if month in [7, 8, 12] else 0,
                
                # Conditions météo
                'wave_height': round(wave_height, 1),
                'wind_speed': round(wind_speed, 1),
                'water_temp': round(water_temp, 1),
                'weather_score': round(weather_score, 1),
                
                # Facteurs de demande
                'weekend_factor': round(weekend_factor, 2),
                'holiday_factor': round(holiday_factor, 2),
                'weather_factor': round(weather_factor, 2),
                
                # Résultats
                'predicted_demand': round(predicted_demand, 2),
                'actual_bookings': actual_bookings,
                'base_price': base_price,
                'optimized_price': round(optimized_price, 2),
                'price_multiplier': round(price_multiplier, 2),
                'cancellation_probability': round(cancellation_prob, 3),
                'was_cancelled': 1 if was_cancelled else 0,
                
                # Spots
                'spot_name': np.random.choice(['Taghazout', 'Essaouira', 'Agadir', 'Bouznika']),
                'surf_level': np.random.choice(['beginner', 'intermediate', 'advanced'])
            }
            
            historical_data.append(booking_data)
        
        return historical_data
    
    def _calculate_weather_score(self, wave_height: float, wind_speed: float, water_temp: float) -> float:
        """
        Calcule un score météo de 0 à 10
        """
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
    
    def train_demand_prediction_model(self, historical_data: List[Dict], model_type: str = 'random_forest') -> Dict:
        """
        Entraîne le modèle de prédiction de la demande
        """
        try:
            # Préparer les données
            df = pd.DataFrame(historical_data)
            
            # Features pour la prédiction de demande (ordre exact)
            feature_columns = self._get_standard_features()
            
            # Vérifier que toutes les features sont présentes
            missing_features = [col for col in feature_columns if col not in df.columns]
            if missing_features:
                logger.warning(f"Features manquantes: {missing_features}")
                # Ajouter des valeurs par défaut
                for col in missing_features:
                    if col == 'season':
                        df[col] = 'summer'
                    elif col in ['is_weekend', 'is_holiday']:
                        df[col] = 0
                    else:
                        df[col] = 1.0
            
            X = df[feature_columns]
            y = df['actual_bookings']
            
            # Encoder les variables catégorielles
            X_encoded = self._encode_features(X)
            
            # Diviser en train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42
            )
            
            # Standardiser
            X_train_scaled = self.demand_scaler.fit_transform(X_train)
            X_test_scaled = self.demand_scaler.transform(X_test)
            
            # Sélectionner et entraîner le modèle
            if model_type not in self.models['demand']:
                raise ValueError(f"Type de modèle non supporté: {model_type}")
            
            self.demand_model = self.models['demand'][model_type]
            self.demand_model.fit(X_train_scaled, y_train)
            
            # Évaluer
            y_pred = self.demand_model.predict(X_test_scaled)
            
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred),
                'model_type': model_type
            }
            
            logger.info(f"Modèle de demande entraîné. R²: {metrics['r2']:.3f}")
            
            return {
                'success': True,
                'metrics': metrics,
                'message': f"Modèle de demande {model_type} entraîné avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement du modèle de demande: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def train_price_optimization_model(self, historical_data: List[Dict], model_type: str = 'random_forest') -> Dict:
        """
        Entraîne le modèle d'optimisation des prix
        """
        try:
            df = pd.DataFrame(historical_data)
            
            # Features pour l'optimisation des prix
            feature_columns = [
                'month', 'season', 'day_of_week', 'is_weekend', 'is_holiday',
                'wave_height', 'wind_speed', 'water_temp', 'weather_score',
                'predicted_demand', 'weekend_factor', 'holiday_factor', 'weather_factor'
            ]
            
            X = df[feature_columns]
            y = df['optimized_price']
            
            # Encoder
            X_encoded = self._encode_features(X)
            
            # Diviser
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42
            )
            
            # Standardiser
            X_train_scaled = self.price_scaler.fit_transform(X_train)
            X_test_scaled = self.price_scaler.transform(X_test)
            
            # Entraîner
            if model_type not in self.models['price']:
                raise ValueError(f"Type de modèle non supporté: {model_type}")
            
            self.price_optimization_model = self.models['price'][model_type]
            self.price_optimization_model.fit(X_train_scaled, y_train)
            
            # Évaluer
            y_pred = self.price_optimization_model.predict(X_test_scaled)
            
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred),
                'model_type': model_type
            }
            
            logger.info(f"Modèle d'optimisation des prix entraîné. R²: {metrics['r2']:.3f}")
            
            return {
                'success': True,
                'metrics': metrics,
                'message': f"Modèle d'optimisation des prix {model_type} entraîné avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement du modèle de prix: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def train_cancellation_prediction_model(self, historical_data: List[Dict], model_type: str = 'random_forest') -> Dict:
        """
        Entraîne le modèle de prédiction d'annulation
        """
        try:
            df = pd.DataFrame(historical_data)
            
            # Features pour la prédiction d'annulation
            feature_columns = [
                'month', 'season', 'day_of_week', 'is_weekend', 'is_holiday',
                'wave_height', 'wind_speed', 'water_temp', 'weather_score',
                'predicted_demand', 'price_multiplier'
            ]
            
            X = df[feature_columns]
            y = df['was_cancelled']
            
            # S'assurer que y est binaire (0 ou 1)
            y = y.astype(int)
            
            # Vérifier qu'il y a au moins 2 classes
            if y.nunique() < 2:
                logger.warning("Pas assez de classes pour la classification, ajout de données simulées")
                # Ajouter quelques annulations simulées
                y.iloc[:len(y)//10] = 1  # 10% d'annulations
            
            # Encoder
            X_encoded = self._encode_features(X)
            
            # Diviser
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42
            )
            
            # Standardiser
            X_train_scaled = self.cancellation_scaler.fit_transform(X_train)
            X_test_scaled = self.cancellation_scaler.transform(X_test)
            
            # Entraîner
            if model_type not in self.models['cancellation']:
                raise ValueError(f"Type de modèle non supporté: {model_type}")
            
            self.cancellation_model = self.models['cancellation'][model_type]
            self.cancellation_model.fit(X_train_scaled, y_train)
            
            # Évaluer
            y_pred = self.cancellation_model.predict(X_test_scaled)
            
            # Métriques de classification
            metrics = {
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'model_type': model_type
            }
            
            logger.info(f"Modèle de prédiction d'annulation entraîné")
            
            return {
                'success': True,
                'metrics': metrics,
                'message': f"Modèle de prédiction d'annulation {model_type} entraîné avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement du modèle d'annulation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _encode_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Encode les variables catégorielles
        """
        X_encoded = X.copy()
        
        for column in X_encoded.columns:
            if X_encoded[column].dtype == 'object':
                if column not in self.label_encoders:
                    self.label_encoders[column] = LabelEncoder()
                    X_encoded[column] = self.label_encoders[column].fit_transform(X_encoded[column])
                else:
                    try:
                        X_encoded[column] = self.label_encoders[column].transform(X_encoded[column])
                    except ValueError:
                        X_encoded[column] = -1
        
        return X_encoded
    
    def predict_demand(self, future_date: datetime, weather_forecast: Dict, spot_name: str = 'Taghazout') -> Dict:
        """
        Prédit la demande pour une date future
        """
        if self.demand_model is None:
            return {
                'success': False,
                'error': 'Modèle de demande non entraîné'
            }
        
        try:
            # Préparer les features
            features = self._prepare_prediction_features(future_date, weather_forecast, spot_name)
            
            # S'assurer que les features sont dans le bon ordre
            standard_features = self._get_standard_features()
            features_ordered = {col: features.get(col, 0) for col in standard_features}
            
            # Encoder
            features_encoded = self._encode_features(pd.DataFrame([features_ordered]))
            
            # Standardiser
            features_scaled = self.demand_scaler.transform(features_encoded.values)
            
            # Prédiction
            predicted_demand = self.demand_model.predict(features_scaled)[0]
            
            # Interprétation
            demand_level = self._interpret_demand_level(predicted_demand)
            
            return {
                'success': True,
                'predicted_demand': round(predicted_demand, 2),
                'demand_level': demand_level,
                'date': future_date.isoformat(),
                'spot': spot_name,
                'weather_conditions': weather_forecast
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction de demande: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def optimize_price(self, future_date: datetime, weather_forecast: Dict, base_price: float = 100) -> Dict:
        """
        Optimise le prix pour une date future
        """
        if self.price_optimization_model is None:
            return {
                'success': False,
                'error': 'Modèle d\'optimisation des prix non entraîné'
            }
        
        try:
            # Prédire la demande
            demand_prediction = self.predict_demand(future_date, weather_forecast)
            
            if not demand_prediction['success']:
                return demand_prediction
            
            # Préparer les features
            features = self._prepare_prediction_features(future_date, weather_forecast)
            features['predicted_demand'] = demand_prediction['predicted_demand']
            
            # Encoder
            features_encoded = self._encode_features(pd.DataFrame([features]))
            
            # Standardiser
            features_scaled = self.price_scaler.transform(features_encoded.values)
            
            # Prédiction du prix optimisé
            optimized_price = self.price_optimization_model.predict(features_scaled)[0]
            
            # Calculer le multiplicateur
            price_multiplier = optimized_price / base_price
            
            # Recommandations de prix
            price_recommendations = self._generate_price_recommendations(
                optimized_price, base_price, demand_prediction['predicted_demand']
            )
            
            return {
                'success': True,
                'base_price': base_price,
                'optimized_price': round(optimized_price, 2),
                'price_multiplier': round(price_multiplier, 2),
                'demand_prediction': demand_prediction,
                'price_recommendations': price_recommendations,
                'date': future_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation des prix: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_cancellation_probability(self, booking_data: Dict) -> Dict:
        """
        Prédit la probabilité d'annulation d'une réservation
        """
        if self.cancellation_model is None:
            return {
                'success': False,
                'error': 'Modèle de prédiction d\'annulation non entraîné'
            }
        
        try:
            # Préparer les features
            features = self._prepare_cancellation_features(booking_data)
            
            # Encoder
            features_encoded = self._encode_features(pd.DataFrame([features]))
            
            # Standardiser
            features_scaled = self.cancellation_scaler.transform(features_encoded.values)
            
            # Prédiction
            if hasattr(self.cancellation_model, 'predict_proba'):
                cancellation_prob = self.cancellation_model.predict_proba(features_scaled)[0][1]
            else:
                # Pour les modèles qui n'ont pas predict_proba
                prediction = self.cancellation_model.predict(features_scaled)[0]
                cancellation_prob = float(prediction)
            
            # Interprétation
            risk_level = self._interpret_cancellation_risk(cancellation_prob)
            
            return {
                'success': True,
                'cancellation_probability': round(cancellation_prob, 3),
                'risk_level': risk_level,
                'recommendations': self._generate_cancellation_recommendations(cancellation_prob)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction d'annulation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_prediction_features(self, date: datetime, weather_forecast: Dict, spot_name: str = 'Taghazout') -> Dict:
        """
        Prépare les features pour la prédiction
        """
        month = date.month
        day_of_week = date.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Saison
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'autumn'
        
        # Facteurs
        weekend_factor = 1.3 if is_weekend else 1.0
        holiday_factor = 1.2 if month in [7, 8, 12] else 1.0
        
        # Score météo
        weather_score = self._calculate_weather_score(
            weather_forecast.get('wave_height', 1.5),
            weather_forecast.get('wind_speed', 15),
            weather_forecast.get('water_temp', 22)
        )
        
        weather_factor = 1.0 + (weather_score - 5) * 0.1
        
        # Retourner les features dans l'ordre exact utilisé pour l'entraînement
        return {
            'month': month,
            'season': season,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'is_holiday': 1 if month in [7, 8, 12] else 0,
            'wave_height': weather_forecast.get('wave_height', 1.5),
            'wind_speed': weather_forecast.get('wind_speed', 15),
            'water_temp': weather_forecast.get('water_temp', 22),
            'weather_score': weather_score,
            'weekend_factor': weekend_factor,
            'holiday_factor': holiday_factor,
            'weather_factor': weather_factor
        }

    def _get_standard_features(self) -> List[str]:
        """
        Retourne la liste standard des features utilisées pour l'entraînement
        """
        return [
            'month', 'season', 'day_of_week', 'is_weekend', 'is_holiday',
            'wave_height', 'wind_speed', 'water_temp', 'weather_score',
            'weekend_factor', 'holiday_factor', 'weather_factor'
        ]
    
    def _prepare_cancellation_features(self, booking_data: Dict) -> Dict:
        """
        Prépare les features pour la prédiction d'annulation
        """
        # Convertir la date de réservation
        booking_date = datetime.fromisoformat(booking_data['booking_date'])
        
        return {
            'month': booking_date.month,
            'season': 'winter' if booking_date.month in [12, 1, 2] else 'spring' if booking_date.month in [3, 4, 5] else 'summer' if booking_date.month in [6, 7, 8] else 'autumn',
            'day_of_week': booking_date.weekday(),
            'is_weekend': 1 if booking_date.weekday() >= 5 else 0,
            'is_holiday': 1 if booking_date.month in [7, 8, 12] else 0,
            'wave_height': booking_data.get('wave_height', 1.5),
            'wind_speed': booking_data.get('wind_speed', 15),
            'water_temp': booking_data.get('water_temp', 22),
            'weather_score': self._calculate_weather_score(
                booking_data.get('wave_height', 1.5),
                booking_data.get('wind_speed', 15),
                booking_data.get('water_temp', 22)
            ),
            'predicted_demand': booking_data.get('predicted_demand', 1.0),
            'price_multiplier': booking_data.get('price_multiplier', 1.0)
        }
    
    def _interpret_demand_level(self, demand: float) -> str:
        """
        Interprète le niveau de demande
        """
        if demand >= 1.5:
            return "Très élevée"
        elif demand >= 1.2:
            return "Élevée"
        elif demand >= 0.8:
            return "Normale"
        elif demand >= 0.5:
            return "Faible"
        else:
            return "Très faible"
    
    def _interpret_cancellation_risk(self, probability: float) -> str:
        """
        Interprète le niveau de risque d'annulation
        """
        if probability >= 0.3:
            return "Élevé"
        elif probability >= 0.15:
            return "Modéré"
        else:
            return "Faible"
    
    def _generate_price_recommendations(self, optimized_price: float, base_price: float, demand: float) -> List[str]:
        """
        Génère des recommandations de prix
        """
        recommendations = []
        
        if optimized_price > base_price * 1.2:
            recommendations.append("Prix élevé recommandé - forte demande attendue")
        elif optimized_price < base_price * 0.8:
            recommendations.append("Prix réduit recommandé - faible demande attendue")
        else:
            recommendations.append("Prix standard recommandé - demande normale")
        
        if demand > 1.3:
            recommendations.append("Considérer une augmentation progressive des prix")
        elif demand < 0.7:
            recommendations.append("Offres spéciales recommandées pour stimuler la demande")
        
        return recommendations
    
    def _generate_cancellation_recommendations(self, probability: float) -> List[str]:
        """
        Génère des recommandations pour réduire les annulations
        """
        recommendations = []
        
        if probability >= 0.3:
            recommendations.extend([
                "Politique de remboursement flexible",
                "Communication proactive sur les conditions météo",
                "Offres de report gratuites"
            ])
        elif probability >= 0.15:
            recommendations.extend([
                "Confirmation 24h avant la session",
                "Mise à jour des conditions en temps réel"
            ])
        else:
            recommendations.append("Politique standard suffisante")
        
        return recommendations
    
    def save_models(self):
        """
        Sauvegarde tous les modèles entraînés
        """
        try:
            models_data = {
                'demand_model': self.demand_model,
                'price_model': self.price_optimization_model,
                'cancellation_model': self.cancellation_model,
                'demand_scaler': self.demand_scaler,
                'price_scaler': self.price_scaler,
                'cancellation_scaler': self.cancellation_scaler,
                'label_encoders': self.label_encoders
            }
            
            joblib.dump(models_data, 'booking_prediction_models.pkl')
            logger.info("Modèles de prédiction sauvegardés")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
    
    def load_models(self):
        """
        Charge les modèles sauvegardés
        """
        try:
            if os.path.exists('booking_prediction_models.pkl'):
                models_data = joblib.load('booking_prediction_models.pkl')
                
                self.demand_model = models_data.get('demand_model')
                self.price_optimization_model = models_data.get('price_model')
                self.cancellation_model = models_data.get('cancellation_model')
                self.demand_scaler = models_data.get('demand_scaler', StandardScaler())
                self.price_scaler = models_data.get('price_scaler', StandardScaler())
                self.cancellation_scaler = models_data.get('cancellation_scaler', StandardScaler())
                self.label_encoders = models_data.get('label_encoders', {})
                
                self.is_trained = True
                logger.info("Modèles de prédiction chargés")
                
        except Exception as e:
            logger.warning(f"Impossible de charger les modèles: {e}")
            self.is_trained = False
    
    def get_system_status(self) -> Dict:
        """
        Retourne le statut du système
        """
        return {
            'demand_model_trained': self.demand_model is not None,
            'price_model_trained': self.price_optimization_model is not None,
            'cancellation_model_trained': self.cancellation_model is not None,
            'is_fully_trained': self.is_trained
        }

# Instance globale du système de prédiction
booking_prediction_system = BookingPredictionSystem()

# ==================== FONCTIONS DE TEST ET DÉMONSTRATION ====================

def test_etl_pipeline():
    """
    Teste le pipeline ETL complet
    """
    try:
        print("🚀 Test du pipeline ETL de prédiction des réservations...")
        
        # Créer une instance du système
        system = BookingPredictionSystem()
        
        # Exécuter le pipeline ETL complet
        result = system.run_full_etl_pipeline(days_back=365)  # 1 an de données
        
        if result['success']:
            print("✅ Pipeline ETL terminé avec succès!")
            print(f"📊 Statistiques: {result['etl_stats']}")
            print(f"🤖 Résultats d'entraînement: {result['training_results']}")
            
            # Tester les prédictions
            test_predictions(system)
            
        else:
            print(f"❌ Erreur dans le pipeline ETL: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def test_predictions(system: BookingPredictionSystem):
    """
    Teste les prédictions du système
    """
    try:
        print("\n🔮 Test des prédictions...")
        
        # Date future pour tester
        future_date = datetime.now() + timedelta(days=7)
        
        # Données météo simulées
        weather_forecast = {
            'wave_height': 2.5,
            'wind_speed': 12,
            'water_temp': 24
        }
        
        # Prédire la demande
        demand_prediction = system.predict_demand(future_date, weather_forecast, 'Taghazout')
        if demand_prediction['success']:
            print(f"📈 Prédiction de demande: {demand_prediction['predicted_demand']} ({demand_prediction['demand_level']})")
        
        # Optimiser le prix
        price_optimization = system.optimize_price(future_date, weather_forecast, 100)
        if price_optimization['success']:
            print(f"💰 Prix optimisé: {price_optimization['optimized_price']}€ (multiplicateur: {price_optimization['price_multiplier']})")
        
        # Prédire l'annulation
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
            print(f"⚠️  Risque d'annulation: {cancellation_prediction['cancellation_probability']} ({cancellation_prediction['risk_level']})")
        
        print("✅ Tests de prédiction terminés!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de prédiction: {e}")

def demo_etl_with_mock_data():
    """
    Démonstration du pipeline ETL avec des données simulées
    """
    try:
        print("🎭 Démonstration ETL avec données simulées...")
        
        # Créer une instance
        system = BookingPredictionSystem()
        
        # Générer des données historiques simulées
        historical_data = system.generate_historical_booking_data(1000)
        
        # Simuler le pipeline ETL
        print("📥 Chargement des données simulées...")
        system.load_transformed_data(historical_data)
        
        # Entraîner les modèles
        print("🧠 Entraînement des modèles...")
        training_results = system._train_all_models()
        
        if training_results['success']:
            print("✅ Modèles entraînés avec succès!")
            
            # Tester les prédictions
            test_predictions(system)
            
            # Sauvegarder les modèles
            system.save_models()
            print("💾 Modèles sauvegardés!")
        else:
            print(f"❌ Erreur d'entraînement: {training_results['error']}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")

if __name__ == "__main__":
    # Test du pipeline ETL complet
    test_etl_pipeline()
    
    # Si pas de données réelles, utiliser la démonstration
    print("\n" + "="*50)
    demo_etl_with_mock_data()
