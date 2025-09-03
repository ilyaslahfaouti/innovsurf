import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './ReserveSession.css'; 
import PhotoEquipment from '../../assets/equipmentts.jpg'; 

const ReserveSession = () => {
    const { id } = useParams();
    const [sessions, setSessions] = useState([]);
    const [equipments, setEquipments] = useState([]);
    const [selectedSession, setSelectedSession] = useState(null);
    const [selectedEquipment, setSelectedEquipment] = useState([]);
    const [equipmentQuantities, setEquipmentQuantities] = useState({});
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchReserveSessionDetails = async () => {
            try {
                const token = localStorage.getItem('accessToken');
                const response = await axios.get(`http://localhost:8000/api/surf-clubs/${id}/lessons/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setSessions(response.data.SurfSession);
                setEquipments(response.data.Equipments);
            } catch (error) {
                console.error("Failed to fetch reserve session details", error);
            }
        };

        fetchReserveSessionDetails();
    }, [id]);

    const handleSessionSelect = (session) => {
        setSelectedSession(session);
    };

    const handleEquipmentSelect = (equipment) => {
        setSelectedEquipment(prev => {
            const isSelected = prev.includes(equipment);

            if (isSelected) {
                const updatedEquipment = prev.filter(item => item !== equipment);
                const { [equipment.id]: removed, ...rest } = equipmentQuantities;
                setEquipmentQuantities(rest);
                return updatedEquipment;
            } else {
                if (equipment.quantity > 0) {
                    setEquipmentQuantities(prevQuantities => ({
                        ...prevQuantities,
                        [equipment.id]: 1, 
                    }));
                    return [...prev, equipment];
                } else {
                    alert(`Le matériel ${equipment.name} n'est plus disponible.`);
                    return prev;
                }
            }
        });
    };

    const handleQuantityChange = (equipmentId, value) => {
        if (value <= 0) return;
        setEquipmentQuantities(prevQuantities => ({
            ...prevQuantities,
            [equipmentId]: value,
        }));
    };

    const handleSubmit = async () => {
        if (!selectedSession) {
            setErrorMessage("You have to select a surf session!");
            return;
        }
        if (selectedEquipment.length === 0) {
            setErrorMessage("You have to select at least one equipment!");
            return;
        }

        const token = localStorage.getItem('accessToken');
        try {
            await axios.post(
                'http://localhost:8000/api/surfers/book_surf_lesson/',
                {
                    surf_session_id: selectedSession.id,
                    equipment_ids: selectedEquipment.map(eq => eq.id),
                    equipment_quantities: equipmentQuantities,
                },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
           navigate('/surfer/profile')
        } catch (error) {
            console.error("Failed to book surf lesson", error);
            setErrorMessage("Erreur lors de la réservation. Veuillez réessayer.");
        }
    };

    return (
        <div className="reserve-session-page">
            <h1 className="reserve-session-title">Book a session</h1>
            {errorMessage && <p className="reserve-session-error">{errorMessage}</p>}
            
            <div className="reserve-session-list">
                <h2 className="reserve-session-subtitle">Select a session</h2>
                <ul>
                    {sessions.map((session) => (
                        <li key={session.id}>
                            <button className={`session-btn ${selectedSession === session ? 'selected' : ''}`} onClick={() => handleSessionSelect(session)}>
                                {new Date(session.lesson_schedule.day).toLocaleDateString()} - {session.lesson_schedule.start_time} à {session.lesson_schedule.end_time}
                            </button>
                        </li>
                    ))}
                </ul>
            </div>

            {selectedSession && (
                <div className="reserve-session-details">
                    <h2 className="reserve-session-subtitle">Détails of the session</h2>
                    <div className="session-details-grid">
                        <div className="Infos">
                            <p>Date: {new Date(selectedSession.lesson_schedule.day).toLocaleDateString()}</p>
                            <p>Houre: {selectedSession.lesson_schedule.start_time} - {selectedSession.lesson_schedule.end_time}</p>
                        </div>
                        <div className="Monitor">
                            <h3>Monitor</h3>
                            <img
                                src={`http://localhost:8000${selectedSession.monitor.photo}`}
                                alt={`${selectedSession.monitor.first_name} ${selectedSession.monitor.last_name}`}
                                className="monitor-photo"
                            />
                            <strong>{selectedSession.monitor.first_name} {selectedSession.monitor.last_name}</strong>
                        </div>
                    </div>
                </div>
            )}

            {selectedSession && (
                <div className="reserve-equipments-section">
                    <h2 className="reserve-session-subtitle">Select an equipment</h2>
                    <ul className="reserve-equipments-list">
                        {equipments.map((equipment) => (
                            <li key={equipment.id} className={`equipment-card ${selectedEquipment.includes(equipment) ? 'selected' : ''}`}>
                                <div className="equipment-photo" onClick={() => handleEquipmentSelect(equipment)}>
                                    <img 
                                        src={`http://localhost:8000${equipment.photos[0]?.image}`} 
                                        alt={equipment.name} 
                                        className="equipment-image"
                                        onError={(e) => { e.target.src = PhotoEquipment; }} /* Si l'image n'est pas trouvée, utiliser l'image par défaut */
                                    />
                                </div>
                                <div className="equipment-overlay">
                                    <strong>{equipment.name}</strong><br />
                                    <strong>{equipment.rent_price}€</strong><br />
                                    <strong>Quantity: {equipment.quantity}</strong>
                                </div>
                                {selectedEquipment.includes(equipment) && (
                                    <div className="quantity-selector">
                                        <label>Quantity :</label>
                                        <input
                                            type="number"
                                            value={equipmentQuantities[equipment.id]}
                                            min="1"
                                            max={equipment.quantity}
                                            onChange={(e) => handleQuantityChange(equipment.id, parseInt(e.target.value))}
                                        />
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {selectedSession && (
                <div className="reserve-summary">
                    <h2 className="reserve-session-subtitle">Summary of your reservation</h2>
                    <p>Session: {new Date(selectedSession.lesson_schedule.day).toLocaleDateString()} - {selectedSession.lesson_schedule.start_time} à {selectedSession.lesson_schedule.end_time}</p>
                    <p>Équipments selected:</p>
                    <ul>
                        {selectedEquipment.map((equipment) => (
                            <li key={equipment.id}>{equipment.name} - Quantity: {equipmentQuantities[equipment.id]}</li>
                        ))}
                    </ul>
                    <button className="reserve-submit-btn" onClick={handleSubmit}>Confirm your reservation</button>
                </div>
            )}
        </div>
    );
};

export default ReserveSession;
