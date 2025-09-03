# windy_mock_service.py
"""
Service Windy de test pour le développement
Simule les réponses API Windy sans avoir besoin d'une vraie clé API
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List

class WindyMockService:
    """Service Windy de test pour le développement"""
    
    def __init__(self):
        self.spots_data = {
            'taghazout': {
                'lat': 30.5451, 'lon': -9.7101, 'name': 'Taghazout',
                'avg_wave_height': 1.8, 'avg_wind_speed': 12
            },
            'agadir': {
                'lat': 30.4278, 'lon': -9.5981, 'name': 'Agadir',
                'avg_wave_height': 1.2, 'avg_wind_speed': 15
            },
            'essaouira': {
                'lat': 31.5085, 'lon': -9.7595, 'name': 'Essaouira',
                'avg_wave_height': 2.1, 'avg_wind_speed': 18
            },
            'bouznika': {
                'lat': 33.7895, 'lon': -7.1599, 'name': 'Bouznika',
                'avg_wave_height': 1.5, 'avg_wind_speed': 10
            }
        }
    
    def get_surf_forecast(self, lat: float, lon: str, days: int = 7) -> Dict:
        """Simule les prévisions météo pour le surf"""
        # Trouver le spot le plus proche
        spot_name = self._find_closest_spot(lat, lon)
        spot_data = self.spots_data[spot_name]
        
        # Générer des données de test
        current_conditions = {
            'wave_height': round(random.uniform(0.8, 3.2), 1),
            'wind_speed': round(random.uniform(5, 25), 1),
            'wind_direction': random.randint(0, 360),
            'water_temp': round(random.uniform(18, 24), 1),
            'tide': round(random.uniform(-1, 1), 1)
        }
        
        # Générer des prévisions quotidiennes
        daily_forecast = []
        for i in range(days):
            day_data = {
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'avg_wave_height': round(random.uniform(0.5, 4.0), 1),
                'avg_wind_speed': round(random.uniform(3, 30), 1),
                'best_hours': self._generate_best_hours()
            }
            daily_forecast.append(day_data)
        
        return {
            'success': True,
            'spot_info': {
                'lat': spot_data['lat'],
                'lon': spot_data['lon'],
                'name': spot_data['name']
            },
            'forecast_period': f"{days} jours",
            'generated_at': datetime.now().isoformat(),
            'current_conditions': current_conditions,
            'daily': daily_forecast
        }
    
    def get_spot_forecast(self, spot_name: str, days: int = 7) -> Dict:
        """Simule les prévisions pour un spot spécifique"""
        spot_key = spot_name.lower().replace(' ', '_')
        
        if spot_key in self.spots_data:
            spot_data = self.spots_data[spot_key]
            return self.get_surf_forecast(spot_data['lat'], spot_data['lon'], days)
        else:
            return {
                'success': False,
                'error': f'Spot "{spot_name}" non trouvé',
                'suggestion': 'Essayez avec un nom de spot connu (ex: Taghazout, Essaouira)'
            }
    
    def get_optimal_surf_times(self, lat: float, lon: float, days: int = 3) -> Dict:
        """Simule les meilleurs moments pour surfer"""
        spot_name = self._find_closest_spot(lat, lon)
        spot_data = self.spots_data[spot_name]
        
        optimal_times = []
        for i in range(days):
            # Générer un score de surf réaliste
            wave_height = random.uniform(1.0, 3.5)
            wind_speed = random.uniform(5, 20)
            
            # Score basé sur les conditions
            wave_score = min(10, wave_height * 3)
            wind_score = max(0, 10 - wind_speed / 2)
            total_score = (wave_score + wind_score) / 2
            
            if total_score > 6:  # Seuil pour être considéré comme optimal
                optimal_times.append({
                    'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                    'score': round(total_score, 1),
                    'wave_height': round(wave_height, 1),
                    'wind_speed': round(wind_speed, 1),
                    'best_hours': self._generate_best_hours(),
                    'recommendation': self._get_surf_recommendation(total_score)
                })
        
        # Trier par score décroissant
        optimal_times.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'success': True,
            'optimal_times': optimal_times,
            'spot_info': {
                'lat': lat,
                'lon': lon,
                'name': spot_data['name'],
                'analysis_days': days
            }
        }
    
    def get_surf_conditions_summary(self, spot_name: str) -> str:
        """Génère un résumé des conditions de surf en langage naturel"""
        forecast = self.get_spot_forecast(spot_name, 3)
        
        if not forecast.get('success'):
            return f"Désolé, je ne peux pas récupérer les prévisions pour {spot_name} actuellement."
        
        conditions = forecast.get('current_conditions', {})
        
        if not conditions:
            return f"Pas de données disponibles pour {spot_name}."
        
        # Générer le résumé
        summary = f"🌊 Conditions actuelles à {spot_name}:\n\n"
        
        # Vagues
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
    
    def _find_closest_spot(self, lat: float, lon: float) -> str:
        """Trouve le spot le plus proche des coordonnées données"""
        closest_spot = 'taghazout'
        min_distance = float('inf')
        
        for spot_name, spot_data in self.spots_data.items():
            distance = ((lat - spot_data['lat']) ** 2 + (lon - spot_data['lon']) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_spot = spot_name
        
        return closest_spot
    
    def _generate_best_hours(self) -> List[Dict]:
        """Génère des heures optimales de test"""
        best_hours = []
        for _ in range(random.randint(1, 3)):
            hour_data = {
                'hour': random.randint(6, 18),
                'score': round(random.uniform(7, 10), 1),
                'wave_height': round(random.uniform(1, 3), 1),
                'wind_speed': round(random.uniform(3, 15), 1)
            }
            best_hours.append(hour_data)
        
        # Trier par score décroissant
        best_hours.sort(key=lambda x: x['score'], reverse=True)
        return best_hours[:3]
    
    def _calculate_surf_score(self, conditions: Dict) -> float:
        """Calcule un score de surf basé sur les conditions"""
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

# Instance globale du service Windy de test
windy_mock_service = WindyMockService()
