import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, X, Check, CheckCheck } from 'lucide-react';
import './NotificationBell.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const NotificationBell = () => {
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        fetchUnreadCount();
        
        // Poll for new notifications every 30 seconds
        const interval = setInterval(fetchUnreadCount, 30000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        // Close dropdown on outside click
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const fetchUnreadCount = async () => {
        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch(`${API_BASE_URL}/profiles/notifications/unread_count/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            const data = await response.json();
            setUnreadCount(data.unread_count || 0);
        } catch (error) {
            console.error('Failed to fetch unread count:', error);
        }
    };

    const fetchNotifications = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch(`${API_BASE_URL}/profiles/notifications/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            const data = await response.json();
            setNotifications(data.results || data || []);
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    const markAsRead = async (notificationId) => {
        try {
            const token = localStorage.getItem('accessToken');
            await fetch(`${API_BASE_URL}/profiles/notifications/${notificationId}/mark_read/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            
            // Update local state
            setNotifications(prev => prev.map(n => 
                n.id === notificationId ? { ...n, is_read: true } : n
            ));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    };

    const markAllAsRead = async () => {
        try {
            const token = localStorage.getItem('accessToken');
            await fetch(`${API_BASE_URL}/profiles/notifications/mark_all_read/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            
            // Update local state
            setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
            setUnreadCount(0);
        } catch (error) {
            console.error('Failed to mark all as read:', error);
        }
    };

    const handleBellClick = () => {
        setIsOpen(!isOpen);
        if (!isOpen) {
            fetchNotifications();
        }
    };

    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'high': return '#F44336';
            case 'normal': return '#2196F3';
            case 'low': return '#9E9E9E';
            default: return '#2196F3';
        }
    };

    return (
        <div className="notification-bell-container" ref={dropdownRef}>
            <motion.button
                className="notification-bell-button"
                onClick={handleBellClick}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
            >
                <Bell size={20} />
                {unreadCount > 0 && (
                    <motion.span
                        className="notification-badge"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        key={unreadCount}
                    >
                        {unreadCount > 99 ? '99+' : unreadCount}
                    </motion.span>
                )}
            </motion.button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="notification-dropdown"
                        initial={{ opacity: 0, y: -10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -10, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="notification-header">
                            <h3>Notifications</h3>
                            <div className="notification-actions">
                                {unreadCount > 0 && (
                                    <motion.button
                                        className="mark-all-read"
                                        onClick={markAllAsRead}
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <CheckCheck size={16} />
                                        Mark all read
                                    </motion.button>
                                )}
                                <button 
                                    className="close-dropdown"
                                    onClick={() => setIsOpen(false)}
                                >
                                    <X size={18} />
                                </button>
                            </div>
                        </div>

                        <div className="notification-list">
                            {loading ? (
                                <div className="notification-loading">Loading...</div>
                            ) : notifications.length === 0 ? (
                                <div className="notification-empty">
                                    <Bell size={40} />
                                    <p>No notifications</p>
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <motion.div
                                        key={notification.id}
                                        className={`notification-item ${!notification.is_read ? 'unread' : ''}`}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        whileHover={{ backgroundColor: 'rgba(247, 201, 72, 0.05)' }}
                                    >
                                        <div 
                                            className="notification-indicator"
                                            style={{ backgroundColor: getPriorityColor(notification.priority) }}
                                        />
                                        <div className="notification-content">
                                            <div className="notification-title">
                                                {notification.title}
                                            </div>
                                            <div className="notification-message">
                                                {notification.message}
                                            </div>
                                            <div className="notification-time">
                                                {notification.time_ago || 'Just now'}
                                            </div>
                                        </div>
                                        {!notification.is_read && (
                                            <motion.button
                                                className="mark-read-btn"
                                                onClick={() => markAsRead(notification.id)}
                                                whileHover={{ scale: 1.1 }}
                                                whileTap={{ scale: 0.9 }}
                                            >
                                                <Check size={16} />
                                            </motion.button>
                                        )}
                                    </motion.div>
                                ))
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default NotificationBell;
