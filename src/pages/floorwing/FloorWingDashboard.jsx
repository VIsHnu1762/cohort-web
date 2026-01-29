import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Users, CheckCircle, Clock, UserCheck, TrendingUp, Award, UserPlus,
    Megaphone, X, AlertCircle, ChevronRight, Filter, Search
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import NotificationBell from '../../components/NotificationBell';
import FloorWingGamificationPanel from '../../components/FloorWingGamificationPanel';
import floorWingService from '../../services/floorWing';
import { floorWingAnnouncementService } from '../../services/announcement';
import {
    StudentsView,
    MentorsView,
    AnnouncementsView,
    StudentDetailDrawer,
    AnnouncementModal
} from './FloorWingComponents';
import './FloorWingDashboard.css';

const PILLAR_COLORS = {
    cfc: '#F44336',
    clt: '#2196F3',
    sri: '#4CAF50',
    iipc: '#FF9800',
    scd: '#9C27B0'
};

const PILLAR_NAMES = {
    cfc: 'CFC',
    clt: 'CLT',
    sri: 'SRI',
    iipc: 'IIPC',
    scd: 'SCD'
};

function FloorWingDashboard() {
    const [loading, setLoading] = useState(true);
    const [dashboardData, setDashboardData] = useState(null);
    const [students, setStudents] = useState([]);
    const [mentors, setMentors] = useState([]);
    const [announcements, setAnnouncements] = useState([]);
    const [activeView, setActiveView] = useState('dashboard');
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [assignmentMode, setAssignmentMode] = useState(false);
    const [showAnnouncementModal, setShowAnnouncementModal] = useState(false);
    const [studentFilter, setStudentFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedStudents, setSelectedStudents] = useState([]);
    
    // Announcement form state
    const [announcementForm, setAnnouncementForm] = useState({
        title: '',
        message: '',
        priority: 'normal',
        status: 'published'
    });

    useEffect(() => {
        loadDashboard();
        loadStudents();
        loadMentors();
        loadAnnouncements();
    }, []);

    const loadDashboard = async () => {
        try {
            const data = await floorWingService.getDashboard();
            setDashboardData(data);
        } catch (error) {
            console.error('Failed to load dashboard:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadStudents = async (filter = 'all') => {
        try {
            const params = filter !== 'all' ? { filter } : {};
            const data = await floorWingService.getStudents(params);
            setStudents(data.students || []);
        } catch (error) {
            console.error('Failed to load students:', error);
        }
    };

    const loadMentors = async () => {
        try {
            const data = await floorWingService.getMentors();
            setMentors(data.mentors || []);
        } catch (error) {
            console.error('Failed to load mentors:', error);
        }
    };

    const loadAnnouncements = async () => {
        try {
            const data = await floorWingAnnouncementService.getAnnouncements();
            setAnnouncements(data.results || data || []);
        } catch (error) {
            console.error('Failed to load announcements:', error);
        }
    };

    const handleAssignStudent = async (studentId, mentorId) => {
        try {
            await floorWingService.assignStudent(studentId, mentorId);
            await loadStudents(studentFilter);
            await loadDashboard();
            setAssignmentMode(false);
            setSelectedStudent(null);
        } catch (error) {
            console.error('Failed to assign student:', error);
            alert('Failed to assign student to mentor');
        }
    };

    const handleBulkAssign = async (mentorId) => {
        try {
            for (const studentId of selectedStudents) {
                await floorWingService.assignStudent(studentId, mentorId);
            }
            setSelectedStudents([]);
            await loadStudents(studentFilter);
            await loadDashboard();
            alert('Students assigned successfully');
        } catch (error) {
            console.error('Failed to bulk assign:', error);
            alert('Failed to assign students');
        }
    };

    const handleCreateAnnouncement = async (e) => {
        e.preventDefault();
        try {
            await floorWingAnnouncementService.createAnnouncement(announcementForm);
            setShowAnnouncementModal(false);
            setAnnouncementForm({
                title: '',
                message: '',
                priority: 'normal',
                status: 'published'
            });
            await loadAnnouncements();
            alert('Announcement created successfully');
        } catch (error) {
            console.error('Failed to create announcement:', error);
            const errorMsg = error.response?.data ? JSON.stringify(error.response.data) : error.message;
            alert('Failed to create announcement: ' + errorMsg);
        }
    };

    const handleFilterChange = (filter) => {
        setStudentFilter(filter);
        loadStudents(filter);
    };

    const toggleStudentSelection = (studentId) => {
        setSelectedStudents(prev =>
            prev.includes(studentId)
                ? prev.filter(id => id !== studentId)
                : [...prev, studentId]
        );
    };

    const filteredStudents = students.filter(student => {
        if (!searchTerm) return true;
        const search = searchTerm.toLowerCase();
        return (
            student.name?.toLowerCase().includes(search) ||
            student.email?.toLowerCase().includes(search) ||
            student.roll_no?.toLowerCase().includes(search)
        );
    });

    if (loading) {
        return (
            <div className="floorwing-dashboard">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const enhancedStats = dashboardData ? [
        { label: 'Total Students', value: dashboardData.total_students, icon: Users, color: '#2196F3' },
        { label: 'Active Mentors', value: dashboardData.total_mentors, icon: UserCheck, color: '#4CAF50' },
        { label: 'Assigned', value: dashboardData.assigned_students || 0, icon: CheckCircle, color: '#9C27B0' },
        { label: 'Unassigned', value: dashboardData.unassigned_students || 0, icon: Clock, color: '#FF9800' },
        { label: 'Avg Completion', value: `${dashboardData.avg_floor_completion || 0}%`, icon: TrendingUp, color: '#00BCD4' },
        { label: 'Pending Reviews', value: dashboardData.pending_mentor_reviews || 0, icon: AlertCircle, color: '#E91E63' },
    ] : [];

    return (
        <motion.div 
            className="floorwing-dashboard"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            {/* Header */}
            <motion.div
                className="floorwing-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="header-content">
                    <h1 className="floorwing-title">
                        {dashboardData?.campus_name} - Floor {dashboardData?.floor}
                    </h1>
                    <p className="floorwing-subtitle">
                        Floor Wing Management Dashboard
                    </p>
                </div>
                <NotificationBell />
            </motion.div>

            {/* Navigation Tabs */}
            <div className="floorwing-tabs">
                <motion.button
                    className={`tab ${activeView === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveView('dashboard')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Dashboard
                </motion.button>
                <motion.button
                    className={`tab ${activeView === 'students' ? 'active' : ''}`}
                    onClick={() => setActiveView('students')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Students
                </motion.button>
                <motion.button
                    className={`tab ${activeView === 'mentors' ? 'active' : ''}`}
                    onClick={() => setActiveView('mentors')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Mentors
                </motion.button>
                <motion.button
                    className={`tab ${activeView === 'announcements' ? 'active' : ''}`}
                    onClick={() => setActiveView('announcements')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Announcements
                    {announcements.length > 0 && (
                        <span className="tab-badge">{announcements.length}</span>
                    )}
                </motion.button>
            </div>

            {/* Content */}
            <AnimatePresence mode="wait">
                {activeView === 'dashboard' && (
                    <motion.div
                        key="dashboard"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        {/* Gamification Panel */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                        >
                            <FloorWingGamificationPanel />
                        </motion.div>

                        {/* Stats Cards */}
                        <div className="stats-grid">
                            {enhancedStats.map((stat, index) => {
                                const Icon = stat.icon;
                                return (
                                    <motion.div
                                        key={stat.label}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <GlassCard className="stat-card">
                                            <div className="stat-icon" style={{ background: `${stat.color}20`, color: stat.color }}>
                                                <Icon size={28} />
                                            </div>
                                            <div className="stat-details">
                                                <span className="stat-label">{stat.label}</span>
                                                <span className="stat-value">{stat.value}</span>
                                            </div>
                                        </GlassCard>
                                    </motion.div>
                                );
                            })}
                        </div>

                        {/* Floor Progress Overview */}
                        <GlassCard>
                            <h2 className="section-title">
                                <TrendingUp size={24} />
                                Floor Progress Overview
                            </h2>
                            <div className="pillar-progress-section">
                                {dashboardData?.pillar_stats && Object.entries(dashboardData.pillar_stats).length > 0 ? (
                                    Object.entries(dashboardData.pillar_stats).map(([pillarId, data]) => (
                                        <div key={pillarId} className="pillar-row">
                                            <div className="pillar-info">
                                                <span className="pillar-name">{PILLAR_NAMES[pillarId] || pillarId.toUpperCase()}</span>
                                            </div>
                                            <div className="pillar-progress-container">
                                                <div className="pillar-progress-bar">
                                                    <motion.div
                                                        className="pillar-progress-fill"
                                                        style={{ background: PILLAR_COLORS[pillarId] }}
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${data.completion_rate || 0}%` }}
                                                        transition={{ duration: 0.8, delay: 0.2 }}
                                                    />
                                                </div>
                                                <span className="pillar-percentage">{data.completion_rate || 0}%</span>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="empty-state-small">
                                        <AlertCircle size={32} opacity={0.5} />
                                        <p>Pillar progress data will appear here</p>
                                    </div>
                                )}
                            </div>
                        </GlassCard>

                        {/* Mentor Workload */}
                        <GlassCard>
                            <h2 className="section-title">
                                <UserCheck size={24} />
                                Mentor Workload Overview
                            </h2>
                            {mentors && mentors.length > 0 ? (
                                <div className="mentor-workload-grid">
                                    {mentors.slice(0, 6).map(mentor => (
                                        <div key={mentor.id} className="mentor-workload-card">
                                            <div className="mentor-workload-header">
                                                <h4>{mentor.name}</h4>
                                                <span className={`workload-badge ${mentor.workload_status || 'balanced'}`}>
                                                    {mentor.workload_status === 'low' ? 'Low' :
                                                     mentor.workload_status === 'overloaded' ? 'Overloaded' : 'Balanced'}
                                                </span>
                                            </div>
                                            <div className="mentor-workload-stats">
                                                <div className="workload-stat">
                                                    <span className="workload-value">{mentor.assigned_students_count || 0}</span>
                                                    <span className="workload-label">Students</span>
                                                </div>
                                                <div className="workload-stat">
                                                    <span className="workload-value">{mentor.pending_reviews || 0}</span>
                                                    <span className="workload-label">Pending</span>
                                                </div>
                                                <div className="workload-stat">
                                                    <span className="workload-value">{mentor.approval_rate || 0}%</span>
                                                    <span className="workload-label">Approved</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="empty-state-small">
                                    <UserCheck size={32} opacity={0.5} />
                                    <p>Mentor workload data will appear here</p>
                                </div>
                            )}
                        </GlassCard>
                    </motion.div>
                )}

                {activeView === 'students' && (
                    <StudentsView
                        students={filteredStudents}
                        mentors={mentors}
                        filter={studentFilter}
                        onFilterChange={handleFilterChange}
                        searchTerm={searchTerm}
                        onSearchChange={setSearchTerm}
                        selectedStudents={selectedStudents}
                        onToggleSelection={toggleStudentSelection}
                        onAssign={handleAssignStudent}
                        onBulkAssign={handleBulkAssign}
                        onStudentClick={setSelectedStudent}
                    />
                )}

                {activeView === 'mentors' && (
                    <MentorsView mentors={mentors} />
                )}

                {activeView === 'announcements' && (
                    <AnnouncementsView
                        announcements={announcements}
                        onRefresh={loadAnnouncements}
                        onCreate={() => setShowAnnouncementModal(true)}
                    />
                )}
            </AnimatePresence>

            {/* Student Detail Drawer */}
            <AnimatePresence>
                {selectedStudent && (
                    <StudentDetailDrawer
                        student={selectedStudent}
                        mentors={mentors}
                        onClose={() => setSelectedStudent(null)}
                        onAssign={handleAssignStudent}
                    />
                )}
            </AnimatePresence>

            {/* Announcement Modal */}
            <AnimatePresence>
                {showAnnouncementModal && (
                    <AnnouncementModal
                        form={announcementForm}
                        onChange={setAnnouncementForm}
                        onSubmit={handleCreateAnnouncement}
                        onClose={() => setShowAnnouncementModal(false)}
                    />
                )}
            </AnimatePresence>
        </motion.div>
    );
}

export default FloorWingDashboard;
