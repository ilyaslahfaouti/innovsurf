import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import './Login.css';
import logo from '../../assets/logo_innovsurf.png'; 

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setUserRole } = useUser();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.post('http://localhost:8000/api/user/login/', { email, password });
      
      const user = response.data.user;
      const accessToken = response.data.access;

      let role = null;
      if (user.is_surfer == 1) {
        role = 'surfer';
        localStorage.setItem('surfer', JSON.stringify(response.data.surfer));
      } else if (user.is_surfclub == 1) {
        role = 'surfclub';
        localStorage.setItem('surfclub', JSON.stringify(response.data.surfclub));
      }

      setUserRole(role);
      localStorage.setItem('userRole', role);
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('user', JSON.stringify(user)); 

      navigate('/');
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  return (
    <div id="login-container">
      <div id="login-card">
        <div id="login-logo">
          <img src={logo} alt="Logo" />
        </div>
        <h2 id="login-title">Sign in</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <div className="input-group">
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
                required
              />
              <span className="input-group-icon"><i className="fas fa-envelope"></i></span>
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-group">
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
              />
              <span className="input-group-icon"><i className="fas fa-eye"></i></span>
            </div>
          </div>
          <div className="form-group" id="remember-me-group">
           
            <a href="#" id="welcome">Welcome back !</a>
          </div>
          <button type="submit" id="login-btn">Sign in</button>
        </form>
        <div id="register-link">
          Don't have an account? <a href="/register">Register here</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
