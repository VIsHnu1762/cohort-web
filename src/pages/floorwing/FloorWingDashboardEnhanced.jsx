import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Users, CheckCircle, Clock, UserCheck, TrendingUp, Award, UserPlus,
    Megaphone, X, AlertCircle, ChevronRight, Filter, Search
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
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
                    <div className="spinner"></div>
                    <p>Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const enhancedStats = dashboardData ? [
        { label: 'Total Students', value: dashboardData.total_students, icon: Users, color: '#2196F3' },
        { label: 'Total Mentors', value: dashboardData.total_mentors, icon: UserCheck, color: '#4CAF50' },
        { label: 'Assigned Students', value: dashboardData.assigned_students || 0, icon: CheckCircle, color: '#9C27B0' },
        { label: 'Unassigned Students', value: dashboardData.unassigned_students || 0, icon: Clock, color: '#FF9800' },
        { label: 'Avg Completion', value: `${dashboardData.avg_floor_completion || 0}%`, icon: TrendingUp, color: '#00BCD4' },
        { label: 'Pending Reviews', value: dashboardData.pending_mentor_reviews || 0, icon: AlertCircle, color: '#E91E63' },
    ] : [];

    return (
        <div className="floorwing-dashboard">
            {/* Header */}
            <motion.div
                className="floorwing-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div>
                    <h1 className="floorwing-title">
                        {dashboardData?.campus_name} - Floor {dashboardData?.floor}
                    </h1>
                    <p className="floorwing-subtitle">
                        {dashboardData?.floor_name} Wing Management Dashboard
                    </p>
                </div>
                <Button
                    variant="primary"
                    onClick={() => setShowAnnouncementModal(true)}
                >
                    <Megaphone size={18} />
                    Create Announcement
                </Button>
            </motion.div>

            {/* Navigation Tabs */}
            <div className="floorwing-tabs">
                <button
                    className={`tab ${activeView === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveView('dashboard')}
                >
                    Dashboard
                </button>
                <button
                    className={`tab ${activeView === 'students' ? 'active' : ''}`}
                    onClick={() => setActiveView('students')}
                >
                    Students
                </button>
                <button
                    className={`tab ${activeView === 'mentors' ? 'active' : ''}`}
                    onClick={() => setActiveView('mentors')}
                >
                    Mentors
                </button>
                <button
                    className={`tab ${activeView === 'announcements' ? 'active' : ''}`}
                    onClick={() => setActiveView('announcements')}
                >
                    Announcements
                    {announcements.length > 0 && (
                        <span className="tab-badge">{announcements.length}</span>
                    )}
                </button>
            </div>

            {/* Content */}
            <AnimatePresence mode="wait">
                {activeView === 'dashboard' && (
                    <DashboardView
                        stats={enhancedStats}
                        dashboardData={dashboardData}
                        mentors={mentors}
                    />
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
        </div>
    );
}

// Dashboard View Component
function DashboardView({ stats, dashboardData, mentors }) {
    return (
        <motion.div
            key="dashboard"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="floorwing-content"
        >
            {/* Enhanced Stats Cards */}
            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <GlassCard className="stat-card">
                            <div className="stat-icon" style={{ backgroundColor: `${stat.color}20`, color: stat.color }}>
                                <stat.icon size={24} />
                            </div>
                            <div className="stat-content">
                                <div className="stat-value">{stat.value}</div>
                                <div className="stat-label">{stat.label}</div>
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>

            {/* Floor Progress Overview */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
            >
                <GlassCard>
                    <h2 className="section-title">Floor Progress Overview</h2>
                    <div className="pillar-progress-grid">
                        {dashboardData?.pillar_stats && Object.entries(dashboardData.pillar_stats).map(([pillar, stats]) => (
                            <div key={pillar} className="pillar-progress-card">
                                <div className="pillar-header">
                                    <span className="pillar-name" style={{ color: PILLAR_COLORS[pillar] }}>
                                        {PILLAR_NAMES[pillar]}
                                    </span>
                                    <span className="pillar-completion">{stats.completion_rate || 0}%</span>
                                </div>
                                <div className="pillar-progress-bar">
                                    <div
                                        className="pillar-progress-fill"
                                        style={{
                                            width: `${stats.completion_rate || 0}%`,
                                            backgroundColor: PILLAR_COLORS[pillar]
                                        }}
                                    />
                                </div>
                                <div className="pillar-stats-mini">
                                    <span className="mini-stat approved">{stats.approved || 0} ✓</span>
                                    <span className="mini-stat pending">{stats.pending || 0} ⏳</span>
                                    <span className="mini-stat rejected">{stats.rejected || 0} ✗</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </GlassCard>
            </motion.div>

            {/* Mentor Workload Visualization */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
            >
                <GlassCard>
                    <h2 className="section-title">Mentor Workload Status</h2>
                    <div className="mentor-workload-grid">
                        {mentors.map((mentor) => (
                            <div key={mentor.id} className="mentor-workload-card">
                                <div className="mentor-workload-header">
                                    <div>
                                        <h3 className="mentor-name">{mentor.name}</h3>
                                        <p className="mentor-email">{mentor.email}</p>
                                    </div>
                                    <span className={`workload-badge ${mentor.workload_status || 'balanced'}`}>
                                        {mentor.workload_status || 'Balanced'}
                                    </span>
                                </div>
                                <div className="mentor-workload-stats">
                                    <div className="workload-stat">
                                        <Users size={16} />
                                        <span>{mentor.assigned_students_count || 0} Students</span>
                                    </div>
                                    <div className="workload-stat">
                                        <Clock size={16} />
                                        <span>{mentor.pending_reviews || 0} Pending</span>
                                    </div>
                                    <div className="workload-stat">
                                        <CheckCircle size={16} />
                                        <span>{mentor.approval_rate || 0}% Approved</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </GlassCard>
            </motion.div>
        </motion.div>
    );
}

// Due to length, I'll continue in the next file with the remaining components...

export default FloorWingDashboard;
