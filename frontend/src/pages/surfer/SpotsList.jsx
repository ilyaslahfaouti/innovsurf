import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './SpotsList.css'; // Import the new CSS file for styling
import surfVideo from '../../assets/video/spots.mp4'; // Import the video file

const SpotsList = () => {
    const [spots, setSpots] = useState([]);

    useEffect(() => {
        const fetchSpots = async () => {
            try {
                const token = localStorage.getItem('accessToken');
                const response = await axios.get('http://localhost:8000/api/surf-spots/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setSpots(response.data);
            } catch (error) {
                console.error("Failed to fetch spots", error);
            }
        };

        fetchSpots();
    }, []);

    return (
        <div>
            {/* Video Header Section */}
            <div className="video-header-container">
                <video autoPlay loop muted className="video-background">
                    <source src={surfVideo} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                <div className="video-overlay">
                    <h1 className="video-title">Innov' Forum</h1>
                    <p className="video-subtitle">It brings together the surfing community from all over Morocco !</p>
                </div>
            </div>

            <div className="spots-list-container">
                <h1 className="spots-title">Surf Spots</h1>
                <div className="spots-grid">
                    {spots.map((spot) => (
                        <Link 
                            to={`/forum/${spot.id}`}  
                            className="spot-card"
                            key={spot.id}
                        >
                            {spot.photos.length > 0 && spot.photos[0] ? (
                                <div className="spot-image-wrapper">
                                    <img src={`http://localhost:8000${spot.photos[0].image}`} alt={spot.name} className="spot-image"/>
                                </div>
                            ) : (
                                <div className="spot-image-placeholder">No Image Available</div>
                            )}
                            <div className="spot-info">
                                <h2 className="spot-name">{spot.name}</h2>
                                <p className="spot-location">{spot.location}</p>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SpotsList;
