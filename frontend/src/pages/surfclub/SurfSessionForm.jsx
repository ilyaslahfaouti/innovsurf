import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './SurfSessionForm.css'; 

const SurfSessionForm = () => {
  const [lessonSchedules, setLessonSchedules] = useState([]);
  const [monitors, setMonitors] = useState([]);
  const [formData, setFormData] = useState({
    lesson_schedule: '',
    monitor: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams(); 
  const navigate = useNavigate();
  const isEdit = !!id; 

  useEffect(() => {
    const fetchLessonSchedules = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get('http://localhost:8000/api/surf-club/lesson-schedules/', { headers });
        setLessonSchedules(response.data.LessonSchedules);
      } catch (err) {
        setError('Error fetching lesson schedules.');
        console.error('Error fetching lesson schedules:', err);
      }
    };

    const fetchMonitors = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get('http://localhost:8000/api/surf-club/monitors-dispo/', { headers });
        setMonitors(response.data.monitors);
      } catch (err) {
        setError('Error fetching monitors.');
        console.error('Error fetching monitors:', err);
      }
    };

    const fetchDataForEdit = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get(`http://localhost:8000/api/surf-club/surf-sessions/${id}/`, { headers });
        setFormData({
          lesson_schedule: response.data.SurfSession.lesson_schedule.id,
          monitor: response.data.SurfSession.monitor?.id || '' 
        });
        setLoading(false); 
      } catch (err) {
        setError('Error fetching surf session details.');
        console.error('Error fetching surf session details:', err);
      }
    };

    const fetchData = async () => {
      await fetchLessonSchedules();
      await fetchMonitors();
      if (isEdit) {
        await fetchDataForEdit();
      } else {
        setLoading(false); 
      }
    };

    fetchData();
  }, [id, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('accessToken');
      const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };
      const url = isEdit
        ? `http://localhost:8000/api/surf-club/surf-session/${id}/`
        : 'http://localhost:8000/api/surf-club/add-surf-session/';

      const method = isEdit ? 'PUT' : 'POST';
      await axios({
        method,
        url,
        headers,
        data: formData
      });

      navigate('surf-session'); 
    } catch (err) {
      setError('Error submitting the form.');
      console.error('Error submitting the form:', err);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="form-container">
      <h1>{isEdit ? 'Edit Surf Session' : 'Create Surf Session'}</h1>
      <form onSubmit={handleSubmit} className="form-content">
        <div className="form-group">
          <label htmlFor="lesson_schedule">Lesson Schedule</label>
          <select
            id="lesson_schedule"
            name="lesson_schedule"
            value={formData.lesson_schedule}
            onChange={handleChange}
            required
            className="form-control"
          >
            <option value="">Select a lesson schedule</option>
            {lessonSchedules.map(schedule => (
              <option key={schedule.id} value={schedule.id}>
                {schedule.day} - {schedule.start_time} to {schedule.end_time}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="monitor">Monitor</label>
          <select
            id="monitor"
            name="monitor"
            value={formData.monitor}
            onChange={handleChange}
            className="form-control"
            required={!isEdit} 
          >
            <option value="">Select a monitor</option>
            {monitors.map(monitor => (
              <option key={monitor.id} value={monitor.id}>
                {monitor.first_name} {monitor.last_name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="submit-button">{isEdit ? 'Update' : 'Create'}</button>
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
};

export default SurfSessionForm;
