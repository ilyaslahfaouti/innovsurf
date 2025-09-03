import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './SurfSessions.css'; 

const SurfSessions = () => {
  const [surfSessions, setSurfSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSurfSessions = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get('http://localhost:8000/api/surf-club/surf-sessions/', { headers });
      setSurfSessions(response.data.surf_sessions);
    } catch (err) {
      setError('Error fetching surf sessions.');
      console.error('Error fetching surf sessions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this session?')) {
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { Authorization: `Bearer ${token}` };
        await axios.delete(`http://localhost:8000/api/surf-club/surf-session/${id}/`, { headers });
        // Refresh the list after deletion
        fetchSurfSessions();
      } catch (err) {
        alert('Error deleting surf session.');
        console.error('Error deleting surf session:', err);
      }
    }
  };

  useEffect(() => {
    fetchSurfSessions();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="surf-sessions-container">
      <div className="header">
        <div> <h1>Surf Sessions</h1></div>
       <div>      <Link to="/dashboard/surf-session/create" className="session-add-link">
          <i className="fas fa-plus"></i> Create New Session
        </Link></div>
  
      </div>
      {surfSessions.length > 0 ? (
        <ul className="surf-sessions-list">
          {surfSessions.map(session => (
            <li key={session.id} className="surf-session-item">
              <div className="session-details">
                <div className="session-info">
              
                  <p><i className="fas fa-calendar-alt"></i> <strong></strong> {session.lesson_schedule.day}</p>
                  <p><i className="fas fa-clock"></i> <strong>Start Time:</strong> {session.lesson_schedule.start_time}</p>
                  <p><i className="fas fa-clock"></i> <strong>End Time:</strong> {session.lesson_schedule.end_time}</p>
                </div>
                <div className="monitor-info">
                  <img 
                    src={`http://localhost:8000${session.monitor.photo}`} 
                    alt={`${session.monitor.first_name} ${session.monitor.last_name}`} 
                    className="monitor-photo" 
                  />
                  <p><i className="fas fa-user"></i> {session.monitor.first_name} {session.monitor.last_name}</p>
                </div>
              </div>
              <div className="session-actions">
                <Link to={`/dashboard/surf-session/${session.id}/edit`} className="edit-link">
                  <i className="fas fa-edit"></i>
                </Link>
                <button onClick={() => handleDelete(session.id)} className="delete-button">
                  <i className="fas fa-trash"></i>
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No surf sessions available.</p>
      )}
    </div>
  );
};

export default SurfSessions;
