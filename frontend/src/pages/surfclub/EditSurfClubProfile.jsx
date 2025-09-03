import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './EditSurfClubProfile.css'; 

const EditSurfClubProfile = () => {
    const [formData, setFormData] = useState({
        user: {
            email: '',
            address: '',
            phone_number: '',
            password: '',
        },
        surf_club: {
            name: '',
            surf_spot: '',
        }
    });
    const [changePassword, setChangePassword] = useState(false);
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [logoFile, setLogoFile] = useState(null); 
    const [formErrors, setFormErrors] = useState({});
    const [surfSpots, setSurfSpots] = useState([]);
    const navigate = useNavigate();
    const token = localStorage.getItem('accessToken');

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/surf-club/profile/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                setFormData({
                    user: response.data.user,
                    surf_club: response.data['surf-club'],
                });
            } catch (error) {
                console.error("Failed to fetch profile", error);
            }
        };

        const fetchSurfSpots = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/surf-spots/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                setSurfSpots(response.data);
            } catch (error) {
                console.error("Failed to fetch surf spots", error);
            }
        };

        fetchProfile();
        fetchSurfSpots();
    }, [token]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        const [section, field] = name.split('.');
        setFormData(prevData => ({
            ...prevData,
            [section]: {
                ...prevData[section],
                [field]: value
            }
        }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setLogoFile(file); // Stocker le fichier dans un état séparé
        }
    };

    const handlePasswordChange = (e) => {
        setChangePassword(e.target.checked);
        if (!e.target.checked) {
            setFormData(prevData => ({
                ...prevData,
                user: {
                    ...prevData.user,
                    password: '' 
                }
            }));
            setPasswordConfirm(''); 
        }
    };

    const handlePasswordConfirmChange = (e) => {
        setPasswordConfirm(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errors = {};
        if (changePassword && formData.user.password !== passwordConfirm) {
            errors.passwordConfirm = 'Passwords do not match';
        }
        setFormErrors(errors);

        if (Object.keys(errors).length === 0) {
            const dataToSend = new FormData();

            // Préparation des données utilisateur
            const userData = {
                email: formData.user.email,
                address: formData.user.address,
                phone_number: formData.user.phone_number,
            };

            if (changePassword) {
                userData.password = formData.user.password;
            }

            dataToSend.append('user', JSON.stringify(userData));
            dataToSend.append('surf_club', JSON.stringify({
                id: formData.surf_club.id,
                name: formData.surf_club.name,
                surf_spot: formData.surf_club.surf_spot
            }));

            if (logoFile) {
                dataToSend.append('logo', logoFile);
            }

            try {
                await axios.put('http://localhost:8000/api/surf-club/profile/update/', dataToSend, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });
                navigate('/surfclub/profile');
            } catch (error) {
                console.error("Failed to update profile", error.response ? error.response.data : error.message);
            }
        }
    };

    return (
        <div className="edit-surfclub-profile">
            <h1>Edit Surf Club Profile</h1>
            <form onSubmit={handleSubmit} className="profile-form">
                <div className="form-section">
                    <h2>Club Information</h2>
                    <label>
                        Name:
                        <input
                            type="text"
                            name="surf_club.name"
                            value={formData.surf_club.name || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Logo:
                        <input
                            type="file"
                            name="surf_club.logo"
                            onChange={handleFileChange}
                        />
                    </label>
                    <label>
                        Surf Spot:
                        <select
                            name="surf_club.surf_spot"
                            value={formData.surf_club.surf_spot || ''}
                            onChange={handleChange}
                        >
                            <option value="">Select a Surf Spot</option>
                            {surfSpots.map(spot => (
                                <option key={spot.id} value={spot.id}>
                                    {spot.name}
                                </option>
                            ))}
                        </select>
                    </label>
                </div>
                <div className="form-section">
                    <h2>User Information</h2>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="user.email"
                            value={formData.user.email || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Address:
                        <input
                            type="text"
                            name="user.address"
                            value={formData.user.address || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Phone Number:
                        <input
                            type="text"
                            name="user.phone_number"
                            value={formData.user.phone_number || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label className="checkbox-label">
                        <input
                            type="checkbox"
                            checked={changePassword}
                            onChange={handlePasswordChange}
                        />
                        Change Password
                    </label>
                    {changePassword && (
                        <>
                            <label>
                                New Password:
                                <input
                                    type="password"
                                    name="user.password"
                                    onChange={handleChange}
                                />
                            </label>
                            <label>
                                Confirm New Password:
                                <input
                                    type="password"
                                    value={passwordConfirm}
                                    onChange={handlePasswordConfirmChange}
                                />
                                {formErrors.passwordConfirm && <p className="error">{formErrors.passwordConfirm}</p>}
                            </label>
                        </>
                    )}
                </div>
                <button type="submit" className="submit-button">Save Changes</button>
            </form>
        </div>
    );
};

export default EditSurfClubProfile;
