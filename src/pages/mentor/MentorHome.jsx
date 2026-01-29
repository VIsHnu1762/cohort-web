import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Users, TrendingUp, Award, Calendar, Bell, User, Mail, Phone, Hash, CheckCircle, X } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import { useAuth } from '../../context/AuthContext';
import { getNotifications, markNotificationRead, deleteNotification } from '../../services/notifications';
import { getMentorStudents } from '../../services/mentor';
import { getAnnouncements } from '../../services/announcements';
import './MentorHome.css';

function MentorHome() {
    const { user } = useAuth();
    const [showProfile, setShowProfile] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [loadingNotifications, setLoadingNotifications] = useState(true);
    const [students, setStudents] = useState([]);
    const [announcements, setAnnouncements] = useState([]);
    const [stats, setStats] = useState({
        totalStudents: 0,
        activeSubmissions: 0,
        completedReviews: 0,
        pendingReviews: 0,
    });

    // Fetch notifications and students on mount
    useEffect(() => {
        loadNotifications();
        loadStudents();
        loadAnnouncements();
    }, []);

    const loadAnnouncements = async () => {
        try {
            const data = await getAnnouncements();
            setAnnouncements(data.announcements || []);
        } catch (error) {
            console.error('Error loading announcements:', error);
        }
    };

    const loadStudents = async () => {
        try {
            const data = await getMentorStudents();
            setStudents(data.students || []);
            
            // Calculate stats from students data
            const totalStudents = data.students.length;
            let activeSubmissions = 0;
            let completedReviews = 0;
            let pendingReviews = 0;
            
            data.students.forEach(student => {
                Object.values(student.submissions).forEach(submission => {
                    if (submission.status === 'pending') {
                        activeSubmissions++;
                        pendingReviews += submission.count;
                    }
                    if (submission.status === 'completed') {
                        completedReviews += submission.count;
                    }
                });
            });
            
            setStats({
                totalStudents,
                activeSubmissions,
                completedReviews,
                pendingReviews
            });
        } catch (error) {
            console.error('Error loading students:', error);
        }
    };

    const loadNotifications = async () => {
        try {
            setLoadingNotifications(true);
            console.log('Fetching notifications...');
            const data = await getNotifications();
            console.log('Notifications received:', data);
            setNotifications(data);
        } catch (error) {
            console.error('Error loading notifications:', error);
            console.error('Error details:', error.response?.data);
        } finally {
            setLoadingNotifications(false);
        }
    };

    const handleMarkAsRead = async (notificationId) => {
        try {
            await markNotificationRead(notificationId);
            setNotifications(prev => 
                prev.map(notif => 
                    notif.id === notificationId ? { ...notif, is_read: true } : notif
                )
            );
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    };

    const handleDeleteNotification = async (notificationId) => {
        try {
            await deleteNotification(notificationId);
            setNotifications(prev => prev.filter(notif => notif.id !== notificationId));
        } catch (error) {
            console.error('Error deleting notification:', error);
        }
    };

    const getNotificationIcon = (type) => {
        switch(type) {
            case 'warning':
                return '⚠️';
            case 'success':
                return '✅';
            case 'error':
                return '❌';
            default:
                return 'ℹ️';
        }
    };

    const getNotificationStyle = (type) => {
        switch(type) {
            case 'warning':
                return {
                    background: 'rgba(251, 191, 36, 0.1)',
                    borderLeft: '3px solid #fbbf24'
                };
            case 'success':
                return {
                    background: 'rgba(74, 222, 128, 0.1)',
                    borderLeft: '3px solid #4ade80'
                };
            case 'error':
                return {
                    background: 'rgba(239, 68, 68, 0.1)',
                    borderLeft: '3px solid #ef4444'
                };
            default:
                return {
                    background: 'rgba(96, 165, 250, 0.1)',
                    borderLeft: '3px solid #60a5fa'
                };
        }
    };

    const formatNotificationTime = (timestamp) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    };

    const getPriorityColor = (priority) => {
        switch(priority) {
            case 'high':
                return '#ef4444';
            case 'medium':
                return '#f59e0b';
            case 'low':
                return '#10b981';
            default:
                return '#6b7280';
        }
    };

    const getCategoryIcon = (category) => {
        switch(category) {
            case 'event':
                return '🎉';
            case 'deadline':
                return '⏰';
            case 'important':
                return '❗';
            case 'reminder':
                return '🔔';
            default:
                return 'ℹ️';
        }
    };

    // Mock mentor data
    const mentorInfo = {
        name: user?.name || 'Dr. Sarah Johnson',
        email: user?.email || 'mentor@test.com',
        phone: '+91 9876543210',
        mentorId: 'MNT-001',
        studentsHandling: stats.totalStudents,
    };

    return (
        <div className="mentor-home-container">
            {/* Profile Modal */}
            {showProfile && (
                <motion.div
                    className="profile-modal-overlay"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    onClick={() => setShowProfile(false)}
                >
                    <motion.div
                        className="profile-modal"
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <GlassCard>
                            <div className="profile-modal-content">
                                <div className="profile-avatar">
                                    <User size={48} />
                                </div>
                                <h2>{mentorInfo.name}</h2>
                                <div className="profile-details">
                                    <div className="profile-detail-item">
                                        <Mail size={18} />
                                        <span>{mentorInfo.email}</span>
                                    </div>
                                    <div className="profile-detail-item">
                                        <Phone size={18} />
                                        <span>{mentorInfo.phone}</span>
                                    </div>
                                    <div className="profile-detail-item">
                                        <Hash size={18} />
                                        <span>Mentor ID: {mentorInfo.mentorId}</span>
                                    </div>
                                    <div className="profile-detail-item">
                                        <Users size={18} />
                                        <span>Students Handling: {mentorInfo.studentsHandling}</span>
                                    </div>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                </motion.div>
            )}

            {/* Header */}
            <div className="mentor-home-header">
                <div className="home-welcome">
                    <h1>Welcome back, {mentorInfo.name.split(' ')[0]}!</h1>
                    <p>Track your progress and stay updated with your learning journey</p>
                </div>
                <motion.button
                    className="profile-icon-btn"
                    onClick={() => setShowProfile(true)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <User size={24} />
                </motion.button>
            </div>

            {/* Stats Grid - Full Width Row */}
            <div className="mentor-stats-grid">
                <GlassCard hoverable>
                    <div className="mentor-stat-card">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                            <Users size={28} />
                        </div>
                        <div className="stat-info">
                            <p className="stat-label">Total Students</p>
                            <h3 className="stat-value">{stats.totalStudents}</h3>
                        </div>
                    </div>
                </GlassCard>

                <GlassCard hoverable>
                    <div className="mentor-stat-card">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                            <TrendingUp size={28} />
                        </div>
                        <div className="stat-info">
                            <p className="stat-label">Active Submissions</p>
                            <h3 className="stat-value">{stats.activeSubmissions}</h3>
                        </div>
                    </div>
                </GlassCard>

                <GlassCard hoverable>
                    <div className="mentor-stat-card">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                            <Award size={28} />
                        </div>
                        <div className="stat-info">
                            <p className="stat-label">Completed Reviews</p>
                            <h3 className="stat-value">{stats.completedReviews}</h3>
                        </div>
                    </div>
                </GlassCard>

                <GlassCard hoverable>
                    <div className="mentor-stat-card">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }}>
                            <BookOpen size={28} />
                        </div>
                        <div className="stat-info">
                            <p className="stat-label">Pending Reviews</p>
                            <h3 className="stat-value">{stats.pendingReviews}</h3>
                        </div>
                    </div>
                </GlassCard>
            </div>

            {/* Dashboard Layout */}
            <div className="mentor-home-dashboard">
                {/* Left Column */}
                <div className="mentor-home-left-column">
                    {/* Notifications */}
                    <GlassCard>
                        <div className="section-header">
                            <h2 className="section-title">
                                <Bell size={24} />
                                Notifications
                            </h2>
                        </div>
                        <div className="activity-list">
                            {loadingNotifications ? (
                                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                                    Loading notifications...
                                </div>
                            ) : notifications.length === 0 ? (
                                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                                    No new notifications
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <motion.div
                                        key={notification.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        style={{
                                            ...getNotificationStyle(notification.notification_type),
                                            padding: '1rem',
                                            borderRadius: '8px',
                                            marginBottom: '0.75rem',
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'flex-start',
                                            gap: '0.75rem',
                                            opacity: notification.is_read ? 0.6 : 1,
                                            transition: 'all 0.2s'
                                        }}
                                    >
                                        <div style={{ flex: 1 }}>
                                            <div style={{ 
                                                display: 'flex', 
                                                alignItems: 'center', 
                                                gap: '0.5rem',
                                                marginBottom: '0.25rem'
                                            }}>
                                                <span style={{ fontSize: '1.2rem' }}>
                                                    {getNotificationIcon(notification.notification_type)}
                                                </span>
                                                <span style={{ 
                                                    fontSize: '0.75rem', 
                                                    color: 'var(--text-secondary)',
                                                    textTransform: 'uppercase',
                                                    fontWeight: '600'
                                                }}>
                                                    {notification.notification_type}
                                                </span>
                                            </div>
                                            <p style={{ 
                                                margin: 0, 
                                                fontSize: '0.9rem',
                                                lineHeight: '1.4',
                                                color: 'var(--text-primary)'
                                            }}>
                                                {notification.message}
                                            </p>
                                            <span style={{ 
                                                fontSize: '0.75rem', 
                                                color: 'var(--text-secondary)',
                                                marginTop: '0.25rem',
                                                display: 'block'
                                            }}>
                                                {formatNotificationTime(notification.created_at)}
                                            </span>
                                        </div>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            {!notification.is_read && (
                                                <button
                                                    onClick={() => handleMarkAsRead(notification.id)}
                                                    style={{
                                                        background: 'rgba(74, 222, 128, 0.2)',
                                                        border: 'none',
                                                        borderRadius: '4px',
                                                        padding: '0.25rem 0.5rem',
                                                        cursor: 'pointer',
                                                        color: '#4ade80',
                                                        fontSize: '0.8rem',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        gap: '0.25rem'
                                                    }}
                                                    title="Mark as read"
                                                >
                                                    <CheckCircle size={14} />
                                                </button>
                                            )}
                                            <button
                                                onClick={() => handleDeleteNotification(notification.id)}
                                                style={{
                                                    background: 'rgba(239, 68, 68, 0.2)',
                                                    border: 'none',
                                                    borderRadius: '4px',
                                                    padding: '0.25rem 0.5rem',
                                                    cursor: 'pointer',
                                                    color: '#ef4444',
                                                    fontSize: '0.8rem'
                                                }}
                                                title="Delete"
                                            >
                                                <X size={14} />
                                            </button>
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </div>
                    </GlassCard>
                </div>

                {/* Right Column */}
                <div className="mentor-home-right-column">
                    {/* Upcoming Events/Announcements */}
                    <GlassCard>
                        <div className="section-header">
                            <h2 className="section-title">
                                <Calendar size={24} />
                                Upcoming Events & Deadlines
                            </h2>
                        </div>
                        <div className="deadlines-list">
                            {announcements.length === 0 ? (
                                <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                                    No upcoming events or deadlines
                                </div>
                            ) : (
                                announcements
                                    .filter(ann => ann.category === 'event' || ann.category === 'deadline')
                                    .slice(0, 5)
                                    .map((announcement) => (
                                        <div key={announcement.id} className="deadline-item">
                                            <div 
                                                className="deadline-priority" 
                                                style={{ background: getPriorityColor(announcement.priority) }}
                                            ></div>
                                            <div className="deadline-info">
                                                <p className="deadline-title">
                                                    <span style={{ marginRight: '0.5rem' }}>
                                                        {getCategoryIcon(announcement.category)}
                                                    </span>
                                                    {announcement.title}
                                                </p>
                                                <span className="deadline-date">
                                                    {announcement.event_date 
                                                        ? new Date(announcement.event_date).toLocaleDateString() 
                                                        : announcement.time_ago}
                                                </span>
                                            </div>
                                        </div>
                                    ))
                            )}
                        </div>
                    </GlassCard>
                </div>
            </div>
        </div>
    );
}

export default MentorHome;
