import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaTrashAlt } from 'react-icons/fa'; 
import './Cart.css';

const Cart = () => {
    const [cart, setCart] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const storedCart = JSON.parse(localStorage.getItem('cart')) || [];
        setCart(storedCart);
    }, []);

    const handleRemoveItem = (index) => {
        const updatedCart = [...cart];
        updatedCart.splice(index, 1);
        setCart(updatedCart);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
    };

    const handleOrder = async () => {
        const token = localStorage.getItem('accessToken');
        const surfClubId = cart[0]?.equipment.surf_club;

        try {
            const response = await axios.post(
                'http://localhost:8000/api/surfers/add-order/',
                {
                    surf_club: surfClubId,
                    items: cart.map(item => ({
                        equipment: item.equipment.id,
                        quantity: item.quantity,
                    })),
                },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
          
            localStorage.removeItem('cart');
            navigate('/surfer/profile')
         
        } catch (error) {
            console.error("Failed to place order", error);
            alert("Erreur lors du passage de la commande. Veuillez réessayer.");
        }
    };

    const calculateTotal = () => {
        return cart.reduce((total, item) => total + item.quantity * item.equipment.sale_price, 0).toFixed(2);
    };

    return (
        <div className="cart-page">
            <h1 className="cart-title">My Cart</h1>
            {cart.length === 0 ? (
                <p>Your cart is empty ! </p>
            ) : (
                <>
                    <ul className="cart-items">
                        {cart.map((item, index) => (
                            <li key={index} className="cart-item">
                                <img src={`http://localhost:8000${item.equipment.photos[0]?.image}`} alt={item.equipment.name} className="cart-item-image" />
                                <div className="cart-item-details">
                                    <p className="cart-item-name">{item.equipment.name}</p>
                                    <p className="cart-item-price">{item.equipment.sale_price} €</p>
                                    <p className="cart-item-quantity">Quantity: {item.quantity}</p>
                                </div>
                                <button className="cart-item-remove" onClick={() => handleRemoveItem(index)}>
                                    <FaTrashAlt />
                                </button>
                            </li>
                        ))}
                    </ul>
                    <div className="cart-total">
                        <p>Total: <span>{calculateTotal()} €</span></p>
                    </div>
                    <button className="cart-order-btn" onClick={handleOrder}>
                    Place your order</button>
                </>
            )}
        </div>
    );
};

export default Cart;
