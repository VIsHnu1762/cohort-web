import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search, User, Mail, Phone, Calendar, MapPin, Award, Target,
    TrendingUp, Edit, Save, X, Plus, Minus, CheckCircle, XCircle,
    Linkedin, Code, Heart, Lightbulb, Trophy, Book
} from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import './StudentProfiles.css';

const StudentProfiles = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [editedXP, setEditedXP] = useState('');
    const [xpAdjustment, setXPAdjustment] = useState('');
    const [adjustmentReason, setAdjustmentReason] = useState('');

    // Mock student data
    const students = [
        {
            id: 1,
            name: 'Amal R',
            email: 'amal@student.com',
            phone: '+91 98765 43210',
            registerNumber: 'CS101',
            department: 'Computer Science',
            year: '3rd Year',
            floor: 'Floor A',
            xp: 1250,
            badges: ['Top Contributor', 'Early Bird', 'Consistency Champion'],
            submissions: {
                total: 45,
                approved: 38,
                pending: 5,
                rejected: 2
            },
            pillars: {
                CLT: { completed: 12, pending: 2, xp: 350 },
                SRI: { completed: 8, pending: 1, xp: 280 },
                CFC: { completed: 10, pending: 2, xp: 320 },
                IIPC: { completed: 5, pending: 0, xp: 200 },
                SCD: { completed: 3, pending: 0, xp: 100 }
            },
            linkedinStats: {
                posts: 15,
                connections: 250,
                engagement: '85%'
            },
            leetcodeStats: {
                problemsSolved: 120,
                rank: '450K',
                contests: 8
            },
            mentorFeedback: [
                { date: '2025-12-01', mentor: 'Dr. Smith', feedback: 'Excellent progress in CLT submissions' },
                { date: '2025-11-28', mentor: 'Prof. Johnson', feedback: 'Good engagement in SRI activities' }
            ]
        },
        {
            id: 2,
            name: 'Priya S',
            email: 'priya@student.com',
            phone: '+91 98765 43211',
            registerNumber: 'CS102',
            department: 'Computer Science',
            year: '3rd Year',
            floor: 'Floor B',
            xp: 980,
            badges: ['Team Player', 'Quick Learner'],
            submissions: {
                total: 35,
                approved: 30,
                pending: 3,
                rejected: 2
            },
            pillars: {
                CLT: { completed: 10, pending: 1, xp: 300 },
                SRI: { completed: 7, pending: 2, xp: 250 },
                CFC: { completed: 8, pending: 0, xp: 260 },
                IIPC: { completed: 6, pending: 0, xp: 220 },
                SCD: { completed: 4, pending: 0, xp: 150 }
            },
            linkedinStats: {
                posts: 12,
                connections: 180,
                engagement: '72%'
            },
            leetcodeStats: {
                problemsSolved: 95,
                rank: '520K',
                contests: 5
            },
            mentorFeedback: [
                { date: '2025-12-05', mentor: 'Dr. Smith', feedback: 'Consistent performer across all pillars' }
            ]
        }
    ];

    const filteredStudents = students.filter(student =>
        student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.registerNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleXPAdjustment = (type) => {
        if (!xpAdjustment || !adjustmentReason) {
            alert('Please enter XP amount and reason');
            return;
        }

        const amount = parseInt(xpAdjustment);
        const newXP = type === 'add' ? selectedStudent.xp + amount : selectedStudent.xp - amount;

        console.log(`${type === 'add' ? 'Adding' : 'Removing'} ${amount} XP`);
        console.log(`Reason: ${adjustmentReason}`);
        console.log(`New XP: ${newXP}`);

        // Update local state (in production, make API call)
        setSelectedStudent({ ...selectedStudent, xp: newXP });
        setXPAdjustment('');
        setAdjustmentReason('');
        alert(`Successfully ${type === 'add' ? 'awarded' : 'deducted'} ${amount} XP`);
    };

    const pillarIcons = {
        CLT: Lightbulb,
        SRI: Heart,
        CFC: Trophy,
        IIPC: Linkedin,
        SCD: Code
    };

    const pillarColors = {
        CLT: '#ffcc00',
        SRI: '#ffcc00',
        CFC: '#42A5F5',
        IIPC: '#66BB6A',
        SCD: '#AB47BC'
    };

    return (
        <div className="student-profiles-page">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div>
                    <h1 className="page-title">Student Profile Management</h1>
                    <p className="page-subtitle">Search, view, and manage student profiles and XP</p>
                </div>
            </motion.div>

            <div className="profiles-layout">
                {/* Left Panel - Student List */}
                <motion.div
                    className="students-list-panel"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    <GlassCard variant="large">
                        <div className="search-section">
                            <Input
                                type="text"
                                placeholder="Search by name, register number, or email..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                icon={<Search size={20} />}
                            />
                        </div>

                        <div className="students-list">
                            {filteredStudents.map((student) => (
                                <motion.div
                                    key={student.id}
                                    className={`student-item ${selectedStudent?.id === student.id ? 'active' : ''}`}
                                    onClick={() => {
                                        setSelectedStudent(student);
                                        setIsEditing(false);
                                    }}
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <div className="student-avatar">
                                        <User size={24} />
                                    </div>
                                    <div className="student-info">
                                        <h3 className="student-name">{student.name}</h3>
                                        <p className="student-register">{student.registerNumber}</p>
                                        <p className="student-xp">{student.xp} XP</p>
                                    </div>
                                    <div className="student-status">
                                        <span className="pending-count">{student.submissions.pending} pending</span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </GlassCard>
                </motion.div>

                {/* Right Panel - Student Details */}
                <motion.div
                    className="student-details-panel"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    <AnimatePresence mode="wait">
                        {selectedStudent ? (
                            <motion.div
                                key={selectedStudent.id}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <GlassCard variant="large">
                                    <div className="profile-header">
                                        <div className="profile-avatar-large">
                                            <User size={48} />
                                        </div>
                                        <div className="profile-header-info">
                                            <h2 className="profile-name">{selectedStudent.name}</h2>
                                            <div className="profile-meta">
                                                <span><Mail size={16} /> {selectedStudent.email}</span>
                                                <span><Phone size={16} /> {selectedStudent.phone}</span>
                                                <span><Book size={16} /> {selectedStudent.registerNumber}</span>
                                            </div>
                                            <div className="profile-meta">
                                                <span><MapPin size={16} /> {selectedStudent.floor}</span>
                                                <span><Calendar size={16} /> {selectedStudent.year}</span>
                                            </div>
                                        </div>
                                        <Button
                                            variant="secondary"
                                            onClick={() => setIsEditing(!isEditing)}
                                        >
                                            {isEditing ? <X size={18} /> : <Edit size={18} />}
                                            {isEditing ? 'Cancel' : 'Edit Profile'}
                                        </Button>
                                    </div>

                                    {/* XP Management Section */}
                                    <div className="xp-management-section">
                                        <div className="xp-display">
                                            <div className="xp-icon">
                                                <Award size={32} color="#ffcc00" />
                                            </div>
                                            <div>
                                                <h3 className="xp-value">{selectedStudent.xp} XP</h3>
                                                <p className="xp-label">Total Experience Points</p>
                                            </div>
                                        </div>

                                        {isEditing && (
                                            <motion.div
                                                className="xp-adjustment"
                                                initial={{ opacity: 0, height: 0 }}
                                                animate={{ opacity: 1, height: 'auto' }}
                                            >
                                                <Input
                                                    type="number"
                                                    placeholder="XP Amount"
                                                    value={xpAdjustment}
                                                    onChange={(e) => setXPAdjustment(e.target.value)}
                                                />
                                                <Input
                                                    type="text"
                                                    placeholder="Reason for adjustment"
                                                    value={adjustmentReason}
                                                    onChange={(e) => setAdjustmentReason(e.target.value)}
                                                />
                                                <div className="xp-buttons">
                                                    <Button
                                                        variant="primary"
                                                        onClick={() => handleXPAdjustment('add')}
                                                    >
                                                        <Plus size={18} /> Award XP
                                                    </Button>
                                                    <Button
                                                        variant="secondary"
                                                        onClick={() => handleXPAdjustment('remove')}
                                                    >
                                                        <Minus size={18} /> Deduct XP
                                                    </Button>
                                                </div>
                                            </motion.div>
                                        )}
                                    </div>

                                    {/* Badges */}
                                    <div className="profile-section">
                                        <h3 className="section-heading">
                                            <Trophy size={20} /> Badges
                                        </h3>
                                        <div className="badges-grid">
                                            {selectedStudent.badges.map((badge, index) => (
                                                <div key={index} className="badge-item">
                                                    <Award size={16} />
                                                    {badge}
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Submissions Overview */}
                                    <div className="profile-section">
                                        <h3 className="section-heading">
                                            <Target size={20} /> Submissions Overview
                                        </h3>
                                        <div className="submissions-stats">
                                            <div className="stat-box">
                                                <div className="stat-icon-wrapper" style={{ background: '#4CAF5020' }}>
                                                    <CheckCircle size={20} color="#4CAF50" />
                                                </div>
                                                <div>
                                                    <p className="stat-value">{selectedStudent.submissions.approved}</p>
                                                    <p className="stat-label">Approved</p>
                                                </div>
                                            </div>
                                            <div className="stat-box">
                                                <div className="stat-icon-wrapper" style={{ background: '#FF980020' }}>
                                                    <TrendingUp size={20} color="#FF9800" />
                                                </div>
                                                <div>
                                                    <p className="stat-value">{selectedStudent.submissions.pending}</p>
                                                    <p className="stat-label">Pending</p>
                                                </div>
                                            </div>
                                            <div className="stat-box">
                                                <div className="stat-icon-wrapper" style={{ background: '#F4433620' }}>
                                                    <XCircle size={20} color="#F44336" />
                                                </div>
                                                <div>
                                                    <p className="stat-value">{selectedStudent.submissions.rejected}</p>
                                                    <p className="stat-label">Rejected</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Pillar Progress */}
                                    <div className="profile-section">
                                        <h3 className="section-heading">Pillar Completion Status</h3>
                                        <div className="pillars-grid">
                                            {Object.entries(selectedStudent.pillars).map(([pillar, data]) => {
                                                const Icon = pillarIcons[pillar];
                                                const color = pillarColors[pillar];
                                                return (
                                                    <div key={pillar} className="pillar-card">
                                                        <div className="pillar-header">
                                                            <Icon size={24} color={color} />
                                                            <span className="pillar-name">{pillar}</span>
                                                        </div>
                                                        <div className="pillar-stats">
                                                            <div className="pillar-stat">
                                                                <span>Completed:</span>
                                                                <strong>{data.completed}</strong>
                                                            </div>
                                                            <div className="pillar-stat">
                                                                <span>Pending:</span>
                                                                <strong>{data.pending}</strong>
                                                            </div>
                                                            <div className="pillar-stat">
                                                                <span>XP:</span>
                                                                <strong style={{ color }}>{data.xp}</strong>
                                                            </div>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    {/* LinkedIn & LeetCode Stats */}
                                    <div className="profile-section">
                                        <h3 className="section-heading">External Platform Stats</h3>
                                        <div className="external-stats">
                                            <div className="external-stat-card">
                                                <Linkedin size={24} color="#0077B5" />
                                                <h4>LinkedIn</h4>
                                                <div className="external-details">
                                                    <p>Posts: <strong>{selectedStudent.linkedinStats.posts}</strong></p>
                                                    <p>Connections: <strong>{selectedStudent.linkedinStats.connections}</strong></p>
                                                    <p>Engagement: <strong>{selectedStudent.linkedinStats.engagement}</strong></p>
                                                </div>
                                            </div>
                                            <div className="external-stat-card">
                                                <Code size={24} color="#FFA116" />
                                                <h4>LeetCode</h4>
                                                <div className="external-details">
                                                    <p>Solved: <strong>{selectedStudent.leetcodeStats.problemsSolved}</strong></p>
                                                    <p>Rank: <strong>{selectedStudent.leetcodeStats.rank}</strong></p>
                                                    <p>Contests: <strong>{selectedStudent.leetcodeStats.contests}</strong></p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Mentor Feedback */}
                                    <div className="profile-section">
                                        <h3 className="section-heading">Recent Mentor Feedback</h3>
                                        <div className="feedback-list">
                                            {selectedStudent.mentorFeedback.map((feedback, index) => (
                                                <div key={index} className="feedback-item">
                                                    <div className="feedback-meta">
                                                        <span className="feedback-date">{feedback.date}</span>
                                                        <span className="feedback-mentor">by {feedback.mentor}</span>
                                                    </div>
                                                    <p className="feedback-text">{feedback.feedback}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </GlassCard>
                            </motion.div>
                        ) : (
                            <GlassCard variant="large">
                                <div className="no-selection">
                                    <User size={64} opacity={0.3} />
                                    <h3>Select a Student</h3>
                                    <p>Choose a student from the list to view their complete profile</p>
                                </div>
                            </GlassCard>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </div>
    );
};

export default StudentProfiles;
