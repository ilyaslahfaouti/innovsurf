import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Orders.css'; 

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getAuthToken = () => {
    return localStorage.getItem('accessToken');
  };

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = getAuthToken();
        const headers = {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        };
        const response = await axios.get(
          "http://localhost:8000/api/surf-club/orders/",
          { headers }
        );
        setOrders(response.data.orders);
        setLoading(false);
      } catch (error) {
        setError("Error fetching orders");
        setLoading(false);
        console.error("Error fetching orders:", error);
      }
    };

    fetchOrders();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="orders-container">
      <h1>Orders</h1>
      <ul className="orders-list">
        {orders.map((order) => (
          <li key={order.id} className="order-item">
            <div className="order-info">
              <p>
                <i className="fas fa-receipt"></i> <strong>Order ID:</strong>{" "}
                {order.id}
              </p>
              <p>
                <i className="fas fa-user"></i> <strong>Surfer:</strong>{" "}
                {order.surfer
                  ? `${order.surfer.firstname} ${order.surfer.lastname}`
                  : "N/A"}
              </p>
              <p>
                <i className="fas fa-calendar-alt"></i> <strong></strong>{" "}
                {order.order_date}
              </p>
              <p>
                <i className="fas fa-dollar-sign"></i> <strong></strong>{" "}
                ${order.total_price}
              </p>
            </div>
            <div className="order-actions">
              <Link to={`/dashboard/orders/${order.id}`} className="action-link">
                <i className="fas fa-eye"></i> View Details
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Orders;
