import React from 'react';
import SurfClubCard from './SurfClubCard';
import './SurfClubList.css'; 

const SurfClubList = ({ clubs }) => {
    if (!clubs || clubs.length === 0) {
        return <p className="no-clubs-message">No clubs available for this surf spot.</p>;
    }

    return (
        <div className="surf-club-list">
            {clubs.map((club) => (
                <SurfClubCard key={club.id} club={club} />
            ))}
        </div>
    );
};

export default SurfClubList;
