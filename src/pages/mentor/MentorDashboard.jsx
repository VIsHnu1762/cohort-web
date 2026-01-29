import React, { useState, useEffect } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import { Users, CheckCircle, Clock, XCircle, Lightbulb, Heart, Trophy, Linkedin, Code, Search, MessageCircle, Send, X as CloseIcon, RefreshCw } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import MentorGamificationPanel from '../../components/MentorGamificationPanel';
import messageService from '../../services/messageService';
import { getMentorStudents } from '../../services/mentor';
import SubmissionReview from './SubmissionReview';
import './MentorDashboard.css';

function MentorDashboard() {
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [showChatModal, setShowChatModal] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('general');
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Fetch students on mount
    useEffect(() => {
        loadStudents();
    }, []);

    const loadStudents = async () => {
        try {
            setLoading(true);
            setError('');
            const data = await getMentorStudents();
            console.log('Fetched students:', data);
            setStudents(data.students || []);
        } catch (err) {
            console.error('Error loading students:', err);
            setError('Failed to load students. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const formatLastSubmission = (timestamp) => {
        if (!timestamp) return 'Never';
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
        return date.toLocaleDateString();
    };

    // Update submissions with formatted timestamps
    const studentsWithFormattedDates = students.map(student => ({
        ...student,
        submissions: Object.entries(student.submissions).reduce((acc, [key, value]) => ({
            ...acc,
            [key]: {
                ...value,
                lastSubmission: formatLastSubmission(value.lastSubmission)
            }
        }), {})
    }));

    const filteredStudents = studentsWithFormattedDates.filter(student =>
        student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.rollNo.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.username.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="mentor-dashboard">
            {/* Header */}
            <motion.div
                className="mentor-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="mentor-title">Student Dashboard</h1>
                <p className="mentor-subtitle">Monitor and review your students' progress</p>
                <Button 
                    onClick={loadStudents} 
                    disabled={loading}
                    className="refresh-button"
                >
                    <RefreshCw size={16} className={loading ? 'spinning' : ''} />
                    Refresh
                </Button>
            </motion.div>

            {/* Loading State */}
            {loading && (
                <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                    <RefreshCw size={48} className="spinning" style={{ marginBottom: '1rem' }} />
                    <p>Loading students...</p>
                </div>
            )}

            {/* Error State */}
            {error && (
                <GlassCard>
                    <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
                        <p>{error}</p>
                        <Button onClick={loadStudents} style={{ marginTop: '1rem' }}>Try Again</Button>
                    </div>
                </GlassCard>
            )}

            {/* Main Content */}
            {!loading && !error && (
                <>
                    {/* Gamification Panel */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                    >
                        <MentorGamificationPanel />
                    </motion.div>

                    {/* Two Column Layout */}
                    <div className="mentor-content">
                {/* Left Side - Student List */}
                <motion.div
                    className="students-panel"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <GlassCard>
                        <div className="students-section">
                            <div className="students-header">
                                <h2 className="section-title">
                                    <Users size={24} />
                                    Assigned Students ({students.length})
                                </h2>
                                <div className="search-box">
                                    <Search size={18} />
                                    <input
                                        type="text"
                                        placeholder="Search students..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="search-input"
                                    />
                                </div>
                            </div>
                            <div className="students-list">
                                {filteredStudents.map((student) => (
                                    <div
                                        key={student.id}
                                        className={`student-card ${selectedStudent?.id === student.id ? 'active' : ''}`}
                                        onClick={() => setSelectedStudent(student)}
                                    >
                                        <div className="student-info">
                                            <h3 className="student-name">{student.name || 'Unknown Student'}</h3>
                                            <p className="student-roll">{student.rollNo || student.roll_no || 'N/A'}</p>
                                            <p className="student-email">{student.email || 'No email'}</p>
                                        </div>
                                        <div className="student-status-summary">
                                            {student.submissions && Object.values(student.submissions).filter(s => s.status === 'pending').length > 0 && (
                                                <span className="pending-badge">
                                                    {Object.values(student.submissions).filter(s => s.status === 'pending').length} Pending
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </GlassCard>
                </motion.div>

                {/* Right Side - Student Details */}
                <motion.div
                    className="details-panel"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                >
                    {selectedStudent ? (
                        <SubmissionReview selectedStudent={selectedStudent} />
                    ) : (
                        <GlassCard>
                            <div className="no-selection">
                                <Users size={64} opacity={0.3} />
                                <h3>Select a Student</h3>
                                <p>Click on a student from the list to view their submission details</p>
                            </div>
                        </GlassCard>
                    )}
                </motion.div>
            </div>

            {/* Chat Modal */}
            <AnimatePresence>
                {showChatModal && selectedStudent && (
                    <motion.div
                        className="modal-overlay"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setShowChatModal(false)}
                    >
                        <motion.div
                            className="chat-modal"
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="chat-modal-header">
                                <div>
                                    <h3>Send Message</h3>
                                    <p>To: {selectedStudent.name}</p>
                                </div>
                                <button
                                    className="close-button"
                                    onClick={() => setShowChatModal(false)}
                                >
                                    <CloseIcon size={20} />
                                </button>
                            </div>

                            <div className="chat-modal-body">
                                <div className="message-type-selector">
                                    <label className="type-label">Message Type:</label>
                                    <div className="type-options">
                                        <label className={`type-option ${messageType === 'general' ? 'active' : ''}`}>
                                            <input
                                                type="radio"
                                                name="messageType"
                                                value="general"
                                                checked={messageType === 'general'}
                                                onChange={(e) => setMessageType(e.target.value)}
                                            />
                                            <span>General</span>
                                        </label>
                                        <label className={`type-option ${messageType === 'completion' ? 'active' : ''}`}>
                                            <input
                                                type="radio"
                                                name="messageType"
                                                value="completion"
                                                checked={messageType === 'completion'}
                                                onChange={(e) => setMessageType(e.target.value)}
                                            />
                                            <span>Completion</span>
                                        </label>
                                        <label className={`type-option ${messageType === 'pending' ? 'active' : ''}`}>
                                            <input
                                                type="radio"
                                                name="messageType"
                                                value="pending"
                                                checked={messageType === 'pending'}
                                                onChange={(e) => setMessageType(e.target.value)}
                                            />
                                            <span>Pending Review</span>
                                        </label>
                                    </div>
                                </div>

                                <div className="message-input-container">
                                    <label className="input-label">Message:</label>
                                    <textarea
                                        className="message-textarea"
                                        placeholder="Type your message here..."
                                        value={message}
                                        onChange={(e) => setMessage(e.target.value)}
                                        rows={6}
                                    />
                                </div>
                            </div>

                            <div className="chat-modal-footer">
                                <Button
                                    variant="secondary"
                                    onClick={() => setShowChatModal(false)}
                                >
                                    Cancel
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={async () => {
                                        if (message.trim()) {
                                            try {
                                                await messageService.sendMessage(
                                                    selectedStudent.id,
                                                    message,
                                                    messageType
                                                );
                                                // Show success feedback
                                                alert('Message sent successfully!');
                                                setMessage('');
                                                setMessageType('general');
                                                setShowChatModal(false);
                                            } catch (error) {
                                                console.error('Failed to send message:', error);
                                                alert('Failed to send message. Please try again.');
                                            }
                                        }
                                    }}
                                    disabled={!message.trim()}
                                >
                                    <Send size={16} />
                                    <span>Send</span>
                                </Button>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
                </>
            )}
        </div>
    );
}

export default MentorDashboard;
