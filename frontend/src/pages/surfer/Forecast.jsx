import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import './Forecast.css'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faWind, faWater, faThermometerHalf, faTachometerAlt } from '@fortawesome/free-solid-svg-icons';

const Forecast = () => {
    const location = useLocation();
    const spot = location.state?.spot;
    const [forecast, setForecast] = useState(null);
    const [currentCondition, setCurrentCondition] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [debugData, setDebugData] = useState(null);

    useEffect(() => {
        if (spot) {
            const fetchForecast = async () => {
                try {
                    setLoading(true);
                    setError(null);
                    setDebugData(null);
                    
                    console.log('Fetching forecast for spot:', spot);
                    
                    const response = await axios.get(`http://localhost:8000/api/surf-spots/prevision/${spot.id}/`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    });
                    
                    console.log('Full API Response:', response);
                    console.log('Response data:', response.data);
                    console.log('Response status:', response.status);
                    
                    setDebugData(response.data);
                    
                    const forecastData = response.data.forecast;
                    console.log('Forecast data extracted:', forecastData);
                    
                    // Vérifier si forecastData existe
                    if (!forecastData) {
                        console.warn("No forecast data in response");
                        setError("Aucune donnée de prévision trouvée dans la réponse de l'API");
                        setLoading(false);
                        return;
                    }
                    
                    // Vérifier si l'API StormGlass a dépassé son quota
                    if (forecastData.errors && forecastData.errors.key === "API quota exceeded") {
                        console.warn("StormGlass API quota exceeded");
                        const quotaInfo = forecastData.meta ? 
                            ` (${forecastData.meta.requestCount}/${forecastData.meta.dailyQuota} requêtes utilisées)` : '';
                        setError(`Quota de l'API météo dépassé${quotaInfo}. Les prévisions ne sont pas disponibles pour le moment.`);
                        setLoading(false);
                        return;
                    }
                    
                    // Vérifier si forecastData contient des erreurs
                    if (forecastData.errors) {
                        console.warn("Forecast data contains errors:", forecastData.errors);
                        setError(`Erreur de l'API météo: ${Object.values(forecastData.errors).join(', ')}`);
                        setLoading(false);
                        return;
                    }
                    
                    // Vérifier la structure des données - plusieurs formats possibles
                    let processedHours = [];
                    
                    // Format 1: StormGlass avec data
                    if (forecastData.data && typeof forecastData.data === 'object') {
                        console.log("Detected StormGlass format with data");
                        processedHours = processStormGlassData(forecastData.data);
                    }
                    // Format 2: Données directes avec hours
                    else if (forecastData.hours && Array.isArray(forecastData.hours)) {
                        console.log("Detected direct format with hours");
                        processedHours = forecastData.hours;
                    }
                    // Format 3: Données directes sans structure
                    else if (Array.isArray(forecastData)) {
                        console.log("Detected array format");
                        processedHours = forecastData;
                    }
                    // Format 4: Données StormGlass directes
                    else if (typeof forecastData === 'object' && Object.keys(forecastData).length > 0) {
                        console.log("Detected direct StormGlass format");
                        processedHours = processStormGlassData(forecastData);
                    }
                    else {
                        console.warn("Unknown forecast data format:", forecastData);
                        setError("Format de données de prévision non reconnu");
                        setLoading(false);
                        return;
                    }
                    
                    console.log("Processed hours:", processedHours);
                    
                    if (processedHours && processedHours.length > 0) {
                        setForecast({ hours: processedHours });
                        
                        // Trouver les conditions actuelles
                        const now = new Date();
                        const currentData = processedHours.find(hour => 
                            hour && hour.time && new Date(hour.time).getTime() >= now.getTime()
                        );
                        
                        setCurrentCondition(currentData || processedHours[0]);
                    } else {
                        console.warn("No processed hours available");
                        setError("Aucune donnée météorologique disponible après traitement");
                    }
                    
                } catch (error) {
                    console.error("Failed to fetch forecast", error);
                    setError(`Erreur lors du chargement des prévisions: ${error.message}`);
                } finally {
                    setLoading(false);
                }
            };

            fetchForecast();
        }
    }, [spot]);

    // Fonction pour traiter les données StormGlass
    const processStormGlassData = (stormGlassData) => {
        const processedHours = [];
        
        // StormGlass retourne les données par paramètre, pas par heure
        const timeKeys = new Set();
        
        // Collecter toutes les clés de temps
        Object.values(stormGlassData).forEach(paramData => {
            if (paramData && Array.isArray(paramData)) {
                paramData.forEach(item => {
                    if (item && item.time) {
                        timeKeys.add(item.time);
                    }
                });
            }
        });
        
        // Convertir en array et trier par temps
        const sortedTimes = Array.from(timeKeys).sort();
        
        // Créer des objets par heure avec toutes les données
        sortedTimes.forEach(time => {
            const hourData = {
                time: time,
                waveHeight: { meteo: null },
                swellPeriod: { meteo: null },
                windSpeed: { noaa: null },
                airTemperature: { noaa: null },
                waterTemperature: { noaa: null }
            };
            
            // Remplir les données pour cette heure
            if (stormGlassData.waveHeight) {
                const waveItem = stormGlassData.waveHeight.find(item => item.time === time);
                if (waveItem) {
                    hourData.waveHeight.meteo = waveItem.waveHeight?.meteo || waveItem.waveHeight?.noaa;
                }
            }
            
            if (stormGlassData.swellPeriod) {
                const swellItem = stormGlassData.swellPeriod.find(item => item.time === time);
                if (swellItem) {
                    hourData.swellPeriod.meteo = swellItem.swellPeriod?.meteo || swellItem.swellPeriod?.noaa;
                }
            }
            
            if (stormGlassData.windSpeed) {
                const windItem = stormGlassData.windSpeed.find(item => item.time === time);
                if (windItem) {
                    hourData.windSpeed.noaa = windItem.windSpeed?.meteo || windItem.windSpeed?.noaa;
                }
            }
            
            if (stormGlassData.airTemperature) {
                const tempItem = stormGlassData.airTemperature.find(item => item.time === time);
                if (tempItem) {
                    hourData.airTemperature.noaa = tempItem.airTemperature?.meteo || tempItem.airTemperature?.noaa;
                }
            }
            
            if (stormGlassData.waterTemperature) {
                const waterTempItem = stormGlassData.waterTemperature.find(item => item.time === time);
                if (waterTempItem) {
                    hourData.waterTemperature = waterTempItem.waterTemperature?.meteo || waterTempItem.waterTemperature?.noaa;
                }
            }
            
            // Ajouter un rating basé sur les conditions
            hourData.rating = calculateSurfRating(hourData);
            
            processedHours.push(hourData);
        });
        
        return processedHours;
    };
    
    // Fonction pour calculer un rating de surf basé sur les conditions
    const calculateSurfRating = (hourData) => {
        let rating = 0;
        
        // Rating basé sur la hauteur des vagues (1-3m = optimal)
        if (hourData.waveHeight?.meteo) {
            const waveHeight = hourData.waveHeight.meteo;
            if (waveHeight >= 1 && waveHeight <= 3) rating += 3;
            else if (waveHeight >= 0.5 && waveHeight <= 4) rating += 2;
            else if (waveHeight > 0) rating += 1;
        }
        
        // Rating basé sur la période des vagues (8-15s = optimal)
        if (hourData.swellPeriod?.meteo) {
            const swellPeriod = hourData.swellPeriod.meteo;
            if (swellPeriod >= 8 && swellPeriod <= 15) rating += 2;
            else if (swellPeriod >= 6 && swellPeriod <= 20) rating += 1;
        }
        
        // Rating basé sur le vent (moins de vent = mieux)
        if (hourData.windSpeed?.noaa) {
            const windSpeed = hourData.windSpeed.noaa;
            if (windSpeed <= 10) rating += 2;
            else if (windSpeed <= 20) rating += 1;
        }
        
        // Rating basé sur la température de l'eau
        if (hourData.waterTemperature) {
            const waterTemp = hourData.waterTemperature;
            if (waterTemp >= 18 && waterTemp <= 25) rating += 1;
        }
        
        // Convertir en étoiles (1-5)
        if (rating >= 7) return '⭐⭐⭐⭐⭐';
        else if (rating >= 5) return '⭐⭐⭐⭐';
        else if (rating >= 3) return '⭐⭐⭐';
        else if (rating >= 1) return '⭐⭐';
        else return '⭐';
    };

    // Gestion des cas d'erreur et de chargement
    if (!spot) {
        return (
            <div className="forecast-page">
                <h1>Erreur</h1>
                <p>Aucun spot de surf sélectionné.</p>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="forecast-page">
                <h1>Chargement des prévisions...</h1>
                <p>Veuillez patienter pendant le chargement des données météorologiques.</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="forecast-page">
                <h1>Prévisions non disponibles</h1>
                
                {/* Message d'erreur principal */}
                <div style={{ 
                    padding: '20px', 
                    backgroundColor: '#fff3cd', 
                    border: '1px solid #ffeaa7', 
                    borderRadius: '8px',
                    marginBottom: '20px'
                }}>
                    <h2 style={{ color: '#856404', marginTop: 0 }}>⚠️ {error}</h2>
                    
                    {/* Informations sur le quota */}
                    {debugData?.forecast?.meta && (
                        <div style={{ marginTop: '15px' }}>
                            <p><strong>Statut de l'API météo :</strong></p>
                            <ul style={{ margin: '10px 0', paddingLeft: '20px' }}>
                                <li>Quota quotidien : {debugData.forecast.meta.dailyQuota} requêtes</li>
                                <li>Requêtes utilisées : {debugData.forecast.meta.requestCount}</li>
                                <li>Requêtes restantes : {Math.max(0, debugData.forecast.meta.dailyQuota - debugData.forecast.meta.requestCount)}</li>
                            </ul>
                        </div>
                    )}
                    
                    {/* Solutions suggérées */}
                    <div style={{ marginTop: '20px' }}>
                        <p><strong>Solutions :</strong></p>
                        <ul style={{ margin: '10px 0', paddingLeft: '20px' }}>
                            <li>Les prévisions seront disponibles demain (quota quotidien réinitialisé)</li>
                            <li>Vous pouvez consulter les informations générales du spot ci-dessous</li>
                            <li>Contactez l'équipe technique si le problème persiste</li>
                        </ul>
                    </div>
                </div>
                
                {/* Informations du spot (toujours disponibles) */}
                {debugData && (
                    <div style={{ 
                        padding: '20px', 
                        backgroundColor: '#f8f9fa', 
                        border: '1px solid #dee2e6', 
                        borderRadius: '8px',
                        marginBottom: '20px'
                    }}>
                        <h3>Informations du spot : {debugData.name}</h3>
                        <p><strong>Localisation :</strong> {debugData.address}</p>
                        <p><strong>Description :</strong> {debugData.description}</p>
                        <p><strong>Coordonnées :</strong> {debugData.latitude}, {debugData.longitude}</p>
                        
                        {debugData.surf_clubs && debugData.surf_clubs.length > 0 && (
                            <div style={{ marginTop: '15px' }}>
                                <p><strong>Clubs disponibles :</strong></p>
                                <ul style={{ margin: '10px 0', paddingLeft: '20px' }}>
                                    {debugData.surf_clubs.map(club => (
                                        <li key={club.id}>{club.name}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}
                
                {/* Debug information pour les développeurs */}
                {debugData && (
                    <div style={{ 
                        marginTop: '20px', 
                        padding: '15px', 
                        backgroundColor: '#f5f5f5', 
                        borderRadius: '5px',
                        border: '1px solid #ddd'
                    }}>
                        <h3>Données de debug (pour les développeurs)</h3>
                        <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                            {JSON.stringify(debugData, null, 2)}
                        </pre>
                    </div>
                )}
                
                <div style={{ marginTop: '20px' }}>
                    <button onClick={() => window.history.back()}>Retour</button>
                    <button 
                        onClick={() => window.location.reload()} 
                        style={{ marginLeft: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px' }}
                    >
                        Réessayer
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="forecast-page">
            <h1>Prévisions pour {spot.name}</h1>
            
            {currentCondition && (
                <div className="current-condition">
                    <h2>Conditions actuelles de surf</h2>
                    <div className="current-condition-grid">
                        <div className="condition-item">
                            <FontAwesomeIcon icon={faWater} className="condition-icon" />
                            <p className="condition-label">Vagues:</p>
                            <p className="condition-value">
                                {currentCondition.waveHeight?.meteo ? 
                                    `${currentCondition.waveHeight.meteo.toFixed(2)} m` : 'N/A'}
                            </p>
                        </div>
                        <div className="condition-item">
                            <FontAwesomeIcon icon={faTachometerAlt} className="condition-icon" />
                            <p className="condition-label">Note:</p>
                            <p className="condition-value condition-rating">
                                {currentCondition.rating || 'N/A'}
                            </p>
                        </div>
                        <div className="condition-item">
                            <FontAwesomeIcon icon={faWind} className="condition-icon" />
                            <p className="condition-label">Vent:</p>
                            <p className="condition-value">
                                {currentCondition.windSpeed?.noaa ? 
                                    `${currentCondition.windSpeed.noaa.toFixed(2)} m/s` : 'N/A'}
                            </p>
                        </div>
                        <div className="condition-item">
                            <FontAwesomeIcon icon={faThermometerHalf} className="condition-icon" />
                            <p className="condition-label">Température:</p>
                            <p className="condition-value">
                                {currentCondition.airTemperature?.noaa ? 
                                    `${currentCondition.airTemperature.noaa.toFixed(2)} °C` : 'N/A'}
                            </p>
                        </div>
                    </div>
                </div>
            )}
            
            {forecast && forecast.hours && Array.isArray(forecast.hours) && forecast.hours.length > 0 ? (
                <div className="forecast-details">
                    <h2>Prévisions météorologiques</h2>
                    <table className="forecast-table">
                        <thead>
                            <tr>
                                <th>Heure</th>
                                <th>Hauteur des vagues (m)</th>
                                <th>Période des vagues (s)</th>
                                <th>Vitesse du vent (m/s)</th>
                                <th>Température (°C)</th>
                                <th>Note surf</th>
                            </tr>
                        </thead>
                        <tbody>
                            {forecast.hours.map((data, index) => {
                                // Vérifier que data existe et a les propriétés nécessaires
                                if (!data) return null;
                                
                                return (
                                    <tr key={index}>
                                        <td>
                                            <i className="fas fa-clock"></i> 
                                            {data.time ? new Date(data.time).toLocaleString('fr-FR') : 'N/A'}
                                        </td>
                                        <td>
                                            {data.waveHeight?.meteo ? 
                                                data.waveHeight.meteo.toFixed(2) : 'N/A'}
                                        </td>
                                        <td>
                                            {data.swellPeriod?.meteo ? 
                                                data.swellPeriod.meteo.toFixed(2) : 'N/A'}
                                        </td>
                                        <td>
                                            {data.windSpeed?.noaa ? 
                                                data.windSpeed.noaa.toFixed(2) : 'N/A'}
                                        </td>
                                        <td>
                                            {data.airTemperature?.noaa ? 
                                                data.airTemperature.noaa.toFixed(2) : 'N/A'}
                                        </td>
                                        <td>
                                            {data.rating || 'N/A'}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="forecast-details">
                    <h2>Prévisions météorologiques</h2>
                    <p>Aucune donnée de prévision disponible pour le moment.</p>
                    
                    {/* Debug information */}
                    {debugData && (
                        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '5px' }}>
                            <h3>Données reçues de l'API</h3>
                            <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                                {JSON.stringify(debugData, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Forecast;
