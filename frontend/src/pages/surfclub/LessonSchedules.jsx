import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './LessonSchedules.css'; 

const LessonSchedules = () => {
  const [lessonSchedules, setLessonSchedules] = useState([]);

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    const fetchLessonSchedules = async () => {
      try {
        const token = getAuthToken();
        const headers = {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        };
        const response = await axios.get('http://localhost:8000/api/surf-club/lesson-schedules/', { headers });
        setLessonSchedules(response.data.LessonSchedules);

      } catch (error) {
        console.error('Error fetching lesson schedules:', error);
      }
    };

    fetchLessonSchedules();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this schedule?')) {
      return;
    }
    try {
      const token = getAuthToken();
      const headers = {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      };
      await axios.delete(`http://localhost:8000/api/surf-club/lesson-schedule/${id}/`, { headers });
      setLessonSchedules(lessonSchedules.filter(schedule => schedule.id !== id));
    } catch (error) {
      console.error('Error deleting lesson schedule:', error);
    }
  };

  return (
    <div className="lesson-schedules-container">
      <div className="header">
        <h1>Lesson Schedules</h1>
        <Link to="/dashboard/lesson-schedule/create" className="lesson-add-link">Add New Schedule</Link>
      </div>
      <ul className="lesson-schedules-list">
        {lessonSchedules.map(schedule => (
          <li key={schedule.id} className="lesson-schedule-item">
            <div className="schedule-info">
              <p><i className="fas fa-calendar-alt"></i> {schedule.day}</p>
              <p><i className="fas fa-clock"></i> <strong>Start Time:</strong> {schedule.start_time}</p>
              <p><i className="fas fa-clock"></i> <strong>End Time:</strong> {schedule.end_time}</p>
            </div>
            <div className="schedule-actions">
              <Link to={`/dashboard/lesson-schedule/${schedule.id}/edit`} className="edit-link">
                <i className="fas fa-edit"></i>
              </Link>
              <button onClick={() => handleDelete(schedule.id)} className="delete-button">
                <i className="fas fa-trash"></i>
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LessonSchedules;
