import React from 'react';
import './Footer.css'; 
import logo from '../assets/logo_innovsurf.png'; 
import { useUser } from '../context/UserContext'; 
import { Link } from 'react-router-dom';

const Footer = () => {
  const { userRole } = useUser(); 

  const surferLinks = [
    { name: 'Surf Clubs', path: '/surf-clubs' },
    { name: 'Prévisions', path: '/previsions' },
    { name: 'Forums', path: '/forums' },
    { name: 'Panier', path: '/cart' },
    { name: 'Mon Profil', path: '/surfer/profile' },
  ];

  const surfClubLinks = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Mon Profil', path: '/surfclub/profile' },
    { name: 'Contact', path: '/contact' },
  ];

  const navigationLinks = userRole === 'surfer' ? surferLinks : surfClubLinks;

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section about">
          <img src={logo} alt="InnovSurf" className="footer-logo" />
          <p>
          It is a platform that brings together surfers and surf clubs from all over Morocco.</p>
          <div className="footer-socials">
            <a href="#"><i className="fab fa-facebook"></i></a>
            <a href="#"><i className="fab fa-instagram"></i></a>
            <a href="#"><i className="fab fa-youtube"></i></a>
            <a href="#"><i className="fab fa-twitter"></i></a>
          </div>
        </div>

        <div className="footer-section links">
          <h3>Navigation</h3>
          <ul>
            {navigationLinks.map((link, index) => (
              <li key={index}>
                <Link to={link.path}>{link.name}</Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="footer-section links">
          <h3>Links</h3>
          <ul>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">Documentation</a></li>
            <li><a href="#">Guides</a></li>
            <li><a href="#">API Status</a></li>
          </ul>
        </div>

        <div className="footer-section contact">
          <h3>Contact Us</h3>
          <p><i className="fas fa-map-marker-alt"></i> 19 Abderrahim Bouabid, Rabat 10100, Morocoo</p>
          <p><i className="fas fa-envelope"></i> support@innovsurf.com</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
