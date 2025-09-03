import React, { useState } from 'react';
import SurferForm from '../surfer/SurferForm';
import SurfClubForm from '../surfclub/SurfClubForm';
import './Register.css';
import surfclub from '../../assets/surfclub.jpg';
import surfer from '../../assets/surfer.jpg';

const Register = () => {
  const [role, setRole] = useState('');

  return (
    <div id="register-container">
      {!role && (
        <div className="row" id="role-selection">
          <div className="col-md-6">
            <div
              className="card register-card"
              onClick={() => setRole('surfer')}
            >
              <img
                src={surfer}
                className="card-img-top register-card-img-top"
                alt="Surfer"
              />
              <div className="card-body text-center">
                <h5 className="card-title register-card-title">I'M A SURFER</h5>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div
              className="card register-card"
              onClick={() => setRole('surfclub')} 
            >
              <img
                src={surfclub}
                className="card-img-top register-card-img-top"
                alt="Surf Club"
              />
              <div className="card-body text-center">
                <h5 className="card-title register-card-title">I'M A SURF CLUB</h5>
              </div>
            </div>
          </div>
        </div>
      )}

      {role === 'surfer' && <SurferForm />}
      {role === 'surfclub' && <SurfClubForm />}
    </div>
  );
};

export default Register;
