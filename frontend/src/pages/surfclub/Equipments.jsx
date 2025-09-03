import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './Equipments.css'; 
import defaultEquipmentImage from '../../assets/equipment.jpg'; 

const Equipments = () => {
  const [equipments, setEquipments] = useState([]);
  const navigate = useNavigate();

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    const fetchEquipments = async () => {
      try {
        const token = getAuthToken();
        const headers = {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        };
        const response = await axios.get('http://localhost:8000/api/surf-club/equipments/', { headers });
        setEquipments(response.data.equipments);
      } catch (error) {
        console.error('Error fetching equipment:', error);
      }
    };

    fetchEquipments();
  }, []);

  const handleDelete = async (id) => {
    const confirmed = window.confirm("Are you sure you want to delete this equipment?");
    if (confirmed) {
      try {
        const token = getAuthToken();
        const headers = {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        };
        await axios.delete(`http://localhost:8000/api/surf-club/equipment/${id}/`, { headers });
        setEquipments(equipments.filter(equipment => equipment.id !== id));
      } catch (error) {
        console.error('Error deleting equipment:', error);
      }
    }
  };

  const handleEdit = (id) => {
    navigate(`/dashboard/equipment/${id}/edit`);
  };

  return (
    <div className="equipments-container">
      <div className="header">
        <h1>Equipments</h1>
        <Link to="/dashboard/equipment/create" className="add-link">Add New Equipment</Link>
      </div>
      <ul className="equipments-list">
        {equipments.map(equipment => (
          <li key={equipment.id} className="equipment-item">
            <div className="equipment-image">
              <img
                src={equipment.photos.length > 0 ? `http://localhost:8000${equipment.photos[0].image}` : defaultEquipmentImage}
                alt={equipment.name}
                className="equipment-photo"
              />
            </div>
            <div className="equipment-content">
              <h3>{equipment.name}</h3>
              <p><i className="fas fa-ruler"></i> {equipment.size}</p>
              <p><i className="fas fa-tag"></i> {equipment.state}</p>

              {equipment.material_type === 'rent' && (
                <p><i className="fas fa-dollar-sign"></i>{equipment.rent_price}</p>
              )}
              {equipment.material_type === 'sale' && (
                <p><i className="fas fa-dollar-sign"></i> {equipment.sale_price}</p>
              )}

              <p><i className="fas fa-boxes"></i> {equipment.quantity}</p>

              <div className="equipment-actions">
                <button onClick={() => handleEdit(equipment.id)} className="action-link">
                  <i className="fas fa-edit"></i>
                </button>
                <button onClick={() => handleDelete(equipment.id)} className="action-link">
                  <i className="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Equipments;
