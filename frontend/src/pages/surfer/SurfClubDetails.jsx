import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './SurfClubDetails.css';

const SurfClubDetails = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { club } = location.state || {}; 

    if (!club) {
        return <p className="surfclub-details-loading">Loading...</p>;
    }

    const handleReserveClick = () => {
        navigate(`/reserve-session/${club.id}`);
    };

    return (
        <div className="surfclub-details-page">
            <div className="surfclub-details-header">
                <img src={`http://localhost:8000${club.logo}`} alt={club.name} className="surfclub-details-logo"/>
                <h1 className="surfclub-details-title">{club.name}</h1>
            </div>
            <div className="surfclub-details-action-cards">
                <div className="surfclub-details-action-card">
                    <h2 className="surfclub-details-action-title">I buy</h2>
                    <p className="surfclub-details-action-description">Explore our available equipment for purchase !</p>
                    <button className="surfclub-details-action-button" onClick={() => navigate(`/surf-clubs/${club.id}/equipments`)}>Buy</button>
                </div>
                <div className="surfclub-details-action-card">
                    <h2 className="surfclub-details-action-title">I book a session</h2>
                    <p className="surfclub-details-action-description">Book your next surf session with us !</p>
                    <button className="surfclub-details-action-button" onClick={handleReserveClick}>Book</button>
                </div>
            </div>
        </div>
    );
};

export default SurfClubDetails;
