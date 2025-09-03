import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './EditSurferProfile.css';

const EditSurferProfile = () => {
    const [formData, setFormData] = useState({
        user: {},
        surfer: {}
    });
    const [passwordChange, setPasswordChange] = useState(false);
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [newPhoto, setNewPhoto] = useState(null); // Stocker le fichier photo
    const [formErrors, setFormErrors] = useState({});
    const navigate = useNavigate();
    const token = localStorage.getItem('accessToken');

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/surfer/profile/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                setFormData({
                    user: response.data.user,
                    surfer: response.data.surfer
                });
            } catch (error) {
                console.error("Failed to fetch profile", error);
            }
        };

        fetchProfile();
    }, [token]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name.split('.')[0]]: {
                ...prevData[name.split('.')[0]],
                [name.split('.')[1]]: value
            }
        }));
    };

    const handlePhotoChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setNewPhoto(file); // Stocker le nouveau fichier photo sélectionné
        }
    };

    const handlePasswordChangeToggle = (e) => {
        setPasswordChange(e.target.checked);
    };

    const handlePasswordConfirmChange = (e) => {
        setPasswordConfirm(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errors = {};
        if (passwordChange && formData.user.password !== passwordConfirm) {
            errors.passwordConfirm = 'Passwords do not match';
        }
        setFormErrors(errors);

        if (Object.keys(errors).length === 0) {
            const userData = { ...formData.user };
            if (!passwordChange) {
                delete userData.password;
            }

            const dataToSubmit = new FormData();
            dataToSubmit.append('user', JSON.stringify(userData));
            dataToSubmit.append('surfer', JSON.stringify(formData.surfer));

            if (newPhoto) {
                dataToSubmit.append('photo', newPhoto); // Ajouter la nouvelle photo uniquement si sélectionnée
            }

            try {
                await axios.put('http://localhost:8000/api/surfer/profile/update/', dataToSubmit, {
                    headers: { 
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });
                navigate('/surfer/profile');
            } catch (error) {
                console.error("Failed to update profile", error);
            }
        }
    };

    return (
        <div className="edit-surfer-profile">
            <h1 className="edit-title">Edit Surfer Profile</h1>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
                <div className="form-section">
                    <h2>Surfer Information</h2>
                    <label>
                        First Name:
                        <input
                            type="text"
                            name="surfer.firstname"
                            value={formData.surfer.firstname || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Last Name:
                        <input
                            type="text"
                            name="surfer.lastname"
                            value={formData.surfer.lastname || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Birthday:
                        <input
                            type="date"
                            name="surfer.birthday"
                            value={formData.surfer.birthday || ''}
                            onChange={handleChange}
                        />
                    </label>
                    <label>
                        Level:
                        <select
                            name="surfer.level"
                            value={formData.surfer.level || ''}
                            onChange={handleChange}
                        >
                            <option value="">Select level</option>
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </label>
                    <label>
                        Profile Photo:
                        <input
                            type="file"
                            name="photo"
                            accept="image/*"
                            onChange={handlePhotoChange}
                        />
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
                    <label>
                        Change Password:
                        <input
                            type="checkbox"
                            checked={passwordChange}
                            onChange={handlePasswordChangeToggle}
                        />
                    </label>
                    {passwordChange && (
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
                                {formErrors.passwordConfirm && <p>{formErrors.passwordConfirm}</p>}
                            </label>
                        </>
                    )}
                </div>
                <button type="submit" className="save-button">Save Changes</button>
            </form>
        </div>
    );
};

export default EditSurferProfile;
