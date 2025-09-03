import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './LessonScheduleForm.css'; 

const LessonScheduleForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lessonSchedule, setLessonSchedule] = useState({
    surf_club: '',
    start_time: '',
    end_time: '',
    day: '',  
  });
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    if (id) {
      const fetchLessonSchedule = async () => {
        try {
          const token = getAuthToken();
          const headers = {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          };
          const response = await axios.get(`http://localhost:8000/api/surf-club/lesson-schedule/${id}/`, { headers });
          setLessonSchedule(response.data);
          setIsEditing(true);
        } catch (error) {
          console.error('Error fetching lesson schedule:', error);
          setError('Error fetching lesson schedule');
        }
      };

      fetchLessonSchedule();
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLessonSchedule(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = getAuthToken();
      const headers = {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      };

      if (isEditing) {
        await axios.put(`http://localhost:8000/api/surf-club/lesson-schedule/${id}/`, lessonSchedule, { headers });
      } else {
        await axios.post('http://localhost:8000/api/surf-club/add-lesson-schedule/', lessonSchedule, { headers });
      }
      
      navigate('/dashboard/lesson-schedule');
    } catch (error) {
      console.error('Error submitting lesson schedule:', error);
      setError('Error submitting lesson schedule');
    }
  };

  return (
    <div className="form-container">
      <h1>{isEditing ? 'Edit Lesson Schedule' : 'Add Lesson Schedule'}</h1>
      <form onSubmit={handleSubmit} className="form-content">
        <div className="form-group">
          <label htmlFor="day">Day</label>
          <input
            type="date"
            id="day"
            name="day"
            value={lessonSchedule.day}
            onChange={handleChange}
            required
            className="form-control"
          />
        </div>
        <div className="form-group">
          <label htmlFor="start_time">Start Time</label>
          <input
            type="time"
            id="start_time"
            name="start_time"
            value={lessonSchedule.start_time}
            onChange={handleChange}
            required
            className="form-control"
          />
        </div>
        <div className="form-group">
          <label htmlFor="end_time">End Time</label>
          <input
            type="time"
            id="end_time"
            name="end_time"
            value={lessonSchedule.end_time}
            onChange={handleChange}
            required
            className="form-control"
          />
        </div>
        <button type="submit" className="submit-button">{isEditing ? 'Update Schedule' : 'Add Schedule'}</button>
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
};

export default LessonScheduleForm;
