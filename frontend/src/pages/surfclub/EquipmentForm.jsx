import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import DragAndDrop from './DragAndDrop'; 
import './EquipmentForm.css'; 

const EquipmentForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [equipment, setEquipment] = useState({
    name: '',
    description: '',
    size: '',
    state: '',
    material_type: 'rent',
    equipment_type: '',
    sale_price: '',
    rent_price: '',
    quantity: 0, 
    is_rent: false,
    is_sell: false,
    photos: []  
  });
  const [previousMaterialType, setPreviousMaterialType] = useState('rent'); // Store the previous material_type
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');
  const [EquipmentTypes, setEquipmentTypes] = useState([]);

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  const fetchEquipmentTypes = async () => {
    try {
      const token = getAuthToken();
      const headers = {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      };
      const response = await axios.get('http://localhost:8000/api/surf-club/equipment-types/', { headers });
      setEquipmentTypes(response.data.equipment_types);
    } catch (error) {
      console.error('Error fetching equipment types:', error);
      setError('Error fetching equipment types');
    }
  };

  useEffect(() => {
    fetchEquipmentTypes();
    if (id) {
      const fetchEquipment = async () => {
        try {
          const token = getAuthToken();
          const headers = {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          };
          const response = await axios.get(`http://localhost:8000/api/surf-club/equipment/${id}/`, { headers });
          const equipmentData = {
            ...response.data,
            photos: response.data.photos || []  
          };
          setEquipment(equipmentData);
          setPreviousMaterialType(equipmentData.material_type); 
          setIsEditing(true);
        } catch (error) {
          console.error('Error fetching equipment:', error);
          setError('Error fetching equipment');
        }
      };
      fetchEquipment();
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEquipment(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleMaterialTypeChange = (e) => {
    const value = e.target.value;
    if (value !== previousMaterialType) {
      setEquipment(prev => ({
        ...prev,
        material_type: value,
        is_rent: false, 
        is_sell: false, 
        rent_price: '',
        sale_price: ''
      }));
      setPreviousMaterialType(value); 
    }
  };

  const handleFilesAdded = (files) => {
    setEquipment(prev => ({
      ...prev,
      photos: [...prev.photos, ...files]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = getAuthToken();
      const headers = {
        "Authorization": `Bearer ${token}`
      };
      const formData = new FormData();
      Object.keys(equipment).forEach(key => {
        if (key !== 'photos' && equipment[key] !== null && equipment[key] !== '') {
          formData.append(key, equipment[key]);
        }
      });
      if (Array.isArray(equipment.photos)) {
        equipment.photos.forEach(photo => {
          formData.append('photos', photo);
        });
      }
      if (isEditing) {
        await axios.put(`http://localhost:8000/api/surf-club/equipment/${id}/`, formData, { headers });
      } else {
        await axios.post('http://localhost:8000/api/surf-club/add-equipment/', formData, { headers });
      }
      navigate('/dashboard/equipments');
    } catch (error) {
      console.error('Error submitting equipment:', error);
      setError('Error submitting equipment');
    }
  };

  return (
    <div className="equipment-form-container">
      <h1>{isEditing ? 'Edit Equipment' : 'Add Equipment'}</h1>
      <form onSubmit={handleSubmit} className="equipment-form">
        <input
          type="text"
          name="name"
          value={equipment.name}
          onChange={handleChange}
          placeholder="Name"
          required
          className="form-input"
        />
        <textarea
          name="description"
          value={equipment.description}
          onChange={handleChange}
          placeholder="Description"
          required
          className="form-input"
        />
        <input
          type="text"
          name="size"
          value={equipment.size}
          onChange={handleChange}
          placeholder="Size"
          required
          className="form-input"
        />
        <select
          name="state"
          value={equipment.state}
          onChange={handleChange}
          required
          className="form-select"
        >
          <option value="">Select State</option>
          <option value="new">New</option>
          <option value="used">Used</option>
          <option value="damaged">Damaged</option>
        </select>
        <select
          name="material_type"
          value={equipment.material_type}
          onChange={handleMaterialTypeChange}
          required
          className="form-select"
        >
          <option value="rent">Rent</option>
          <option value="sale">Sale</option>
        </select>
        {equipment.material_type === 'sale' && (
          <input
            type="number"
            name="sale_price"
            value={equipment.sale_price || ''}
            onChange={handleChange}
            placeholder="Sale Price"
            className="form-input"
          />
        )}
        {equipment.material_type === 'rent' && (
          <input
            type="number"
            name="rent_price"
            value={equipment.rent_price || ''}
            onChange={handleChange}
            placeholder="Rent Price"
            className="form-input"
          />
        )}
        <input
          type="number"
          name="quantity"
          value={equipment.quantity || ''}
          onChange={handleChange}
          placeholder="Quantity"
          required
          className="form-input"
        />
        <select
          name="equipment_type"
          value={equipment.equipment_type}
          onChange={handleChange}
          required
          className="form-select"
        >
          <option value="">Select Equipment Type</option>
          {EquipmentTypes.map(type => (
            <option key={type.id} value={type.id}>{type.type}</option>
          ))}
        </select>

        {/* Drag and Drop Zone */}
        <DragAndDrop onFilesAdded={handleFilesAdded} />

        <button type="submit" className="submit-button">
          {isEditing ? 'Update Equipment' : 'Add Equipment'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};

export default EquipmentForm;
