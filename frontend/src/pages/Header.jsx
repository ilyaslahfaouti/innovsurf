import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaShoppingCart } from 'react-icons/fa'; 
import './Header.css';
import logo from '../assets/logo_innovsurf.png';

const Header = ({ userRole, setUserRole }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0); 
  const [firstName, setFirstName] = useState(''); 
  const navigate = useNavigate();

  useEffect(() => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    setCartCount(cart.reduce((total, item) => total + item.quantity, 0));

    if (userRole === 'surfer') {
      const surfer = JSON.parse(localStorage.getItem('surfer')) || {};
      setFirstName(surfer.firstname || 'Surfer');
    } else if (userRole === 'surfclub') {
      const surfclub = JSON.parse(localStorage.getItem('surfclub')) || {};
      setFirstName(surfclub.name || 'Club');
    }
  }, [userRole]);

  const handleLogout = () => {
    localStorage.clear();
    setUserRole(null);
    try { window.dispatchEvent(new CustomEvent('app:logout')); } catch (e) {}
    navigate('/login');
  };

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header id="header">
      <nav className="navbar navbar-expand-lg navbar-light bg-light" id="navbar">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/" id="navbar-brand">
            <img src={logo} alt="Logo" className="logo" />
          </Link>

          <button className="navbar-toggler" type="button" onClick={toggleMenu}>
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className={`collapse navbar-collapse ${menuOpen ? 'show' : ''}`} id="navbarNav">
            <ul className="navbar-nav">
              {userRole === 'surfer' && (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/surf-clubs">Surf Clubs</Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/previsions">Forecast</Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/forums">Forums</Link>
                  </li>
                </>
              )}
              {userRole === 'surfclub' && (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/dashboard">Dashboard</Link>
                  </li>
                </>
              )}
              <li className="nav-item">
                <Link className="nav-link" to="/contact">Contact</Link>
              </li>

              {userRole && (
                <li className="nav-item">
                  <Link className="nav-link" to={userRole === 'surfer' ? "/surfer/profile" : "/surfclub/profile"}>
                    <FaUser className="me-2" />
                    {firstName}
                  </Link>
                </li>
              )}
              {userRole === 'surfer' && (
                <li className="nav-item">
                  <Link className="nav-link" to="/cart">
                    <FaShoppingCart className="me-2" />
                    {cartCount > 0 && <span className="badge badge-danger">{cartCount}</span>}
                  </Link>
                </li>
              )}
              <li className="nav-item">
                {!userRole ? (
                  <Link className="btn btn-p nav-link" to="/login">Login</Link>
                ) : (
                  <button className="btn btn-d nav-link" onClick={handleLogout}>Logout</button>
                )}
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
