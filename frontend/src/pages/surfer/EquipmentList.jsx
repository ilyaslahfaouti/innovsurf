import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import './EquipmentList.css'; 

const EquipmentList = () => {
    const { id } = useParams(); // ID of the Surf Club
    const [equipments, setEquipments] = useState([]);

    useEffect(() => {
        const fetchEquipments = async () => {
            const token = localStorage.getItem('accessToken');
            try {
                const response = await axios.get(`http://localhost:8000/api/surf-clubs/${id}/equipments/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setEquipments(response.data.Equipments);
            } catch (error) {
                console.error("Failed to fetch equipments", error);
            }
        };

        fetchEquipments();
    }, [id]);

    return (
        <div className="equipment-list-page-specific">
            <h1 className="equipment-list-title-specific">Equipements for sale</h1>
            <div className="equipment-grid-specific">
                {equipments.map((equipment) => (
                    <div key={equipment.id} className="equipment-item-specific">
                        {equipment.is_sell && <div className="equipment-badge-specific">SALE</div>}
                        <div className="equipment-photo-container-specific">
                            <img 
                                src={`http://localhost:8000${equipment.photos[0]?.image}`} 
                                alt={equipment.name} 
                                className="equipment-photo-specific" 
                            />
                        </div>
                        <div className="equipment-info-specific">
                            <h3 className="equipment-name-specific">{equipment.name}</h3>
                            <p className="equipment-price-specific">
                                {equipment.sale_price ? `${equipment.sale_price} €` : `${equipment.rent_price} €`}
                            </p>
                            <div className="equipment-rating-specific">
                                ⭐️⭐️⭐️⭐️⭐️
                            </div>
                            <Link 
                                to={`/equipment/${equipment.id}`} 
                                state={{ equipment, surfClubId: id }} 
                                className="equipment-details-link-specific"
                            >
                                View products
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EquipmentList;
