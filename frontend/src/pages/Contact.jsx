import React, { useState } from 'react';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    message: ''
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/contact/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setResponseMessage('Message sent successfully!');
        setFormData({
          first_name: '',
          last_name: '',
          email: '',
          message: ''
        });
      } else {
        setResponseMessage('Error sending message.');
      }
    } catch (error) {
      setResponseMessage('An error occurred.');
    }
  };

  return (
    <div className="contact-page">
      <div className="contact-page-header-section">
        <div className="contact-page-overlay-text">
          <h1>Innov' discuss</h1>
          <p>
          We are here to address your questions and concerns</p>
        </div>
        <div className="contact-page-info-boxes">
          <div className="contact-page-info-box">
            <i className="fas fa-map-marker-alt"></i>
            <h5>Physical Address</h5>
            <p>19 Abderrahim Bouabid,<br /> Rabat 10100, Morocoo</p>
          </div>
          <div className="contact-page-info-box">
            <i className="fas fa-envelope"></i>
            <h5>Email Address</h5>
            <p>support@innovsurf.com</p>
          </div>
          <div className="contact-page-info-box">
            <i className="fas fa-phone"></i>
            <h5>Phone Numbers</h5>
            <p>+212 6 10 75 02 59<br />+212 7 85 23 12 90</p>
          </div>
        </div>
      </div>

      <div className="contact-page-form-section">
        <h2>Send Us Your Message</h2>
        <p>
        Please fill out the form below to contact us.</p>
        <div className="contact-page-form-container">
          <div className="contact-page-image">
            <img src={require('../assets/contact2.jpg')} alt="Contact Illustration" />
          </div>
          <form className="contact-page-form" onSubmit={handleSubmit}>
            <div className="contact-page-form-group">
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="contact-page-form-group">
              <input
                type="email"
                name="email"
                placeholder="E-mail"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="contact-page-form-group">
              <textarea
                name="message"
                placeholder="Comment or message"
                value={formData.message}
                onChange={handleChange}
                required
              ></textarea>
            </div>
            <button type="submit" className="contact-page-submit-button">
              Send Message
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Contact;
