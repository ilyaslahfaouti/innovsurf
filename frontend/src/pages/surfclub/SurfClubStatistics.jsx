import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SurfClubStatistics.css'; 

const SurfClubStatistics = () => {
    const [statistics, setStatistics] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const token = localStorage.getItem('accessToken');

    useEffect(() => {
        const fetchStatistics = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/surf-club/statistics/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setStatistics(response.data);
            } catch (err) {
                setError(err.response ? err.response.data : 'An error occurred');
                if (err.response && err.response.status === 401) {
                    navigate('/login'); 
                }
            }
        };

        fetchStatistics();
    }, [token, navigate]);

    if (error) return <p className="error-message">Error: {error}</p>;
    if (!statistics) return <p className="loading-message">Loading...</p>;

    return (
        <div className="surfclub-statistics">
            <h1 className="statistics-title">Surf Club Statistics</h1>
            <div className="statistics-cards">
                <div className="statistics-card">
                    <h2>{statistics.surf_club_name}</h2>
                    <p className="card-description">Surf Club Name</p>
                </div>
                <div className="statistics-card">
                    <h2>{statistics.number_of_monitors}</h2>
                    <p className="card-description">Number of Monitors</p>
                </div>
                <div className="statistics-card">
                    <h2>{statistics.number_of_equipment}</h2>
                    <p className="card-description">Number of Equipment</p>
                </div>
                <div className="statistics-card">
                    <h2>{statistics.number_of_orders}</h2>
                    <p className="card-description">Number of Orders</p>
                </div>
                <div className="statistics-card">
                    <h2>{statistics.number_of_surf_lessons}</h2>
                    <p className="card-description">Number of Surf Lessons</p>
                </div>
                <div className="statistics-card">
                    <h2>{statistics.number_of_surf_sessions}</h2>
                    <p className="card-description">Number of Surf Sessions</p>
                </div>
            </div>
        </div>
    );
};

export default SurfClubStatistics;
