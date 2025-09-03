import React from 'react';
import { Link } from 'react-router-dom';
import './SurfClubCard.css'; 

const SurfClubCard = ({ club }) => {
    return (
        <div className="surf-club-card">
            <Link to={`/surf-clubs/${club.id}`} state={{ club }} className="surf-club-link">
                <div className="surf-club-image-wrapper">
                    <img src={`http://localhost:8000${club.logo}`} alt={club.name} className="surf-club-image" />
                </div>
                <div className="surf-club-info">
                    <h3 className="surf-club-name">{club.name}</h3>
                </div>
            </Link>
        </div>
    );
};

export default SurfClubCard;
