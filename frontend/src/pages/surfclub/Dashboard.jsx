import React, { useEffect, useState } from 'react';
import { Link, Outlet } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [forecast, setForecast] = useState(null);

  useEffect(()=>{
    const token = localStorage.getItem('accessToken');
    if (!token) return;
    fetch('http://localhost:8000/api/ai/demand-forecast/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(r=>r.json())
    .then(setForecast)
    .catch(()=>{});
  },[]);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="dashboard-container">
      <button className="hamburger-btn" onClick={toggleSidebar}>
        <i className="fas fa-bars"></i>
      </button>

      <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <nav className="sidebar-nav">
          <ul>
            <li>
              <Link to="/">
                <i className="fas fa-home"></i> Home
              </Link>
            </li>
            <li>
              <Link to="/dashboard/statistics">
                <i className="fas fa-home"></i> Statistics
              </Link>
            </li>
            <li>
              <Link to="/dashboard/monitors">
                <i className="fas fa-users"></i> Monitors
              </Link>
            </li>
            <li>
              <Link to="/dashboard/equipments">
                <i className="fas fa-box"></i> Equipements
              </Link>
            </li>
            <li>
              <Link to="/dashboard/surf-session">
                <i className="fas fa-calendar-alt"></i> Surf Session
              </Link>
            </li>
            <li>
              <Link to="/dashboard/lesson-schedule">
                <i className="fas fa-calendar-check"></i> Lesson Schedule
              </Link>
            </li>
            <li>
              <Link to="/dashboard/surf-lesson">
                <i className="fas fa-water"></i> Surf Lesson
              </Link>
            </li>
            <li>
              <Link to="/dashboard/orders">
                <i className="fas fa-shopping-cart"></i> Orders
              </Link>
            </li>
          </ul>
        </nav>
      </aside>
      <main className="content">
        {forecast && (
          <div className="card" style={{padding:'16px', marginBottom:'16px'}}>
            <h3 style={{marginTop:0}}>Prévision de demande (IA)</h3>
            <p style={{margin:'4px 0'}}>Club: <b>{forecast.club}</b></p>
            <div style={{display:'flex', gap:'16px', flexWrap:'wrap'}}>
              <div className="badge-primary">Cette semaine: {forecast.demand_forecast?.this_week}</div>
              <div className="badge-primary">Semaine prochaine: {forecast.demand_forecast?.next_week}</div>
              <div className="badge-primary">Tendance: {forecast.demand_forecast?.trend}</div>
              <div className="badge-primary">Prix suggéré: {forecast.suggested_price} €</div>
            </div>
            {Array.isArray(forecast.demand_forecast?.history) && (
              <div style={{marginTop:'12px'}}>
                <small>Historique (semaines):</small>
                {(() => {
                  const data = forecast.demand_forecast.history;
                  const w = 160, h = 60, pad = 4;
                  const max = Math.max(...data), min = Math.min(...data);
                  const rng = Math.max(1, max - min);
                  const step = (w - pad*2) / (data.length - 1);
                  const pts = data.map((v,i)=>{
                    const x = pad + i*step;
                    const y = pad + (h - pad*2) - ((v - min)/rng)*(h - pad*2);
                    return `${x},${y}`;
                  }).join(' ');
                  return (
                    <svg width={w} height={h} style={{display:'block', marginTop:'6px'}}>
                      <defs>
                        <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.4" />
                          <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                      <polyline fill="none" stroke="var(--color-primary)" strokeWidth="2" points={pts} />
                      <polygon fill="url(#g1)" points={`${pts} ${w-pad},${h-pad} ${pad},${h-pad}`} />
                    </svg>
                  );
                })()}
              </div>
            )}
            <small>Généré le {new Date(forecast.generated_at).toLocaleString()}</small>
          </div>
        )}
        <Outlet /> 
      </main>
    </div>
  );
};

export default Dashboard;
