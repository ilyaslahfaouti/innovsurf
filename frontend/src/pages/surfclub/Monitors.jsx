import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Monitors.css'; // Assurez-vous d'importer le fichier CSS
import defaultMonitorImage from '../../assets/monitor.jpg'; // Importez l'image par défaut

const Monitors = () => {
  const [monitors, setMonitors] = useState([]);

  // Fonction pour récupérer le token d'authentification
  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    const fetchMonitors = async () => {
      try {
        const token = getAuthToken();
        const headers = {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        };
        const response = await axios.get('http://localhost:8000/api/surf-club/monitors/', { headers });
        setMonitors(response.data.monitors);
      } catch (error) {
        console.error('Error fetching monitors:', error);
      }
    };

    fetchMonitors();
  }, []);

  // Fonction pour supprimer un moniteur avec confirmation
  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this monitor?')) {
      try {
        const token = getAuthToken();
        const headers = {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        };
        await axios.delete(`http://localhost:8000/api/surf-club/monitor/${id}/`, { headers });
        // Recharger la liste des moniteurs après suppression
        setMonitors(prev => prev.filter(monitor => monitor.id !== id));
      } catch (error) {
        console.error('Error deleting monitor:', error);
      }
    }
  };

  return (
    <div className="monitors-container">
       <div className='header'>
      <h1>Monitors</h1>
      <Link to="/dashboard/monitor/create" className="add-link">Add New Monitor</Link>
      </div>
      <ul className="monitors-list">
        {monitors.map(monitor => (
          <li key={monitor.id} className="monitor-item">
            <div className="monitor-image">
              <img
                src={monitor.photo ? `http://localhost:8000${monitor.photo}` : defaultMonitorImage}
                alt={`${monitor.first_name} ${monitor.last_name}`}
                className="monitor-photo"
              />
            </div>
            <div className="monitor-content">
              <div className="monitor-info">
                <div className="monitor-detail">
                  <i className="fas fa-user"></i>
                  <span>{monitor.first_name} {monitor.last_name}</span>
                </div>
                <div className="monitor-detail">
                  <i className="fas fa-birthday-cake"></i>
                  <span>{monitor.birthday}</span>
                </div>
                <div className="monitor-detail">
                  <i className={`fas ${monitor.active ? 'fa-check-circle' : 'fa-times-circle'}`}></i>
                  <span>{monitor.active ? 'Active' : 'Inactive'}</span>
                </div>
              </div>
              <div className="monitor-actions">
                <Link to={`/dashboard/monitor/${monitor.id}/edit`} className="action-link">
                  <i className="fas fa-edit"></i>
                </Link>
                <button onClick={() => handleDelete(monitor.id)} className="action-link">
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

export default Monitors;
