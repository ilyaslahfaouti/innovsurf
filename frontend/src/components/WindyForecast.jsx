import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './WindyForecast.css';

const WindyForecast = ({ spotName, onClose }) => {
    const [forecast, setForecast] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedDays, setSelectedDays] = useState(3);

    useEffect(() => {
        if (spotName) {
            fetchForecast(spotName, selectedDays);
        }
    }, [spotName, selectedDays]);

    const fetchForecast = async (spot, days) => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await axios.get(`http://localhost:8000/api/windy/forecast/?spot=${spot}&days=${days}`);
            setForecast(response.data);
        } catch (err) {
            console.error('Erreur lors de la récupération des prévisions:', err);
            setError('Impossible de récupérer les prévisions météo. Vérifiez votre connexion.');
        } finally {
            setLoading(false);
        }
    };

    const fetchOptimalTimes = async (spot) => {
        try {
            setLoading(true);
            const response = await axios.get(`http://localhost:8000/api/windy/optimal-times/?spot=${spot}&days=3`);
            return response.data;
        } catch (err) {
            console.error('Erreur lors de la récupération des moments optimaux:', err);
            return null;
        } finally {
            setLoading(false);
        }
    };

    const getWindDirection = (degrees) => {
        const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO'];
        const index = Math.round(degrees / 22.5) % 16;
        return directions[index];
    };

    const getWaveHeightColor = (height) => {
        if (height < 0.5) return '#e74c3c'; // Rouge - trop petit
        if (height < 1) return '#f39c12';   // Orange - petit
        if (height < 2) return '#f1c40f';   // Jaune - moyen
        if (height < 3) return '#27ae60';   // Vert - bon
        return '#8e44ad';                    // Violet - grand
    };

    const getWindSpeedColor = (speed) => {
        if (speed < 10) return '#27ae60';   // Vert - optimal
        if (speed < 15) return '#f1c40f';   // Jaune - acceptable
        if (speed < 20) return '#f39c12';   // Orange - difficile
        return '#e74c3c';                    // Rouge - trop fort
    };

    if (loading) {
        return (
            <div className="windy-forecast-overlay">
                <div className="windy-forecast-container">
                    <div className="loading-spinner">
                        <div className="spinner"></div>
                        <p>Chargement des prévisions météo...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="windy-forecast-overlay">
                <div className="windy-forecast-container">
                    <div className="error-message">
                        <h3>❌ Erreur</h3>
                        <p>{error}</p>
                        <button onClick={() => fetchForecast(spotName, selectedDays)} className="retry-button">
                            Réessayer
                        </button>
                        <button onClick={onClose} className="close-button">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    if (!forecast || !forecast.success) {
        return (
            <div className="windy-forecast-overlay">
                <div className="windy-forecast-container">
                    <div className="no-data">
                        <h3>📊 Aucune donnée disponible</h3>
                        <p>Impossible de récupérer les prévisions pour {spotName}</p>
                        <button onClick={onClose} className="close-button">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="windy-forecast-overlay">
            <div className="windy-forecast-container">
                {/* Header */}
                <div className="windy-header">
                    <h2>🌊 Prévisions Météo - {spotName}</h2>
                    <div className="windy-controls">
                        <select 
                            value={selectedDays} 
                            onChange={(e) => setSelectedDays(parseInt(e.target.value))}
                            className="days-selector"
                        >
                            <option value={1}>1 jour</option>
                            <option value={3}>3 jours</option>
                            <option value={7}>7 jours</option>
                        </select>
                        <button onClick={onClose} className="close-button">✕</button>
                    </div>
                </div>

                {/* Conditions actuelles */}
                {forecast.current_conditions && (
                    <div className="current-conditions">
                        <h3>📅 Conditions actuelles</h3>
                        <div className="conditions-grid">
                            <div className="condition-item">
                                <span className="condition-label">📏 Vagues</span>
                                <span 
                                    className="condition-value wave-height"
                                    style={{ color: getWaveHeightColor(forecast.current_conditions.wave_height) }}
                                >
                                    {forecast.current_conditions.wave_height}m
                                </span>
                            </div>
                            <div className="condition-item">
                                <span className="condition-label">💨 Vent</span>
                                <span 
                                    className="condition-value wind-speed"
                                    style={{ color: getWindSpeedColor(forecast.current_conditions.wind_speed) }}
                                >
                                    {forecast.current_conditions.wind_speed} km/h
                                </span>
                            </div>
                            <div className="condition-item">
                                <span className="condition-label">🧭 Direction</span>
                                <span className="condition-value">
                                    {getWindDirection(forecast.current_conditions.wind_direction)}
                                </span>
                            </div>
                            <div className="condition-item">
                                <span className="condition-label">🌡️ Eau</span>
                                <span className="condition-value">
                                    {forecast.current_conditions.water_temp}°C
                                </span>
                            </div>
                        </div>
                    </div>
                )}

                {/* Prévisions quotidiennes */}
                <div className="daily-forecast">
                    <h3>📈 Prévisions sur {selectedDays} jours</h3>
                    <div className="forecast-days">
                        {forecast.daily && forecast.daily.map((day, index) => (
                            <div key={index} className="forecast-day">
                                <div className="day-header">
                                    <h4>{new Date(day.date).toLocaleDateString('fr-FR', { 
                                        weekday: 'long', 
                                        day: 'numeric', 
                                        month: 'long' 
                                    })}</h4>
                                </div>
                                
                                <div className="day-stats">
                                    <div className="stat-item">
                                        <span className="stat-label">📏 Vagues moyennes</span>
                                        <span 
                                            className="stat-value"
                                            style={{ color: getWaveHeightColor(day.avg_wave_height) }}
                                        >
                                            {day.avg_wave_height}m
                                        </span>
                                    </div>
                                    <div className="stat-item">
                                        <span className="stat-label">💨 Vent moyen</span>
                                        <span 
                                            className="stat-value"
                                            style={{ color: getWindSpeedColor(day.avg_wind_speed) }}
                                        >
                                            {day.avg_wind_speed} km/h
                                        </span>
                                    </div>
                                </div>

                                {/* Meilleures heures */}
                                {day.best_hours && day.best_hours.length > 0 && (
                                    <div className="best-hours">
                                        <h5>⏰ Meilleures heures</h5>
                                        <div className="hours-list">
                                            {day.best_hours.map((hour, hourIndex) => (
                                                <div key={hourIndex} className="best-hour">
                                                    <span className="hour-time">{hour.hour}h</span>
                                                    <span className="hour-score">Score: {hour.score}/10</span>
                                                    <span className="hour-waves">{hour.wave_height}m</span>
                                                    <span className="hour-wind">{hour.wind_speed} km/h</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Bouton pour obtenir les moments optimaux */}
                <div className="optimal-times-section">
                    <button 
                        onClick={() => fetchOptimalTimes(spotName)}
                        className="optimal-times-button"
                    >
                        🏄‍♂️ Voir les meilleurs moments pour surfer
                    </button>
                </div>

                {/* Footer */}
                <div className="windy-footer">
                    <p>🌊 Données météo fournies par Windy</p>
                    <p>💡 Conseil: Les meilleures conditions sont généralement tôt le matin ou en fin d'après-midi</p>
                </div>
            </div>
        </div>
    );
};

export default WindyForecast;
