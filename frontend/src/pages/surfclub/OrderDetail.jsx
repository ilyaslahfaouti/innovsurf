import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './OrderDetail.css'; 

const OrderDetails = () => {
  const { id } = useParams();
  const [orderItems, setOrderItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    const fetchOrderItems = async () => {
      try {
        const token = getAuthToken();
        const headers = {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        };
        const response = await axios.get(
          `http://localhost:8000/api/surf-club/orders/${id}/`,
          { headers }
        );
        setOrderItems(response.data.orderItems);
        setLoading(false);
      } catch (error) {
        setError("Error fetching order items");
        setLoading(false);
        console.error("Error fetching order items:", error);
      }
    };

    fetchOrderItems();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="order-details-container">
      <h1>Order Details</h1>
      <ul className="order-items-list">
        {orderItems.map((item) => (
          <li key={item.id} className="order-item">
            <div className="order-item-info">
              <p>
                <i className="fas fa-box"></i> <strong>Equipment Name:</strong>{" "}
                {item.equipment.name}
              </p>
              <p>
                <i className="fas fa-layer-group"></i> <strong>Quantity:</strong>{" "}
                {item.quantity}
              </p>
              <p>
                <i className="fas fa-info-circle"></i>{" "}
                <strong>Description:</strong> {item.equipment.description}
              </p>
              <p>
                <i className="fas fa-ruler-combined"></i> <strong>Size:</strong>{" "}
                {item.equipment.size}
              </p>
              <p>
                <i className="fas fa-thermometer-half"></i> <strong>State:</strong>{" "}
                {item.equipment.state}
              </p>
              <p>
                <i className="fas fa-dollar-sign"></i> <strong>Price:</strong> $
                {item.equipment.material_type === "sale"
                  ? item.equipment.sale_price
                  : item.equipment.rent_price}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OrderDetails;
