import React, { useEffect, useState } from 'react';
import axios from 'axios';
import SurfSpotCard from '../../components/SurfSpotCard';
import './SurfClubs.css'; 

const SurfClubs = () => {
    const [surfSpots, setSurfSpots] = useState([]);

    useEffect(() => {
        const fetchSurfSpots = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/surf-spots/');
                setSurfSpots(response.data);
            } catch (error) {
                console.error("Failed to fetch surf spots", error);
            }
        };

        fetchSurfSpots();
    }, []);

    return (
        <div className="surf-clubs-page">
            <h1 className="page-title">Select a Surf Spot</h1>
            <div className="surf-spot-list">
                {surfSpots.map((spot) => (
                    <SurfSpotCard key={spot.id} surfSpot={spot} />
                ))}
            </div>
        </div>
    );
};

export default SurfClubs;
