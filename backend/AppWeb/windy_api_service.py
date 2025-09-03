# windy_api_service.py
"""
Service d'intégration avec l'API Windy pour les prévisions météo du surf
Windy est une excellente source de données météo pour les surfeurs
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class WindyAPIService:
    """Service pour l'API Windy - Prévisions météo pour le surf"""
    
    def __init__(self):
        # Clé API Windy (gratuite avec limitations)
        self.api_key = getattr(settings, 'WINDY_API_KEY', None)
        self.base_url = "https://api.windy.com/api"
        
        # Mode développement (utilise le service de test si pas de clé API)
        self.dev_mode = not self.api_key or self.api_key == 'test_key_for_development'
        
        # Endpoints disponibles
        self.endpoints = {
            'forecast': '/forecast',
            'point': '/point-forecast',
            'webcams': '/webcams',
            'stations': '/stations'
        }
        
        # Paramètres par défaut pour le surf
        self.surf_params = {
            'wind': True,      # Vitesse et direction du vent
            'waves': True,     # Hauteur et direction des vagues
            'tide': True,      # Marées
            'temp': True,      # Température de l'eau
            'pressure': True,  # Pression atmosphérique
            'precipitation': True  # Précipitations
        }
    
    def get_surf_forecast(self, lat: float, lon: float, days: int = 7) -> Dict:
        """
        Récupère les prévisions météo pour le surf à un endroit donné
        """
        # En mode développement, utiliser le service de test
        if self.dev_mode:
            try:
                from .windy_mock_service import windy_mock_service
                return windy_mock_service.get_surf_forecast(lat, lon, days)
            except ImportError:
                logger.warning("Service de test Windy non disponible, utilisation du fallback")
                return self._get_fallback_forecast(lat, lon, days)
        
        # Mode production avec vraie API
        try:
            # Paramètres de la requête
            params = {
                'lat': lat,
                'lon': lon,
                'model': 'gfs',  # Modèle GFS (Global Forecast System)
                'parameters': ','.join([k for k, v in self.surf_params.items() if v]),
                'levels': 'surface,850hPa',  # Niveaux atmosphériques
                'key': self.api_key
            }
            
            # Appel API
            response = requests.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._process_surf_data(data, days)
            else:
                logger.error(f"Erreur API Windy: {response.status_code}")
                return self._get_fallback_forecast(lat, lon, days)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'appel API Windy: {e}")
            return self._get_fallback_forecast(lat, lon, days)
    
    def get_spot_forecast(self, spot_name: str, days: int = 7) -> Dict:
        """
        Récupère les prévisions pour un spot de surf spécifique
        """
        # En mode développement, utiliser le service de test
        if self.dev_mode:
            try:
                from .windy_mock_service import windy_mock_service
                return windy_mock_service.get_spot_forecast(spot_name, days)
            except ImportError:
                logger.warning("Service de test Windy non disponible, utilisation du fallback")
                return self._search_spot_by_name(spot_name, days)
        
        # Mode production
        spots = self._get_morocco_spots()
        spot_key = spot_name.lower().replace(' ', '_')
        if spot_key in spots:
            spot = spots[spot_key]
            return self.get_surf_forecast(spot['lat'], spot['lon'], days)
        else:
            return self._search_spot_by_name(spot_name, days)
    
    def get_optimal_surf_times(self, lat: float, lon: float, days: int = 3) -> Dict:
        """
        Détermine les meilleurs moments pour surfer
        """
        # En mode développement, utiliser le service de test
        if self.dev_mode:
            try:
                from .windy_mock_service import windy_mock_service
                return windy_mock_service.get_optimal_surf_times(lat, lon, days)
            except ImportError:
                logger.warning("Service de test Windy non disponible, utilisation du fallback")
                return {'success': False, 'error': 'Service de test non disponible'}
        
        # Mode production
        forecast = self.get_surf_forecast(lat, lon, days)
        
        if not forecast.get('success'):
            return {'success': False, 'error': 'Impossible de récupérer les prévisions'}
        
        optimal_times = []
        
        for day_data in forecast.get('daily', []):
            day_optimal = self._analyze_day_for_surf(day_data)
            if day_optimal['score'] > 7:  # Score minimum pour être considéré comme optimal
                optimal_times.append(day_optimal)
        
        # Trier par score décroissant
        optimal_times.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'success': True,
            'optimal_times': optimal_times,
            'spot_info': {
                'lat': lat,
                'lon': lon,
                'analysis_days': days
            }
        }
    
    def get_surf_conditions_summary(self, spot_name: str) -> str:
        """
        Génère un résumé des conditions de surf en langage naturel
        """
        # En mode développement, utiliser le service de test
        if self.dev_mode:
            try:
                from .windy_mock_service import windy_mock_service
                return windy_mock_service.get_surf_conditions_summary(spot_name)
            except ImportError:
                logger.warning("Service de test Windy non disponible, utilisation du fallback")
                return f"Désolé, je ne peux pas récupérer les prévisions pour {spot_name} actuellement."
        
        # Mode production
        forecast = self.get_spot_forecast(spot_name, 3)
        
        if not forecast.get('success'):
            return f"Désolé, je ne peux pas récupérer les prévisions pour {spot_name} actuellement."
        
        # Analyser les conditions
        conditions = forecast.get('current_conditions', {})
        
        if not conditions:
            return f"Pas de données disponibles pour {spot_name}."
        
        # Générer le résumé
        summary = f"🌊 Conditions actuelles à {spot_name}:\n\n"
        
        # Vagues
        if 'wave_height' in conditions:
            wave_height = conditions['wave_height']
            if wave_height < 0.5:
                summary += "📏 Vagues: Très petites (< 0.5m) - Pas idéal pour le surf\n"
            elif wave_height < 1:
                summary += "📏 Vagues: Petites (0.5-1m) - Bon pour débuter\n"
            elif wave_height < 2:
                summary += "📏 Vagues: Moyennes (1-2m) - Parfait pour tous niveaux\n"
            elif wave_height < 3:
                summary += "📏 Vagues: Grandes (2-3m) - Pour surfeurs expérimentés\n"
            else:
                summary += "📏 Vagues: Très grandes (>3m) - Experts uniquement\n"
        
        # Vent
        if 'wind_speed' in conditions:
            wind_speed = conditions['wind_speed']
            if wind_speed < 10:
                summary += "💨 Vent: Léger (< 10 km/h) - Conditions optimales\n"
            elif wind_speed < 20:
                summary += "💨 Vent: Modéré (10-20 km/h) - Bonnes conditions\n"
            elif wind_speed < 30:
                summary += "💨 Vent: Fort (20-30 km/h) - Conditions difficiles\n"
            else:
                summary += "💨 Vent: Très fort (>30 km/h) - Pas recommandé\n"
        
        # Température
        if 'water_temp' in conditions:
            water_temp = conditions['water_temp']
            summary += f"🌡️ Température eau: {water_temp}°C\n"
        
        # Recommandation générale
        score = self._calculate_surf_score(conditions)
        if score > 8:
            summary += "\n🏄‍♂️ Recommandation: Conditions EXCELLENTES pour le surf !"
        elif score > 6:
            summary += "\n🏄‍♂️ Recommandation: Bonnes conditions pour surfer"
        elif score > 4:
            summary += "\n🏄‍♂️ Recommandation: Conditions moyennes, surfez avec précaution"
        else:
            summary += "\n🏄‍♂️ Recommandation: Conditions difficiles, attendez un meilleur moment"
        
        return summary
    
    def _get_morocco_spots(self) -> Dict:
        """Retourne les coordonnées des spots populaires au Maroc"""
        return {
            'taghazout': {'lat': 30.5451, 'lon': -9.7101, 'name': 'Taghazout'},
            'agadir': {'lat': 30.4278, 'lon': -9.5981, 'name': 'Agadir'},
            'essaouira': {'lat': 31.5085, 'lon': -9.7595, 'name': 'Essaouira'},
            'bouznika': {'lat': 33.7895, 'lon': -7.1599, 'name': 'Bouznika'},
            'anchor_point': {'lat': 30.5451, 'lon': -9.7101, 'name': 'Anchor Point'},
            'boilers': {'lat': 30.5451, 'lon': -9.7101, 'name': 'Boilers'},
            'killers': {'lat': 30.5451, 'lon': -9.7101, 'name': 'Killers'},
            'panoramas': {'lat': 30.5451, 'lon': -9.7101, 'name': 'Panoramas'}
        }
    
    def _process_surf_data(self, data: Dict, days: int) -> Dict:
        """Traite les données brutes de l'API Windy pour le surf"""
        try:
            processed_data = {
                'success': True,
                'spot_info': {
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'name': data.get('name', 'Spot inconnu')
                },
                'forecast_period': f"{days} jours",
                'generated_at': datetime.now().isoformat(),
                'daily': [],
                'current_conditions': {}
            }
            
            # Traiter les données horaires
            if 'hourly' in data:
                hourly_data = data['hourly']
                current_hour = datetime.now().hour
                
                # Conditions actuelles (heure la plus proche)
                if str(current_hour) in hourly_data:
                    current = hourly_data[str(current_hour)]
                    processed_data['current_conditions'] = {
                        'wave_height': current.get('wave_height', 0),
                        'wind_speed': current.get('wind_speed', 0),
                        'wind_direction': current.get('wind_direction', 0),
                        'water_temp': current.get('water_temp', 0),
                        'tide': current.get('tide', 0)
                    }
                
                # Agréger par jour
                daily_aggregated = {}
                for hour, hour_data in hourly_data.items():
                    date = datetime.now().date()
                    if int(hour) < current_hour:
                        date += timedelta(days=1)
                    
                    date_str = date.strftime('%Y-%m-%d')
                    if date_str not in daily_aggregated:
                        daily_aggregated[date_str] = {
                            'date': date_str,
                            'hours': [],
                            'avg_wave_height': 0,
                            'avg_wind_speed': 0,
                            'best_hours': []
                        }
                    
                    daily_aggregated[date_str]['hours'].append({
                        'hour': hour,
                        'wave_height': hour_data.get('wave_height', 0),
                        'wind_speed': hour_data.get('wind_speed', 0),
                        'wind_direction': hour_data.get('wind_direction', 0),
                        'water_temp': hour_data.get('water_temp', 0)
                    })
                
                # Calculer les moyennes et meilleurs moments
                for day_data in daily_aggregated.values():
                    wave_heights = [h['wave_height'] for h in day_data['hours']]
                    wind_speeds = [h['wind_speed'] for h in day_data['hours']]
                    
                    day_data['avg_wave_height'] = sum(wave_heights) / len(wave_heights)
                    day_data['avg_wind_speed'] = sum(wind_speeds) / len(wind_speeds)
                    
                    # Trouver les meilleures heures (vagues + vent faible)
                    best_hours = []
                    for hour_data in day_data['hours']:
                        score = self._calculate_hour_score(hour_data)
                        if score > 7:
                            best_hours.append({
                                'hour': hour_data['hour'],
                                'score': score,
                                'wave_height': hour_data['wave_height'],
                                'wind_speed': hour_data['wind_speed']
                            })
                    
                    day_data['best_hours'] = sorted(best_hours, key=lambda x: x['score'], reverse=True)[:3]
                
                processed_data['daily'] = list(daily_aggregated.values())[:days]
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_day_for_surf(self, day_data: Dict) -> Dict:
        """Analyse une journée pour déterminer si elle est bonne pour le surf"""
        avg_wave_height = day_data.get('avg_wave_height', 0)
        avg_wind_speed = day_data.get('avg_wind_speed', 0)
        best_hours = day_data.get('best_hours', [])
        
        # Calculer un score de surf
        wave_score = min(10, avg_wave_height * 3)  # Vagues optimales entre 1-3m
        wind_score = max(0, 10 - avg_wind_speed / 2)  # Vent faible = meilleur score
        hour_score = len(best_hours) * 2  # Plus d'heures optimales = meilleur score
        
        total_score = (wave_score + wind_score + hour_score) / 3
        
        return {
            'date': day_data.get('date'),
            'score': round(total_score, 1),
            'wave_height': round(avg_wave_height, 1),
            'wind_speed': round(avg_wind_speed, 1),
            'best_hours': best_hours,
            'recommendation': self._get_surf_recommendation(total_score)
        }
    
    def _calculate_surf_score(self, conditions: Dict) -> float:
        """Calcule un score de surf basé sur les conditions actuelles"""
        wave_height = conditions.get('wave_height', 0)
        wind_speed = conditions.get('wind_speed', 0)
        
        # Score pour les vagues (optimal entre 1-3m)
        if 1 <= wave_height <= 3:
            wave_score = 10
        elif 0.5 <= wave_height < 1:
            wave_score = 7
        elif 3 < wave_height <= 4:
            wave_score = 6
        else:
            wave_score = 3
        
        # Score pour le vent (optimal < 15 km/h)
        if wind_speed < 10:
            wind_score = 10
        elif wind_speed < 15:
            wind_score = 8
        elif wind_speed < 20:
            wind_score = 5
        else:
            wind_score = 2
        
        return (wave_score + wind_score) / 2
    
    def _calculate_hour_score(self, hour_data: Dict) -> float:
        """Calcule un score pour une heure spécifique"""
        wave_height = hour_data.get('wave_height', 0)
        wind_speed = hour_data.get('wind_speed', 0)
        
        # Score vagues
        if 1 <= wave_height <= 3:
            wave_score = 10
        elif 0.5 <= wave_height < 1:
            wave_score = 7
        else:
            wave_score = 4
        
        # Score vent
        if wind_speed < 10:
            wind_score = 10
        elif wind_speed < 15:
            wind_score = 8
        else:
            wind_score = 4
        
        return (wave_score + wind_score) / 2
    
    def _get_surf_recommendation(self, score: float) -> str:
        """Génère une recommandation basée sur le score"""
        if score >= 8:
            return "Excellent pour le surf !"
        elif score >= 6:
            return "Bonnes conditions"
        elif score >= 4:
            return "Conditions moyennes"
        else:
            return "Conditions difficiles"
    
    def _get_fallback_forecast(self, lat: float, lon: float, days: int) -> Dict:
        """Prévisions de secours si l'API Windy échoue"""
        return {
            'success': False,
            'error': 'API Windy temporairement indisponible',
            'fallback_data': {
                'spot_info': {'lat': lat, 'lon': lon},
                'message': 'Utilisez les données météo locales ou consultez windsurf.com'
            }
        }
    
    def _search_spot_by_name(self, spot_name: str, days: int) -> Dict:
        """Recherche approximative d'un spot par nom"""
        # Coordonnées approximatives du Maroc
        morocco_center = {'lat': 31.7917, 'lon': -7.0926}
        
        return {
            'success': False,
            'error': f'Spot "{spot_name}" non trouvé',
            'suggestion': 'Essayez avec un nom de spot connu (ex: Taghazout, Essaouira)',
            'approximate_location': morocco_center
        }

# Instance globale du service Windy
windy_service = WindyAPIService()
