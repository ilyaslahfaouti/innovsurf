import React from 'react';
import './ChatbotButton.css';

const ChatbotButton = ({ onClick }) => {
    return (
        <button className="chatbot-button" onClick={onClick}>
            <div className="chatbot-button-icon">🤖</div>
            <div className="chatbot-button-text">InnovBot IA</div>
        </button>
    );
};

export default ChatbotButton;
