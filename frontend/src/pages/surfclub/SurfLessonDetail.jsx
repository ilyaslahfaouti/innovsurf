import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './SurfLessonDetail.css'; 

const SurfLessonDetail = () => {
  const [surfLesson, setSurfLesson] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchSurfLesson = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get(`http://localhost:8000/api/surf-club/surf-lessons/${id}/`, { headers });
        setSurfLesson(response.data.SurfLesson);
      } catch (error) {
        console.error('Error fetching surf lesson details:', error);
      }
    };

    fetchSurfLesson();
  }, [id]);

  if (!surfLesson) {
    return <div>Loading...</div>;
  }

  return (
    <div className="surf-lesson-detail-container">
      <h1>Surf Lesson Details</h1>
      <div className="section surfer">
        <h2>Surfer</h2>
        <div className="info-container">
          <img 
            src={`http://localhost:8000${surfLesson.surfer.photo}`} 
            alt={`${surfLesson.surfer.firstname} ${surfLesson.surfer.lastname}`} 
            className="surfer-photo"
          />
          <div className="info">
            <p><i className="fas fa-user"></i> {surfLesson.surfer.firstname} {surfLesson.surfer.lastname}</p>
            <p><i className="fas fa-birthday-cake"></i> {surfLesson.surfer.birthday}</p>
            <p><i className="fas fa-level-up-alt"></i> Level: {surfLesson.surfer.level}</p>
          </div>
        </div>
      </div>

      <div className="section surf-session">
        <h2>Surf Session</h2>
        <div className="info-container">
          <div className="info">
            <div className="lesson-schedule">
              <p><i className="fas fa-calendar-day"></i> {surfLesson.LessonSchedule.day}</p>
              <p><i className="fas fa-clock"></i> Start Time: {surfLesson.LessonSchedule.start_time}</p>
              <p><i className="fas fa-clock"></i> End Time: {surfLesson.LessonSchedule.end_time}</p>
            </div>
          </div>
          <div className="monitor">
           
            <img 
            src={`http://localhost:8000${surfLesson.monitor.photo}`} 
            className="surfer-photo"
          />

            <p><i className="fas fa-user"></i><strong> Monitor</strong> {surfLesson.monitor.first_name} {surfLesson.monitor.last_name}</p>
          </div>
        </div>
      </div>

      <div className="section equipment">
        <h2>Equipment</h2>
        <ul className="equipment-list">
          {surfLesson.equipment_selection.length > 0 ? (
            surfLesson.equipment_selection.map(equipment => (
              <li key={equipment.id}>
                <i className="fas fa-tools"></i> {equipment.name} - State: {equipment.state} (Quantity: {equipment.quantity})
              </li>
            ))
          ) : (
            <li>No equipment selected.</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default SurfLessonDetail;
