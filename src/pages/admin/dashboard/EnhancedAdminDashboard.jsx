import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Users, UserCheck, Trophy, Bell, Shield, Settings,
    TrendingUp, CheckCircle, XCircle, Clock, Award, Building2,
    User, Zap, Target, Medal, Calendar, X, Heart
} from 'lucide-react';
import {
    BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import GlassCard from '../../../components/GlassCard';
import { dashboardStats, analyticsData, mentorsData, floorsData } from '../../../data/mockAdminData';
import { useAuth } from '../../../context/AuthContext';
import snsctLogo from '../../../assets/snsct.jpeg';
import snscasLogo from '../../../assets/snscas.jpeg';
import './SimpleDashboard.css';

function EnhancedAdminDashboard() {
    const navigate = useNavigate();
    const { user } = useAuth();
    const [stats, setStats] = useState(dashboardStats);
    const [loading, setLoading] = useState(true);
    const [selectedTeam, setSelectedTeam] = useState(null);
    const [likes, setLikes] = useState({});

    // Fetch real-time stats from API
    const fetchStats = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/profiles/admin/stats/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setStats(data);
            }
        } catch (error) {
            console.error('Error fetching admin stats:', error);
        } finally {
            setLoading(false);
        }
    };

    // Fetch stats on mount and set up auto-refresh every 30 seconds
    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    // Chart colors matching brand
    const COLORS = ['#ffcc00', '#ffcc00', '#FFC107', '#FF5722', '#4CAF50'];

    // Top performers
    const topMentors = mentorsData
        .sort((a, b) => b.approvalRate - a.approvalRate)
        .slice(0, 3);

    const lowestFloor = floorsData
        .sort((a, b) => a.performanceScore - b.performanceScore)[0];

    // Hackathon Spotlight Teams Data
    const hackathonTeams = [
        {
            id: 1,
            teamName: "Code Crusaders",
            hackathon: "Smart City Hackathon 2024",
            achievement: "1st Place",
            position: "🥇",
            prize: "$5,000",
            project: "AI-Powered Traffic Management System",
            description: "An intelligent system that optimizes traffic flow using machine learning algorithms and real-time data analysis.",
            date: "15 Nov 2024",
            members: [
                { name: "Rahul Sharma", role: "Team Lead", avatar: "https://ui-avatars.com/api/?name=Rahul+Sharma&background=F7C948&color=000" },
                { name: "Priya Patel", role: "Frontend Dev", avatar: "https://ui-avatars.com/api/?name=Priya+Patel&background=E53935&color=fff" },
                { name: "Arjun Kumar", role: "Backend Dev", avatar: "https://ui-avatars.com/api/?name=Arjun+Kumar&background=FFC107&color=000" },
                { name: "Neha Singh", role: "UI/UX Designer", avatar: "https://ui-avatars.com/api/?name=Neha+Singh&background=4CAF50&color=fff" }
            ],
            score: 98,
            likes: 469,
            color: '#ffcc00',
            logo: "https://ui-avatars.com/api/?name=CC&background=F7C948&color=000&size=120&bold=true"
        },
        {
            id: 2,
            teamName: "Tech Titans",
            hackathon: "Healthcare Innovation Challenge",
            achievement: "2nd Place",
            position: "🥈",
            prize: "$3,000",
            project: "Telemedicine Platform with AI Diagnosis",
            description: "A comprehensive telemedicine solution featuring AI-powered preliminary diagnosis and remote patient monitoring.",
            date: "22 Oct 2024",
            members: [
                { name: "Amit Verma", role: "Full Stack Dev", avatar: "https://ui-avatars.com/api/?name=Amit+Verma&background=E53935&color=fff" },
                { name: "Sneha Das", role: "AI Engineer", avatar: "https://ui-avatars.com/api/?name=Sneha+Das&background=F7C948&color=000" },
                { name: "Karan Joshi", role: "DevOps", avatar: "https://ui-avatars.com/api/?name=Karan+Joshi&background=FFC107&color=000" }
            ],
            score: 95,
            likes: 223,
            color: '#ffcc00',
            logo: "https://ui-avatars.com/api/?name=TT&background=E53935&color=fff&size=120&bold=true"
        },
        {
            id: 3,
            teamName: "Innovation Squad",
            hackathon: "Green Tech Summit",
            achievement: "3rd Place",
            position: "🥉",
            prize: "$2,000",
            project: "Carbon Footprint Tracker",
            description: "Mobile application to track and reduce personal carbon footprint with gamification and social features.",
            date: "08 Sep 2024",
            members: [
                { name: "Vikram Singh", role: "Mobile Dev", avatar: "https://ui-avatars.com/api/?name=Vikram+Singh&background=FFC107&color=000" },
                { name: "Anjali Reddy", role: "Backend Dev", avatar: "https://ui-avatars.com/api/?name=Anjali+Reddy&background=4CAF50&color=fff" },
                { name: "Rohan Mehta", role: "Data Scientist", avatar: "https://ui-avatars.com/api/?name=Rohan+Mehta&background=E53935&color=fff" },
                { name: "Divya Iyer", role: "Product Manager", avatar: "https://ui-avatars.com/api/?name=Divya+Iyer&background=F7C948&color=000" }
            ],
            score: 92,
            likes: 226,
            color: '#FFC107',
            logo: "https://ui-avatars.com/api/?name=IS&background=FFC107&color=000&size=120&bold=true"
        }
    ];

    const toggleLike = (teamId) => {
        setLikes(prev => ({
            ...prev,
            [teamId]: !prev[teamId]
        }));
    };

    return (
        <div className="admin-dashboard-enhanced">
            {/* Animated Background */}
            <div className="admin-background">
                <div className="admin-bg-gradient admin-bg-gradient-1"></div>
                <div className="admin-bg-gradient admin-bg-gradient-2"></div>
            </div>

            {/* Header Section */}
            <div className="admin-header-section">
                <div className="admin-header-logos">
                    <img src={snsctLogo} alt="SNSCT" className="admin-header-logo" />
                    <img src={snscasLogo} alt="SNSCAS" className="admin-header-logo" />
                </div>
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="admin-welcome"
                >
                    <h1>
                        Welcome back, <span className="admin-title-gradient">{user?.username || 'Admin'}!</span>
                    </h1>
                    <p>Here's what's happening with your cohort today</p>
                </motion.div>

                <motion.button
                    className="admin-profile-icon-btn"
                    onClick={() => navigate('/admin/settings')}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <User size={24} />
                </motion.button>
            </div>

            {/* Dashboard Content */}
            <div className="admin-dashboard-grid">
                {/* Left Column */}
                <div className="admin-left-column">
                    {/* Overall Stats Card */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <GlassCard>
                            <div className="admin-overall-stats">
                                <h2>Overall Statistics</h2>
                                <div className="admin-stats-grid">
                                    <div className="admin-stat-item" onClick={() => navigate('/admin/students')}>
                                        <div className="admin-stat-icon" style={{ backgroundColor: 'rgba(247, 201, 72, 0.2)' }}>
                                            <Users size={24} style={{ color: '#ffcc00' }} />
                                        </div>
                                        <div className="admin-stat-info">
                                            <span className="admin-stat-value">{stats.totalStudents}</span>
                                            <span className="admin-stat-label">Total Students</span>
                                            <span className="admin-stat-trend up">+8.5% vs last month</span>
                                        </div>
                                    </div>

                                    <div className="admin-stat-item" onClick={() => navigate('/admin/mentors')}>
                                        <div className="admin-stat-icon" style={{ backgroundColor: 'rgba(229, 57, 53, 0.2)' }}>
                                            <UserCheck size={24} style={{ color: '#ffcc00' }} />
                                        </div>
                                        <div className="admin-stat-info">
                                            <span className="admin-stat-value">{stats.totalMentors}</span>
                                            <span className="admin-stat-label">Total Mentors</span>
                                        </div>
                                    </div>

                                    <div className="admin-stat-item" onClick={() => navigate('/admin/submissions')}>
                                        <div className="admin-stat-icon" style={{ backgroundColor: 'rgba(255, 193, 7, 0.2)' }}>
                                            <Clock size={24} style={{ color: '#FFC107' }} />
                                        </div>
                                        <div className="admin-stat-info">
                                            <span className="admin-stat-value">{stats.pendingSubmissions}</span>
                                            <span className="admin-stat-label">Pending Submissions</span>
                                            <span className="admin-stat-trend down">-12.3% vs last week</span>
                                        </div>
                                    </div>

                                    <div className="admin-stat-item">
                                        <div className="admin-stat-icon" style={{ backgroundColor: 'rgba(76, 175, 80, 0.2)' }}>
                                            <Award size={24} style={{ color: '#4CAF50' }} />
                                        </div>
                                        <div className="admin-stat-info">
                                            <span className="admin-stat-value">{stats.xpGivenThisMonth.toLocaleString()}</span>
                                            <span className="admin-stat-label">XP This Month</span>
                                            <span className="admin-stat-trend up">+15.7% vs last month</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>

                    {/* Pillar Completion Chart */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        <GlassCard>
                            <div className="admin-chart-container">
                                <h2>Pillar Completion Rate</h2>
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={analyticsData.pillarCompletion}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
                                        <XAxis
                                            dataKey="pillar"
                                            stroke="#9CA3AF"
                                            style={{ fontSize: '12px' }}
                                        />
                                        <YAxis
                                            stroke="#9CA3AF"
                                            style={{ fontSize: '12px' }}
                                        />
                                        <Tooltip
                                            contentStyle={{
                                                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                                border: '1px solid #374151',
                                                borderRadius: '8px',
                                                color: '#fff'
                                            }}
                                        />
                                        <defs>
                                            <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="0%" stopColor="#ffcc00" />
                                                <stop offset="100%" stopColor="#ffcc00" />
                                            </linearGradient>
                                        </defs>
                                        <Bar dataKey="completion" fill="url(#barGradient)" radius={[8, 8, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </GlassCard>
                    </motion.div>
                </div>

                {/* Right Column */}
                <div className="admin-right-column">
                    {/* Quick Actions */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <GlassCard>
                            <div className="admin-quick-actions">
                                <h2>Quick Actions</h2>
                                <div className="admin-action-buttons">
                                    <button className="admin-action-btn primary" onClick={() => navigate('/admin/campus-select')}>
                                        <Building2 size={20} />
                                        <span>Campus Management</span>
                                    </button>
                                    <button className="admin-action-btn" onClick={() => navigate('/admin/students')}>
                                        <Users size={20} />
                                        <span>Manage Students</span>
                                    </button>
                                    <button className="admin-action-btn" onClick={() => navigate('/admin/mentors')}>
                                        <UserCheck size={20} />
                                        <span>Manage Mentors</span>
                                    </button>
                                    <button className="admin-action-btn" onClick={() => navigate('/admin/submissions')}>
                                        <CheckCircle size={20} />
                                        <span>Review Submissions</span>
                                    </button>
                                    <button className="admin-action-btn" onClick={() => navigate('/admin/leaderboard')}>
                                        <Trophy size={20} />
                                        <span>Leaderboard</span>
                                    </button>
                                    <button className="admin-action-btn" onClick={() => navigate('/admin/notifications')}>
                                        <Bell size={20} />
                                        <span>Send Notifications</span>
                                    </button>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>

                    {/* Hackathon Spotlight */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        <GlassCard>
                            <div className="hackathon-spotlight-container">
                                <div className="hackathon-header">
                                    <h2>
                                        <Trophy size={24} style={{ marginRight: '10px', color: '#ffcc00' }} />
                                        Projects Spotlight
                                    </h2>
                                    <p className="hackathon-subtitle">Celebrating our champion teams</p>
                                </div>

                                <div className="hackathon-projects-grid">
                                    {hackathonTeams.map((team, index) => (
                                        <motion.div
                                            key={team.id}
                                            className="project-card"
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: 0.1 * index }}
                                            onClick={() => setSelectedTeam(team)}
                                            whileHover={{ scale: 1.02 }}
                                        >
                                            <div className="project-logo">
                                                <img src={team.logo} alt={team.teamName} />
                                            </div>

                                            <div className="project-members-grid">
                                                {team.members.slice(0, 4).map((member, idx) => (
                                                    <div key={idx} className="member-avatar-small">
                                                        <img src={member.avatar} alt={member.name} title={member.name} />
                                                    </div>
                                                ))}
                                            </div>

                                            <div className="project-info">
                                                <h3 className="project-card-title">{team.teamName}</h3>
                                                <p className="project-card-desc">{team.project}</p>

                                                <div className="project-card-footer">
                                                    <button
                                                        className={`like-btn ${likes[team.id] ? 'liked' : ''}`}
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            toggleLike(team.id);
                                                        }}
                                                    >
                                                        <Heart size={18} fill={likes[team.id] ? '#ffcc00' : 'none'} />
                                                    </button>
                                                    <span className="likes-count">{team.likes + (likes[team.id] ? 1 : 0)}</span>
                                                </div>
                                            </div>
                                        </motion.div>
                                    ))}
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                </div>
            </div>

            {/* Team Details Modal */}
            <AnimatePresence>
                {selectedTeam && (
                    <motion.div
                        className="team-modal-overlay"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setSelectedTeam(null)}
                    >
                        <motion.div
                            className="team-modal-content"
                            initial={{ scale: 0.9, opacity: 0, y: 20 }}
                            animate={{ scale: 1, opacity: 1, y: 0 }}
                            exit={{ scale: 0.9, opacity: 0, y: 20 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <button className="modal-close-btn" onClick={() => setSelectedTeam(null)}>
                                <X size={24} />
                            </button>

                            <div className="modal-header">
                                <div className="modal-logo">
                                    <img src={selectedTeam.logo} alt={selectedTeam.teamName} />
                                </div>
                                <div className="modal-header-info">
                                    <h2 className="modal-team-name">{selectedTeam.teamName}</h2>
                                    <p className="modal-project-name">{selectedTeam.project}</p>
                                </div>
                                <div className="modal-like-section">
                                    <button
                                        className={`modal-like-btn ${likes[selectedTeam.id] ? 'liked' : ''}`}
                                        onClick={() => toggleLike(selectedTeam.id)}
                                    >
                                        <Heart size={24} fill={likes[selectedTeam.id] ? '#ffcc00' : 'none'} />
                                    </button>
                                    <span className="modal-likes-count">{selectedTeam.likes + (likes[selectedTeam.id] ? 1 : 0)}</span>
                                </div>
                            </div>

                            <div className="modal-body">
                                <div className="modal-section">
                                    <div className="modal-info-grid">
                                        <div className="modal-info-item">
                                            <Trophy size={20} style={{ color: selectedTeam.color }} />
                                            <div>
                                                <p className="info-label">Achievement</p>
                                                <p className="info-value">{selectedTeam.position} {selectedTeam.achievement}</p>
                                            </div>
                                        </div>

                                        <div className="modal-info-item">
                                            <Award size={20} style={{ color: '#ffcc00' }} />
                                            <div>
                                                <p className="info-label">Hackathon</p>
                                                <p className="info-value">{selectedTeam.hackathon}</p>
                                            </div>
                                        </div>

                                        <div className="modal-info-item">
                                            <Medal size={20} style={{ color: '#4CAF50' }} />
                                            <div>
                                                <p className="info-label">Prize</p>
                                                <p className="info-value">{selectedTeam.prize}</p>
                                            </div>
                                        </div>

                                        <div className="modal-info-item">
                                            <Calendar size={20} style={{ color: '#ffcc00' }} />
                                            <div>
                                                <p className="info-label">Date</p>
                                                <p className="info-value">{selectedTeam.date}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="modal-section">
                                    <h3 className="section-title">
                                        <Zap size={20} />
                                        Project Description
                                    </h3>
                                    <p className="project-description">{selectedTeam.description}</p>
                                </div>

                                <div className="modal-section">
                                    <h3 className="section-title">
                                        <Users size={20} />
                                        Team Members
                                    </h3>
                                    <div className="modal-members-grid">
                                        {selectedTeam.members.map((member, idx) => (
                                            <div key={idx} className="modal-member-card">
                                                <img src={member.avatar} alt={member.name} className="modal-member-avatar" />
                                                <div className="modal-member-info">
                                                    <p className="modal-member-name">{member.name}</p>
                                                    <p className="modal-member-role">{member.role}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="modal-section">
                                    <div className="modal-score-section">
                                        <div className="score-header">
                                            <Target size={20} />
                                            <span>Final Score</span>
                                        </div>
                                        <div className="score-display">
                                            <span className="score-number">{selectedTeam.score}</span>
                                            <span className="score-max">/100</span>
                                        </div>
                                        <div className="score-bar">
                                            <motion.div
                                                className="score-bar-fill"
                                                style={{ backgroundColor: selectedTeam.color }}
                                                initial={{ width: 0 }}
                                                animate={{ width: `${selectedTeam.score}%` }}
                                                transition={{ duration: 1, delay: 0.3 }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Bottom Section - Full Width Charts */}
            <div className="admin-bottom-section">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <GlassCard>
                        <div className="admin-chart-container">
                            <h2>Top Mentor Performance</h2>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={analyticsData.mentorPerformance.slice(0, 5)} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
                                    <XAxis
                                        type="number"
                                        stroke="#9CA3AF"
                                        style={{ fontSize: '12px' }}
                                    />
                                    <YAxis
                                        type="category"
                                        dataKey="name"
                                        stroke="#9CA3AF"
                                        style={{ fontSize: '11px' }}
                                        width={120}
                                    />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                            border: '1px solid #374151',
                                            borderRadius: '8px',
                                            color: '#fff'
                                        }}
                                    />
                                    <defs>
                                        <linearGradient id="mentorGradient" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#ffcc00" />
                                            <stop offset="100%" stopColor="#ffcc00" />
                                        </linearGradient>
                                    </defs>
                                    <Bar dataKey="approvalRate" fill="url(#mentorGradient)" radius={[0, 8, 8, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </GlassCard>
                </motion.div>
            </div>
        </div>
    );
}

export default EnhancedAdminDashboard;

