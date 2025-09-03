import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import SurfClubList from '../../components/SurfClubList'; 
import './SurfSpotDetails.css'; 

const SurfSpotDetails = () => {
    const { id } = useParams();
    const [surfSpot, setSurfSpot] = useState(null);
    const [currentSlide, setCurrentSlide] = useState(0);

    useEffect(() => {
        const fetchSurfSpotDetails = async () => {
            try {
                const token = localStorage.getItem('accessToken');
                const response = await axios.get(`http://localhost:8000/api/surf-spots/${id}/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setSurfSpot(response.data['surf-spot']);
            } catch (error) {
                console.error("Failed to fetch surf spot details", error);
            }
        };

        fetchSurfSpotDetails();
    }, [id]);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentSlide((prev) => (prev === surfSpot?.photos.length - 1 ? 0 : prev + 1));
        }, 3000); // Change slide every 3 seconds

        return () => clearInterval(interval);
    }, [surfSpot?.photos.length]);

    if (!surfSpot) {
        return <p className="surfspot-details-page-loading">Loading...</p>;
    }

    return (
        <div className="surfspot-details-page">
            <div className="surfspot-details-card">
                <div className="surfspot-info">
                    <h2 className="surfspot-info-title">{surfSpot.name}</h2>
                    <p className="surfspot-info-description">{surfSpot.description}</p>
                    
                    <p className="surfspot-info-address">
                        <i className="fas fa-map-marker-alt"></i> {surfSpot.address}
                    </p>
                </div>

                <div className="surfspot-slider">
                    <div className="surfspot-slider-wrapper" style={{ transform: `translateX(-${currentSlide * 100}%)` }}>
                        {surfSpot.photos && surfSpot.photos.length > 0 ? (
                            surfSpot.photos.map((photo, index) => (
                                <div 
                                    key={index} 
                                    className={`surfspot-slide ${index === currentSlide ? 'active' : ''}`}
                                    style={{backgroundImage: `url(http://localhost:8000${photo.image})`}}
                                >
                                </div>
                            ))
                        ) : (
                            <p>No photos available</p>
                        )}
                    </div>
                </div>
            </div>

            <h2 className="surfspot-clubs-title">Surf Clubs</h2>
            <SurfClubList clubs={surfSpot.surf_clubs} />
        </div>
    );
};

export default SurfSpotDetails;
