import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FaRuler, FaTag, FaEuroSign, FaArrowLeft, FaArrowRight } from 'react-icons/fa'; // Importing icons
import './EquipmentDetails.css';

const EquipmentDetails = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { equipment } = location.state || {};
    const [quantity, setQuantity] = useState(1);
    const [currentSlide, setCurrentSlide] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentSlide((prev) => 
                equipment?.photos?.length ? (prev === equipment.photos.length - 1 ? 0 : prev + 1) : 0
            );
        }, 3000); // Change slide every 3 seconds

        return () => clearInterval(interval);
    }, [equipment]);

    const handleNextSlide = () => {
        setCurrentSlide((prev) =>
            prev === equipment.photos.length - 1 ? 0 : prev + 1
        );
    };

    const handlePrevSlide = () => {
        setCurrentSlide((prev) =>
            prev === 0 ? equipment.photos.length - 1 : prev - 1
        );
    };

    const handleQuantityChange = (e) => {
        const value = parseInt(e.target.value);
        if (value > 0 && value <= equipment.quantity) {
            setQuantity(value);
        } else if (value > equipment.quantity) {
            setQuantity(equipment.quantity); // Set to max if exceeded
        }
    };

    if (!equipment) {
        return <p>Loading...</p>;
    }

    const handleAddToCart = () => {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingItem = cart.find(item => item.equipment.id === equipment.id);
        if (existingItem) {
            if (existingItem.quantity + quantity <= equipment.quantity) {
                existingItem.quantity += quantity;
            } else {
                existingItem.quantity = equipment.quantity; // Limit to available stock
            }
        } else {
            cart.push({ equipment, quantity });
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        navigate(`/surf-clubs/${equipment.surf_club}/equipments`);
    };

    return (
        <div className="equipment-details-page">
            <div className="equipment-image-section">
                <div className="equipment-slider">
                    <div className="equipment-slider-wrapper" style={{ transform: `translateX(-${currentSlide * 100}%)` }}>
                        {equipment.photos && equipment.photos.length > 0 ? (
                            equipment.photos.map((photo, index) => (
                                <div key={index} className={`equipment-slide ${index === currentSlide ? 'active' : ''}`}>
                                    <img 
                                        src={`http://localhost:8000${photo.image}`} 
                                        alt={`Slide ${index + 1}`} 
                                        className="equipment-slide-image"
                                    />
                                </div>
                            ))
                        ) : (
                            <p>No photos available</p>
                        )}
                    </div>
                    <button className="prev-button" onClick={handlePrevSlide}>
                        <FaArrowLeft />
                    </button>
                    <button className="next-button" onClick={handleNextSlide}>
                        <FaArrowRight />
                    </button>
                </div>
            </div>
            <div className="equipment-info-section">
                <h2 className="equipment-category">BEST EQUIPMENT</h2>
                <h1 className="equipment-title">{equipment.name}</h1>
                <p className="equipment-description">{equipment.description}</p>
                <div className="equipment-details">
                    <p><FaRuler /> <strong>Size:</strong> {equipment.size}</p>
                    <p><FaTag /> <strong>State:</strong> {equipment.state}</p>
                    <p><FaEuroSign /> <strong>Price:</strong> {equipment.sale_price} €</p>
                    <p><strong>Stock:</strong> {equipment.quantity}</p>
                </div>
                <div className="equipment-quantity">
                    <label htmlFor="quantity">Quantity:</label>
                    <input
                        type="number"
                        id="quantity"
                        value={quantity}
                        onChange={handleQuantityChange}
                        min="1"
                        max={equipment.quantity}
                    />
                </div>
                <button className="add-to-cart-btn" onClick={handleAddToCart}>Add to Cart</button>
            </div>
        </div>
    );
};

export default EquipmentDetails;
