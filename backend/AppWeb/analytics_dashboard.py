# analytics_dashboard.py
"""
Dashboard analytics avancé pour YalaSurf
Visualisations des données météo, surf et performances IA
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
import json
import io
import base64
from .surf_prediction_model import surf_prediction_model
from .recommendation_system import recommendation_system
from .booking_prediction import booking_prediction_system
from .windy_api_service import windy_service

logger = logging.getLogger(__name__)

class AnalyticsDashboard:
    """
    Dashboard analytics pour visualiser les données et performances IA
    """
    
    def __init__(self):
        self.plt_style = 'seaborn-v0_8'
        self.color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        self.is_initialized = False
        
        # Configuration des graphiques
        plt.style.use(self.plt_style)
        sns.set_palette(self.color_palette)
        
    def initialize_dashboard(self):
        """
        Initialise le dashboard
        """
        try:
            # Vérifier que tous les systèmes sont disponibles
            self._check_systems_status()
            self.is_initialized = True
            logger.info("Dashboard analytics initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du dashboard: {e}")
            self.is_initialized = False
    
    def _check_systems_status(self):
        """
        Vérifie le statut de tous les systèmes IA
        """
        self.systems_status = {
            'surf_prediction': surf_prediction_model.get_model_info(),
            'recommendation': recommendation_system.is_initialized,
            'booking_prediction': booking_prediction_system.get_system_status()
        }
    
    def generate_weather_analytics(self, spot_name: str = 'Taghazout', days: int = 30) -> Dict:
        """
        Génère des analytics sur les conditions météo
        """
        try:
            # Récupérer les données météo
            weather_data = windy_service.get_spot_forecast(spot_name, days)
            
            if not weather_data.get('success'):
                return {'success': False, 'error': 'Impossible de récupérer les données météo'}
            
            # Créer les visualisations
            charts = {}
            
            # Graphique des vagues
            wave_chart = self._create_wave_analysis_chart(weather_data)
            charts['wave_analysis'] = wave_chart
            
            # Graphique du vent
            wind_chart = self._create_wind_analysis_chart(weather_data)
            charts['wind_analysis'] = wind_chart
            
            # Graphique de température
            temp_chart = self._create_temperature_chart(weather_data)
            charts['temperature_analysis'] = temp_chart
            
            # Graphique des scores de surf
            surf_score_chart = self._create_surf_score_chart(weather_data)
            charts['surf_score_analysis'] = surf_score_chart
            
            # Résumé statistique
            summary_stats = self._calculate_weather_summary(weather_data)
            
            return {
                'success': True,
                'spot_name': spot_name,
                'analysis_period': f"{days} jours",
                'charts': charts,
                'summary_stats': summary_stats,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des analytics météo: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_wave_analysis_chart(self, weather_data: Dict) -> str:
        """
        Crée un graphique d'analyse des vagues
        """
        try:
            plt.figure(figsize=(12, 6))
            
            # Extraire les données des vagues
            daily_data = weather_data.get('daily', [])
            dates = [day['date'] for day in daily_data]
            wave_heights = [day.get('avg_wave_height', 0) for day in daily_data]
            
            # Créer le graphique
            plt.plot(dates, wave_heights, marker='o', linewidth=2, markersize=6)
            plt.fill_between(dates, wave_heights, alpha=0.3)
            
            plt.title('Analyse des Vagues - Hauteur Moyenne', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Hauteur des Vagues (m)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Ajouter des lignes de référence
            plt.axhline(y=1, color='green', linestyle='--', alpha=0.7, label='Optimal débutant')
            plt.axhline(y=3, color='orange', linestyle='--', alpha=0.7, label='Optimal expérimenté')
            plt.legend()
            
            # Convertir en base64
            chart_base64 = self._chart_to_base64()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique des vagues: {e}")
            return ""
    
    def _create_wind_analysis_chart(self, weather_data: Dict) -> str:
        """
        Crée un graphique d'analyse du vent
        """
        try:
            plt.figure(figsize=(12, 6))
            
            # Extraire les données du vent
            daily_data = weather_data.get('daily', [])
            dates = [day['date'] for day in daily_data]
            wind_speeds = [day.get('avg_wind_speed', 0) for day in daily_data]
            
            # Créer le graphique
            bars = plt.bar(dates, wind_speeds, alpha=0.7, color='skyblue')
            
            # Colorer selon l'intensité du vent
            for i, speed in enumerate(wind_speeds):
                if speed < 10:
                    bars[i].set_color('green')  # Vent léger - optimal
                elif speed < 20:
                    bars[i].set_color('orange')  # Vent modéré - acceptable
                else:
                    bars[i].set_color('red')  # Vent fort - difficile
            
            plt.title('Analyse du Vent - Vitesse Moyenne', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Vitesse du Vent (km/h)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Ajouter des lignes de référence
            plt.axhline(y=10, color='green', linestyle='--', alpha=0.7, label='Vent léger (optimal)')
            plt.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Vent modéré (acceptable)')
            plt.legend()
            
            # Convertir en base64
            chart_base64 = self._chart_to_base64()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique du vent: {e}")
            return ""
    
    def _create_temperature_chart(self, weather_data: Dict) -> str:
        """
        Crée un graphique de température
        """
        try:
            plt.figure(figsize=(12, 6))
            
            # Extraire les données de température
            daily_data = weather_data.get('daily', [])
            dates = [day['date'] for day in daily_data]
            
            # Simuler les températures (à adapter selon tes données réelles)
            water_temps = [22 + np.random.normal(0, 2) for _ in range(len(dates))]
            
            # Créer le graphique
            plt.plot(dates, water_temps, marker='s', linewidth=2, markersize=6, color='blue')
            
            plt.title('Température de l\'Eau', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Température (°C)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Zone de confort
            plt.axhspan(18, 25, alpha=0.2, color='green', label='Zone de confort (18-25°C)')
            plt.legend()
            
            # Convertir en base64
            chart_base64 = self._chart_to_base64()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique de température: {e}")
            return ""
    
    def _create_surf_score_chart(self, weather_data: Dict) -> str:
        """
        Crée un graphique des scores de surf
        """
        try:
            plt.figure(figsize=(12, 6))
            
            # Calculer les scores de surf pour chaque jour
            daily_data = weather_data.get('daily', [])
            dates = [day['date'] for day in daily_data]
            
            surf_scores = []
            for day in daily_data:
                # Calculer le score basé sur les conditions
                wave_height = day.get('avg_wave_height', 0)
                wind_speed = day.get('avg_wind_speed', 0)
                
                # Score simplifié (0-10)
                wave_score = min(10, wave_height * 3) if wave_height > 0 else 0
                wind_score = max(0, 10 - wind_speed / 2)
                daily_score = (wave_score + wind_score) / 2
                
                surf_scores.append(daily_score)
            
            # Créer le graphique
            bars = plt.bar(dates, surf_scores, alpha=0.7)
            
            # Colorer selon le score
            for i, score in enumerate(surf_scores):
                if score >= 8:
                    bars[i].set_color('green')  # Excellent
                elif score >= 6:
                    bars[i].set_color('lightgreen')  # Bon
                elif score >= 4:
                    bars[i].set_color('orange')  # Moyen
                else:
                    bars[i].set_color('red')  # Difficile
            
            plt.title('Scores de Surf Quotidiens', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Score de Surf (0-10)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Lignes de référence
            plt.axhline(y=8, color='green', linestyle='--', alpha=0.7, label='Excellent (≥8)')
            plt.axhline(y=6, color='lightgreen', linestyle='--', alpha=0.7, label='Bon (≥6)')
            plt.axhline(y=4, color='orange', linestyle='--', alpha=0.7, label='Moyen (≥4)')
            plt.legend()
            
            # Convertir en base64
            chart_base64 = self._chart_to_base64()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique des scores: {e}")
            return ""
    
    def _calculate_weather_summary(self, weather_data: Dict) -> Dict:
        """
        Calcule un résumé statistique des conditions météo
        """
        try:
            daily_data = weather_data.get('daily', [])
            
            if not daily_data:
                return {}
            
            # Statistiques des vagues
            wave_heights = [day.get('avg_wave_height', 0) for day in daily_data]
            wind_speeds = [day.get('avg_wind_speed', 0) for day in daily_data]
            
            summary = {
                'vagues': {
                    'moyenne': round(np.mean(wave_heights), 1),
                    'min': round(np.min(wave_heights), 1),
                    'max': round(np.max(wave_heights), 1),
                    'ecart_type': round(np.std(wave_heights), 1)
                },
                'vent': {
                    'moyenne': round(np.mean(wind_speeds), 1),
                    'min': round(np.min(wind_speeds), 1),
                    'max': round(np.max(wind_speeds), 1),
                    'ecart_type': round(np.std(wind_speeds), 1)
                },
                'jours_analyses': len(daily_data),
                'meilleurs_jours': self._find_best_surf_days(daily_data),
                'recommandations': self._generate_weather_recommendations(wave_heights, wind_speeds)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul du résumé météo: {e}")
            return {}
    
    def _find_best_surf_days(self, daily_data: List[Dict]) -> List[Dict]:
        """
        Trouve les meilleurs jours pour surfer
        """
        try:
            day_scores = []
            
            for day in daily_data:
                wave_height = day.get('avg_wave_height', 0)
                wind_speed = day.get('avg_wind_speed', 0)
                
                # Score simplifié
                wave_score = min(10, wave_height * 3) if wave_height > 0 else 0
                wind_score = max(0, 10 - wind_speed / 2)
                daily_score = (wave_score + wind_score) / 2
                
                day_scores.append({
                    'date': day['date'],
                    'score': round(daily_score, 1),
                    'wave_height': day.get('avg_wave_height', 0),
                    'wind_speed': day.get('avg_wind_speed', 0)
                })
            
            # Trier par score et retourner les 5 meilleurs
            day_scores.sort(key=lambda x: x['score'], reverse=True)
            return day_scores[:5]
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des meilleurs jours: {e}")
            return []
    
    def _generate_weather_recommendations(self, wave_heights: List[float], wind_speeds: List[float]) -> List[str]:
        """
        Génère des recommandations basées sur les conditions météo
        """
        recommendations = []
        
        try:
            avg_wave_height = np.mean(wave_heights)
            avg_wind_speed = np.mean(wind_speeds)
            
            # Recommandations sur les vagues
            if avg_wave_height < 1:
                recommendations.append("Vagues petites - idéal pour débutants")
            elif avg_wave_height > 3:
                recommendations.append("Vagues grandes - pour surfeurs expérimentés uniquement")
            else:
                recommendations.append("Vagues moyennes - parfait pour tous niveaux")
            
            # Recommandations sur le vent
            if avg_wind_speed < 10:
                recommendations.append("Vent léger - conditions optimales")
            elif avg_wind_speed > 25:
                recommendations.append("Vent fort - conditions difficiles")
            else:
                recommendations.append("Vent modéré - conditions acceptables")
            
            # Recommandations générales
            if avg_wave_height >= 1.5 and avg_wind_speed <= 15:
                recommendations.append("Conditions excellentes pour le surf !")
            elif avg_wave_height >= 1 and avg_wind_speed <= 20:
                recommendations.append("Bonnes conditions pour surfer")
            else:
                recommendations.append("Conditions moyennes - surfez avec précaution")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des recommandations: {e}")
            return ["Analyse des conditions en cours..."]
    
    def generate_ai_performance_metrics(self) -> Dict:
        """
        Génère des métriques de performance des systèmes IA
        """
        try:
            metrics = {
                'surf_prediction': {
                    'status': 'Actif' if surf_prediction_model.is_trained else 'Non entraîné',
                    'model_type': surf_prediction_model.get_model_info().get('model_type', 'N/A'),
                    'feature_count': surf_prediction_model.get_model_info().get('feature_count', 0)
                },
                'recommendation_system': {
                    'status': 'Actif' if recommendation_system.is_initialized else 'Non initialisé',
                    'spots_available': len(recommendation_system.spots_data) if hasattr(recommendation_system, 'spots_data') else 0,
                    'equipment_available': len(recommendation_system.equipment_data) if hasattr(recommendation_system, 'equipment_data') else 0
                },
                'booking_prediction': {
                    'demand_model': 'Entraîné' if booking_prediction_system.demand_model else 'Non entraîné',
                    'price_model': 'Entraîné' if booking_prediction_system.price_optimization_model else 'Non entraîné',
                    'cancellation_model': 'Entraîné' if booking_prediction_system.cancellation_model else 'Non entraîné'
                },
                'overall_performance': self._calculate_overall_ai_performance()
            }
            
            return {
                'success': True,
                'metrics': metrics,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des métriques IA: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_overall_ai_performance(self) -> Dict:
        """
        Calcule la performance globale des systèmes IA
        """
        try:
            # Score basé sur le nombre de systèmes actifs
            active_systems = 0
            total_systems = 3
            
            if surf_prediction_model.is_trained:
                active_systems += 1
            
            if recommendation_system.is_initialized:
                active_systems += 1
            
            if booking_prediction_system.is_trained:
                active_systems += 1
            
            performance_score = (active_systems / total_systems) * 100
            
            # Niveau de performance
            if performance_score >= 80:
                level = "Excellent"
                color = "green"
            elif performance_score >= 60:
                level = "Bon"
                color = "orange"
            else:
                level = "À améliorer"
                color = "red"
            
            return {
                'score': round(performance_score, 1),
                'level': level,
                'color': color,
                'active_systems': active_systems,
                'total_systems': total_systems
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la performance globale: {e}")
            return {'score': 0, 'level': 'Erreur', 'color': 'red'}
    
    def generate_spot_comparison_chart(self, spot_names: List[str] = None) -> str:
        """
        Crée un graphique de comparaison des spots
        """
        try:
            if not spot_names:
                spot_names = ['Taghazout', 'Essaouira', 'Agadir']
            
            plt.figure(figsize=(14, 8))
            
            # Données simulées pour la comparaison
            categories = ['Vagues', 'Vent', 'Température', 'Affluence', 'Accessibilité']
            
            # Scores pour chaque spot (0-10)
            taghazout_scores = [9, 7, 8, 6, 8]
            essaouira_scores = [7, 9, 7, 5, 9]
            agadir_scores = [6, 6, 9, 8, 9]
            
            # Créer le graphique radar
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]  # Fermer le polygone
            
            taghazout_scores += taghazout_scores[:1]
            essaouira_scores += essaouira_scores[:1]
            agadir_scores += agadir_scores[:1]
            
            ax = plt.subplot(111, projection='polar')
            ax.plot(angles, taghazout_scores, 'o-', linewidth=2, label='Taghazout', color='#1f77b4')
            ax.fill(angles, taghazout_scores, alpha=0.25, color='#1f77b4')
            
            ax.plot(angles, essaouira_scores, 'o-', linewidth=2, label='Essaouira', color='#ff7f0e')
            ax.fill(angles, essaouira_scores, alpha=0.25, color='#ff7f0e')
            
            ax.plot(angles, agadir_scores, 'o-', linewidth=2, label='Agadir', color='#2ca02c')
            ax.fill(angles, agadir_scores, alpha=0.25, color='#2ca02c')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 10)
            ax.set_title('Comparaison des Spots de Surf', fontsize=16, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            ax.grid(True)
            
            # Convertir en base64
            chart_base64 = self._chart_to_base64()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique de comparaison: {e}")
            return ""
    
    def _chart_to_base64(self) -> str:
        """
        Convertit un graphique matplotlib en base64
        """
        try:
            # Sauvegarder le graphique dans un buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            
            # Convertir en base64
            chart_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            
            return f"data:image/png;base64,{chart_base64}"
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion en base64: {e}")
            return ""
    
    def get_dashboard_summary(self) -> Dict:
        """
        Retourne un résumé complet du dashboard
        """
        try:
            return {
                'success': True,
                'dashboard_status': 'Actif' if self.is_initialized else 'Non initialisé',
                'available_analytics': [
                    'Analyse météo et conditions de surf',
                    'Comparaison des spots',
                    'Métriques de performance IA',
                    'Graphiques interactifs',
                    'Recommandations personnalisées'
                ],
                'last_updated': datetime.now().isoformat(),
                'systems_status': self.systems_status if hasattr(self, 'systems_status') else {}
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du résumé: {e}")
            return {'success': False, 'error': str(e)}

# Instance globale du dashboard
analytics_dashboard = AnalyticsDashboard()
