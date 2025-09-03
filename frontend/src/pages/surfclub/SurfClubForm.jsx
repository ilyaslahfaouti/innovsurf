import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SurfClubForm.css'; 
import logoImage from '../../assets/logo_innovsurf.png'; 

const SurfClubForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [adress, setAdress] = useState('');
  const [phone_number, setPhoneNumber] = useState('');
  const [surf_spot, setSurfSpot] = useState('');
  const [logo, setLogo] = useState(null);
  const [surfSpots, setSurfSpots] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/api/surf-spots/')
      .then(response => setSurfSpots(response.data))
      .catch(error => console.error('Error fetching surf spots:', error));
  }, []);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'logo') {
      setLogo(files[0]); // Set file object
    } else {
      switch (name) {
        case 'email':
          setEmail(value);
          break;
        case 'password':
          setPassword(value);
          break;
        case 'confirmPassword':
          setConfirmPassword(value);
          break;
        case 'name':
          setName(value);
          break;
        case 'adress':
          setAdress(value);
          break;
        case 'phone_number':
          setPhoneNumber(value);
          break;
        case 'surf_spot':
          setSurfSpot(value);
          break;
        default:
          break;
      }
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('confirmPassword', confirmPassword);
    formData.append('name', name);
    formData.append('address', adress);
    formData.append('phone_number', phone_number);
    formData.append('surf_spot', surf_spot);
    formData.append('role', "surfclub");
    if (logo) {
      formData.append('logo', logo);
    }
    formData.append('role', 'surfclub');

    try {
      await axios.post('http://localhost:8000/api/user/register/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      navigate('/login');
    } catch (error) {
      console.error('Error registering:', error);
    }
  };

  return (
    <div id="register-container">
      <div id="register-form">
        <div id="register-logo">
          <img src={logoImage} alt="Logo" />
        </div>
        <h2>Register as Surf Club</h2>
        <form onSubmit={handleRegister}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">Club Name</label>
              <input
                type="text"
                name="name"
                id="name"
                placeholder="Enter club name"
                value={name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                name="email"
                id="email"
                placeholder="Enter email"
                value={email}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="adress">Address</label>
              <input
                type="text"
                name="adress"
                id="adress"
                placeholder="Enter address"
                value={adress}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="phone_number">Phone Number</label>
              <input
                type="number"
                name="phone_number"
                id="phone_number"
                placeholder="Enter phone number"
                value={phone_number}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="surf_spot">Surf Spot</label>
              <select
                name="surf_spot"
                id="surf_spot"
                value={surf_spot}
                onChange={handleChange}
                required
              >
                <option value="">Select Surf Spot</option>
                {surfSpots.map(spot => (
                  <option key={spot.id} value={spot.id}>{spot.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="logo">Club Logo</label>
              <input
                type="file"
                name="logo"
                id="logo"
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                name="password"
                id="password"
                placeholder="Enter password"
                value={password}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                id="confirmPassword"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <button type="submit" id="register-btn">Register as Surf Club</button>
        </form>
      </div>
    </div>
  );
};

export default SurfClubForm;
