import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bell, Send, AlertCircle, Info, CheckCircle } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import './Notifications.css';

const Notifications = () => {
    const [message, setMessage] = useState('');
    const [notificationType, setNotificationType] = useState('info');

    const recentNotifications = [
        { id: 1, type: 'success', message: 'Assignment submissions approved for CLT batch', time: '2 hours ago' },
        { id: 2, type: 'info', message: 'New mentor Reshma added to Floor A', time: '5 hours ago' },
        { id: 3, type: 'warning', message: 'Deadline reminder: SCD pillar submissions due tomorrow', time: '1 day ago' },
        { id: 4, type: 'info', message: 'Leaderboard updated with latest rankings', time: '2 days ago' },
        { id: 5, type: 'success', message: 'System maintenance completed successfully', time: '3 days ago' },
    ];

    const handleSend = () => {
        console.log('Sending notification:', { message, type: notificationType });
        setMessage('');
    };

    return (
        <div className="notifications-page">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div>
                    <h1 className="page-title">
                        <Bell size={32} />
                        Notifications
                    </h1>
                    <p className="page-subtitle">Send announcements and view notification history</p>
                </div>
            </motion.div>

            {/* Send Notification */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="send-notification-section"
            >
                <GlassCard>
                    <div className="notification-form">
                        <h2 className="section-title">Send New Notification</h2>
                        <div className="form-group">
                            <label>Notification Type</label>
                            <div className="type-selector">
                                {['info', 'success', 'warning'].map((type) => (
                                    <button
                                        key={type}
                                        className={`type-btn ${notificationType === type ? 'active' : ''}`}
                                        onClick={() => setNotificationType(type)}
                                    >
                                        {type === 'info' && <Info size={18} />}
                                        {type === 'success' && <CheckCircle size={18} />}
                                        {type === 'warning' && <AlertCircle size={18} />}
                                        {type.charAt(0).toUpperCase() + type.slice(1)}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="form-group">
                            <label>Message</label>
                            <textarea
                                className="notification-textarea"
                                placeholder="Enter your notification message..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                rows={4}
                            />
                        </div>
                        <Button onClick={handleSend} variant="primary">
                            <Send size={18} />
                            Send Notification
                        </Button>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Recent Notifications */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="recent-notifications-section"
            >
                <GlassCard>
                    <h2 className="section-title">Recent Notifications</h2>
                    <div className="notifications-list">
                        {recentNotifications.map((notif, index) => (
                            <motion.div
                                key={notif.id}
                                className={`notification-item ${notif.type}`}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.25 + index * 0.05 }}
                            >
                                <div className="notification-icon">
                                    {notif.type === 'info' && <Info size={20} />}
                                    {notif.type === 'success' && <CheckCircle size={20} />}
                                    {notif.type === 'warning' && <AlertCircle size={20} />}
                                </div>
                                <div className="notification-content">
                                    <p className="notification-message">{notif.message}</p>
                                    <span className="notification-time">{notif.time}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </GlassCard>
            </motion.div>
        </div>
    );
};

export default Notifications;
