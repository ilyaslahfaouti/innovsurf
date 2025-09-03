import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = ({ isOpen, onClose }) => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [suggestedQuestions, setSuggestedQuestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [showAllSuggestions, setShowAllSuggestions] = useState(false);
    const messagesEndRef = useRef(null);

    // A chaque ouverture du chatbot, on démarre une session éphémère sans historique
    useEffect(() => {
        if (isOpen) {
            setMessages([]);
            setSessionId(Date.now().toString() + Math.random().toString(36).substr(2, 9));
        }
    }, [isOpen]);

    // Réagir à la déconnexion: réinitialiser la session et messages
    useEffect(() => {
        const onLogout = () => {
            setMessages([]);
            setSessionId(Date.now().toString() + Math.random().toString(36).substr(2, 9));
        };
        window.addEventListener('app:logout', onLogout);
        return () => window.removeEventListener('app:logout', onLogout);
    }, []);

    // Message de bienvenue
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([
                {
                    id: 1,
                    type: 'bot',
                    content: 'Bonjour ! Je suis YalaBot, votre assistant surf IA. Comment puis-je vous aider aujourd\'hui ? 🏄‍♂️',
                    timestamp: new Date()
                }
            ]);
        }
    }, [isOpen, messages.length]);

    // Scroll automatique vers le bas
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async (message) => {
        if (!message.trim()) return;

        const userMessage = {
            id: Date.now(),
            type: 'user',
            content: message,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const token = localStorage.getItem('accessToken');
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await axios.post(
                'http://localhost:8000/api/chatbot/',
                {
                    message: message,
                    session_id: sessionId
                },
                { headers }
            );

            const botMessage = {
                id: Date.now() + 1,
                type: 'bot',
                content: response.data.response,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, botMessage]);
            setSuggestedQuestions(response.data.suggested_questions || []);
        } catch (error) {
            console.error('Erreur chatbot:', error);
            const errorMessage = {
                id: Date.now() + 1,
                type: 'bot',
                content: 'Désolé, je rencontre un problème technique. Pouvez-vous réessayer ?',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        sendMessage(inputMessage);
    };

    const handleSuggestedQuestion = (question) => {
        sendMessage(question);
    };

    if (!isOpen) return null;

    return (
        <div className="chatbot-overlay" onClick={onClose}>
            <div className="chatbot-container" onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div className="chatbot-header">
                    <div className="chatbot-title">
                        <div className="chatbot-avatar">🤖</div>
                        <div>
                            <h3>InnovBot IA</h3>
                            <span className="chatbot-status">En ligne</span>
                        </div>
                    </div>
                    <button
                        type="button"
                        className="chatbot-toggle-suggestions"
                        onClick={() => setShowSuggestions(v => !v)}
                        aria-expanded={showSuggestions}
                    >
                        {showSuggestions ? 'Masquer' : 'Suggestions'}
                    </button>
                    <button className="chatbot-close" onClick={onClose}>
                        ✕
                    </button>
                </div>

                {/* Messages */}
                <div className="chatbot-messages">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`chatbot-message ${message.type === 'user' ? 'user' : 'bot'}`}
                        >
                            <div className="message-content">
                                {message.content}
                            </div>
                            <div className="message-timestamp">
                                {message.timestamp.toLocaleTimeString('fr-FR', {
                                    hour: '2-digit',
                                    minute: '2-digit'
                                })}
                            </div>
                        </div>
                    ))}
                    
                    {isLoading && (
                        <div className="chatbot-message bot">
                            <div className="message-content">
                                <div className="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    <div ref={messagesEndRef} />
                </div>

                {/* Questions suggérées (repliables) */}
                {suggestedQuestions.length > 0 && showSuggestions && (
                    <div className="chatbot-suggestions">
                        <p>Suggestions rapides</p>
                        <div className="suggestion-buttons">
                            {suggestedQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    className="suggestion-button"
                                    onClick={() => handleSuggestedQuestion(question)}
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Input */}
                <form className="chatbot-input-container" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Tapez votre message..."
                        className="chatbot-input"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className="chatbot-send-button"
                        disabled={isLoading || !inputMessage.trim()}
                    >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <path
                                d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Chatbot;
