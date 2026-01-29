import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, UserCheck, Users, CheckCircle, Clock, TrendingUp, ChevronDown, ChevronUp, Mail } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Input from '../../../components/Input';
import './MentorProfiles.css';

const MentorProfiles = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedMentor, setSelectedMentor] = useState(null);
    const [expandedMentor, setExpandedMentor] = useState(null);

    // Mock mentor data with their students
    const mentors = [
        {
            id: 1,
            name: 'Reshma',
            email: 'reshma@mentor.com',
            phone: '+91 98765 11111',
            department: 'Computer Science',
            expertise: ['Full Stack Development', 'React', 'Node.js', 'Database Design'],
            studentsHandled: 28,
            verificationsPending: 12,
            verificationsCompleted: 156,
            avgResponseTime: '1.9 hours',
            rating: 4.9,
            floors: ['Floor A', 'Floor B'],
            students: [
                { id: 1, name: 'Amal Krishna', xp: 4850, pillarsCompleted: 5 },
                { id: 2, name: 'Sreeram', xp: 4520, pillarsCompleted: 5 },
                { id: 3, name: 'Vishnu', xp: 4200, pillarsCompleted: 4 },
                { id: 4, name: 'Athira', xp: 3890, pillarsCompleted: 4 },
            ]
        },
        {
            id: 2,
            name: 'Thulasi',
            email: 'thulasi@mentor.com',
            phone: '+91 98765 22222',
            department: 'Information Technology',
            expertise: ['Data Science', 'Python', 'Machine Learning', 'AI'],
            studentsHandled: 22,
            verificationsPending: 7,
            verificationsCompleted: 134,
            avgResponseTime: '2.1 hours',
            rating: 4.8,
            floors: ['Floor C', 'Floor D'],
            students: [
                { id: 5, name: 'Rahul', xp: 3650, pillarsCompleted: 4 },
                { id: 6, name: 'Priya', xp: 3420, pillarsCompleted: 3 },
                { id: 7, name: 'Karthik', xp: 3180, pillarsCompleted: 3 },
            ]
        },
        {
            id: 3,
            name: 'Gopi',
            email: 'gopi@mentor.com',
            phone: '+91 98765 33333',
            department: 'Computer Science',
            expertise: ['DevOps', 'Cloud Computing', 'System Design', 'Docker & Kubernetes'],
            studentsHandled: 25,
            verificationsPending: 9,
            verificationsCompleted: 148,
            avgResponseTime: '1.7 hours',
            rating: 4.9,
            floors: ['Floor A', 'Floor E'],
            students: [
                { id: 8, name: 'Anjali', xp: 2950, pillarsCompleted: 3 },
                { id: 9, name: 'Arjun', xp: 2720, pillarsCompleted: 2 },
                { id: 10, name: 'Meera', xp: 2500, pillarsCompleted: 2 },
            ]
        }
    ];

    const filteredMentors = mentors.filter(mentor =>
        mentor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        mentor.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Calculate overall stats
    const totalMentors = mentors.length;
    const totalStudents = mentors.reduce((sum, m) => sum + m.studentsHandled, 0);
    const avgApprovalRate = mentors.reduce((sum, m) => sum + m.approvalRate, 0) / mentors.length;
    const avgResponseTime = '1.5 hours';

    return (
        <div className="mentor-profiles-page">
            <div style={{ padding: '0 2rem' }}>
                <div className="page-header">
                    <div className="header-content">
                        <h1 className="page-title">Mentor Profiles</h1>
                        <p className="page-subtitle">View and manage mentor profiles and assignments</p>
                    </div>
                </div>

                {/* Stats Overview */}
                <div className="mentor-stats-grid">
                    <motion.div
                        className="mentor-stat-card"
                        whileHover={{ scale: 1.02 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                    >
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                            <Users size={28} />
                        </div>
                        <div className="stat-content">
                            <h3 className="stat-value">{totalMentors}</h3>
                            <p className="stat-label">Total Mentors</p>
                        </div>
                    </motion.div>

                    <motion.div
                        className="mentor-stat-card"
                        whileHover={{ scale: 1.02 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ffcc00 0%, #ffcc00 100%)' }}>
                            <CheckCircle size={28} />
                        </div>
                        <div className="stat-content">
                            <h3 className="stat-value">{avgApprovalRate.toFixed(1)}%</h3>
                            <p className="stat-label">Avg Approval Rate</p>
                        </div>
                    </motion.div>

                    <motion.div
                        className="mentor-stat-card"
                        whileHover={{ scale: 1.02 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)' }}>
                            <Users size={28} />
                        </div>
                        <div className="stat-content">
                            <h3 className="stat-value">{totalStudents}</h3>
                            <p className="stat-label">Total Students</p>
                        </div>
                    </motion.div>

                    <motion.div
                        className="mentor-stat-card"
                        whileHover={{ scale: 1.02 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                    >
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                            <Clock size={28} />
                        </div>
                        <div className="stat-content">
                            <h3 className="stat-value">{avgResponseTime}</h3>
                            <p className="stat-label">Avg Response Time</p>
                        </div>
                    </motion.div>
                </div>

                {/* Action Bar */}
                <div className="mentor-actions">
                    <div className="search-container">
                        <Input
                            icon={Search}
                            placeholder="Search mentors..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <motion.button
                        className="action-btn primary-action-btn"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <UserCheck size={20} />
                        Add Mentor
                    </motion.button>
                </div>

                <div className="mentor-layout">
                    {/* Mentors Sidebar */}
                    <GlassCard className="mentor-sidebar">
                        <h3 className="sidebar-title">Mentors ({filteredMentors.length})</h3>
                        <nav className="mentor-nav">
                            {filteredMentors.map((mentor) => (
                                <motion.button
                                    key={mentor.id}
                                    onClick={() => setSelectedMentor(mentor)}
                                    className={`nav-item ${selectedMentor?.id === mentor.id ? 'active' : ''}`}
                                    whileHover={{ x: 4 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <UserCheck size={20} />
                                    <span>{mentor.name}</span>
                                </motion.button>
                            ))}
                        </nav>
                    </GlassCard>

                    {/* Mentor Content Area */}
                    <div className="mentor-content-area">
                        {selectedMentor ? (
                            <>
                                {/* Mentor Profile Card - Dashboard Style */}
                                <motion.div
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <GlassCard className="mentor-dashboard-card">
                                        <div className="mentor-profile-header">
                                            <div className="mentor-avatar-section">
                                                <div className="mentor-avatar-large">
                                                    <UserCheck size={48} />
                                                </div>
                                                <div className="mentor-info-section">
                                                    <h2 className="mentor-name-title">{selectedMentor.name}</h2>
                                                    <p className="mentor-department-badge">{selectedMentor.department}</p>
                                                    <div className="mentor-contact-info">
                                                        <span className="contact-item">
                                                            <Mail size={14} />
                                                            {selectedMentor.email}
                                                        </span>
                                                        <span className="contact-item">{selectedMentor.phone}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="mentor-action-buttons">
                                                <motion.button
                                                    className="mentor-primary-action"
                                                    whileHover={{ scale: 1.05 }}
                                                    whileTap={{ scale: 0.95 }}
                                                >
                                                    <Mail size={18} />
                                                    Message
                                                </motion.button>
                                                <motion.button
                                                    className="mentor-secondary-action"
                                                    whileHover={{ scale: 1.05 }}
                                                    whileTap={{ scale: 0.95 }}
                                                >
                                                    <Users size={18} />
                                                    Assign Students
                                                </motion.button>
                                            </div>
                                        </div>
                                    </GlassCard>
                                </motion.div>

                                {/* Performance Stats - Dashboard Style */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.1 }}
                                >
                                    <GlassCard className="mentor-dashboard-card">
                                        <h2 className="section-title-dashboard">Performance Metrics</h2>
                                        <div className="mentor-performance-grid">
                                            <div className="performance-stat-item">
                                                <div className="perf-stat-icon" style={{ backgroundColor: 'rgba(247, 201, 72, 0.2)' }}>
                                                    <Users size={24} style={{ color: '#ffcc00' }} />
                                                </div>
                                                <div className="perf-stat-info">
                                                    <span className="perf-stat-value">{selectedMentor.studentsHandled}</span>
                                                    <span className="perf-stat-label">Students Handled</span>
                                                </div>
                                            </div>

                                            <div className="performance-stat-item">
                                                <div className="perf-stat-icon" style={{ backgroundColor: 'rgba(229, 57, 53, 0.2)' }}>
                                                    <CheckCircle size={24} style={{ color: '#ffcc00' }} />
                                                </div>
                                                <div className="perf-stat-info">
                                                    <span className="perf-stat-value">{selectedMentor.verificationsCompleted}</span>
                                                    <span className="perf-stat-label">Verifications Done</span>
                                                </div>
                                            </div>

                                            <div className="performance-stat-item">
                                                <div className="perf-stat-icon" style={{ backgroundColor: 'rgba(255, 193, 7, 0.2)' }}>
                                                    <Clock size={24} style={{ color: '#FFC107' }} />
                                                </div>
                                                <div className="perf-stat-info">
                                                    <span className="perf-stat-value">{selectedMentor.verificationsPending}</span>
                                                    <span className="perf-stat-label">Pending Reviews</span>
                                                </div>
                                            </div>

                                            <div className="performance-stat-item">
                                                <div className="perf-stat-icon" style={{ backgroundColor: 'rgba(76, 175, 80, 0.2)' }}>
                                                    <TrendingUp size={24} style={{ color: '#4CAF50' }} />
                                                </div>
                                                <div className="perf-stat-info">
                                                    <span className="perf-stat-value">{selectedMentor.rating}</span>
                                                    <span className="perf-stat-label">Average Rating</span>
                                                </div>
                                            </div>
                                        </div>
                                    </GlassCard>
                                </motion.div>

                                {/* Expertise & Floors - Dashboard Style */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 }}
                                >
                                    <GlassCard className="mentor-dashboard-card">
                                        <h2 className="section-title-dashboard">Expertise & Assignment</h2>
                                        <div className="expertise-floors-container">
                                            <div className="expertise-section-dashboard">
                                                <h3 className="subsection-title">
                                                    <CheckCircle size={18} />
                                                    Expertise Areas
                                                </h3>
                                                <div className="expertise-tags-dashboard">
                                                    {selectedMentor.expertise.map((skill, index) => (
                                                        <span key={index} className="expertise-tag-dashboard">{skill}</span>
                                                    ))}
                                                </div>
                                            </div>
                                            <div className="floors-section-dashboard">
                                                <h3 className="subsection-title">
                                                    <Users size={18} />
                                                    Assigned Floors
                                                </h3>
                                                <div className="floors-tags-dashboard">
                                                    {selectedMentor.floors.map((floor, index) => (
                                                        <span key={index} className="floor-tag-dashboard">{floor}</span>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </GlassCard>
                                </motion.div>

                                {/* Students List - Dashboard Style */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.3 }}
                                >
                                    <GlassCard className="mentor-dashboard-card">
                                        <h2 className="section-title-dashboard">
                                            Students Under Guidance ({selectedMentor.students.length})
                                        </h2>
                                        <div className="students-grid-dashboard">
                                            {selectedMentor.students.map((student) => (
                                                <div key={student.id} className="student-card-dashboard">
                                                    <div className="student-avatar-dashboard">
                                                        {student.name.charAt(0)}
                                                    </div>
                                                    <div className="student-info-dashboard">
                                                        <span className="student-name-dashboard">{student.name}</span>
                                                        <div className="student-badges-dashboard">
                                                            <span className="student-xp-badge-dashboard">
                                                                <TrendingUp size={12} />
                                                                {student.xp} XP
                                                            </span>
                                                            <span className="student-pillars-badge-dashboard">
                                                                <CheckCircle size={12} />
                                                                {student.pillarsCompleted} Pillars
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </GlassCard>
                                </motion.div>
                            </>
                        ) : (
                            <GlassCard className="empty-state-card">
                                <div className="empty-state">
                                    <UserCheck size={64} />
                                    <p>Select a mentor to view details</p>
                                </div>
                            </GlassCard>
                        )}
                    </div>
                </div>

                {/* Expanded Mentor Cards with Students */}
                <div className="mentors-expanded-grid">
                    {filteredMentors.map((mentor) => (
                        <motion.div
                            key={mentor.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                        >
                            <GlassCard>
                                <div className="mentor-card-expanded">
                                    <div
                                        className="mentor-card-header"
                                        onClick={() => setExpandedMentor(expandedMentor === mentor.id ? null : mentor.id)}
                                        style={{ cursor: 'pointer' }}
                                    >
                                        <div className="mentor-card-info">
                                            <div className="mentor-avatar-large">
                                                <UserCheck size={32} />
                                            </div>
                                            <div>
                                                <h3>{mentor.name}</h3>
                                                <p className="mentor-department">{mentor.department}</p>
                                                <p className="mentor-contact">{mentor.email}</p>
                                            </div>
                                        </div>
                                        <button className="expand-btn">
                                            {expandedMentor === mentor.id ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
                                        </button>
                                    </div>

                                    <div className="mentor-quick-stats">
                                        <div className="quick-stat">
                                            <Users size={20} />
                                            <span>{mentor.studentsHandled} Students</span>
                                        </div>
                                        <div className="quick-stat">
                                            <CheckCircle size={20} />
                                            <span>{mentor.verificationsCompleted} Verified</span>
                                        </div>
                                        <div className="quick-stat">
                                            <Clock size={20} />
                                            <span>{mentor.avgResponseTime}</span>
                                        </div>
                                    </div>

                                    {expandedMentor === mentor.id && (
                                        <motion.div
                                            className="mentor-students-section"
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: 'auto', opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                        >
                                            <h4>Assigned Students</h4>
                                            <div className="students-grid">
                                                {mentor.students.map((student) => (
                                                    <div key={student.id} className="student-card">
                                                        <div className="student-avatar-small">
                                                            {student.name.split(' ').map(n => n[0]).join('')}
                                                        </div>
                                                        <div className="student-details">
                                                            <p className="student-name">{student.name}</p>
                                                            <p className="student-xp">{student.xp} XP</p>
                                                            <p className="student-pillars">{student.pillarsCompleted} pillars completed</p>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </motion.div>
                                    )}
                                </div>
                            </GlassCard>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MentorProfiles;
