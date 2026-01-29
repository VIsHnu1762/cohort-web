import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Users, UserCheck, Crown, TrendingUp, FileText, X } from 'lucide-react';
import { getFloorDetail, assignFloorWing, assignMentor, getStudentDetail } from '../../../services/admin';
import GlassCard from '../../../components/GlassCard';
import './FloorDetail.css';

const FloorDetail = () => {
    const { campus, floor } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [floorData, setFloorData] = useState(null);
    const [selectedTab, setSelectedTab] = useState('students');
    const [assignmentMode, setAssignmentMode] = useState(null); // 'floor_wing' or 'mentor'
    const [selectedUser, setSelectedUser] = useState('');
    const [availableUsers, setAvailableUsers] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [studentDetail, setStudentDetail] = useState(null);
    const [loadingStudent, setLoadingStudent] = useState(false);

    useEffect(() => {
        loadFloorData();
    }, [campus, floor]);

    const loadFloorData = async () => {
        try {
            setLoading(true);
            const data = await getFloorDetail(campus, floor);
            setFloorData(data);
        } catch (error) {
            console.error('Error loading floor data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAssignFloorWing = async () => {
        if (!selectedUser) return;
        
        try {
            await assignFloorWing(campus, parseInt(floor), parseInt(selectedUser));
            setAssignmentMode(null);
            setSelectedUser('');
            loadFloorData();
        } catch (error) {
            console.error('Error assigning floor wing:', error);
            alert('Failed to assign floor wing: ' + (error.response?.data?.error || error.message));
        }
    };

    const handleAssignMentor = async () => {
        if (!selectedUser) return;
        
        try {
            await assignMentor(campus, parseInt(floor), parseInt(selectedUser));
            setAssignmentMode(null);
            setSelectedUser('');
            loadFloorData();
        } catch (error) {
            console.error('Error assigning mentor:', error);
            alert('Failed to assign mentor: ' + (error.response?.data?.error || error.message));
        }
    };

    const getUnassignedUsers = () => {
        if (!floorData) return [];
        
        if (assignmentMode === 'floor_wing') {
            // Get users who are not floor wings yet
            return floorData.students?.filter(s => !s.role || s.role === 'STUDENT') || [];
        } else if (assignmentMode === 'mentor') {
            // Get users who are not mentors yet or mentors without floor
            return floorData.students?.filter(s => 
                !s.role || s.role === 'STUDENT' || (s.role === 'MENTOR' && !s.floor)
            ) || [];
        }
        return [];
    };

    const handleStudentClick = async (student) => {
        setSelectedStudent(student);
        setLoadingStudent(true);
        setStudentDetail(null); // Clear previous data
        try {
            const details = await getStudentDetail(student.id);
            setStudentDetail(details);
        } catch (error) {
            console.error('Error loading student details:', error);
            alert('Failed to load student details');
            // Close drawer on error
            setSelectedStudent(null);
            setStudentDetail(null);
        } finally {
            setLoadingStudent(false);
        }
    };

    const closeStudentDrawer = () => {
        setSelectedStudent(null);
        setStudentDetail(null);
    };

    if (loading) {
        return (
            <div className="floor-detail-loading">
                <div className="spinner"></div>
                <p>Loading floor details...</p>
            </div>
        );
    }

    if (!floorData) {
        return (
            <div className="floor-detail-error">
                <p>Failed to load floor data</p>
                <button onClick={() => navigate(`/admin/campus/${campus}`)}>
                    Back to Campus
                </button>
            </div>
        );
    }

    const campusName = campus === 'TECH' ? 'SNS College of Technology' : 'Dr. SNS Rajalakshmi College of Arts and Science';

    return (
        <div className="floor-detail">
            <div className="floor-detail-header">
                <button 
                    className="back-button"
                    onClick={() => navigate(`/admin/campus/${campus}`)}
                >
                    <ArrowLeft size={20} />
                    Back to {campusName} Campus
                </button>
                
                <div className="floor-title">
                    <h1>{campusName} Campus - Floor {floor}</h1>
                    <p className="floor-subtitle">Manage students, mentors, and floor wing</p>
                </div>

                <div className="floor-stats-row">
                    <div className="stat-card">
                        <Users size={24} />
                        <div>
                            <div className="stat-value">{floorData.students?.length || 0}</div>
                            <div className="stat-label">Students</div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <UserCheck size={24} />
                        <div>
                            <div className="stat-value">{floorData.mentors?.length || 0}</div>
                            <div className="stat-label">Mentors</div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <Crown size={24} />
                        <div>
                            <div className="stat-value">{floorData.floor_wing ? '1' : '0'}</div>
                            <div className="stat-label">Floor Wing</div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <FileText size={24} />
                        <div>
                            <div className="stat-value">{floorData.total_submissions || 0}</div>
                            <div className="stat-label">Submissions</div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="floor-tabs">
                <button 
                    className={`tab-button ${selectedTab === 'students' ? 'active' : ''}`}
                    onClick={() => setSelectedTab('students')}
                >
                    <Users size={20} />
                    Students
                </button>
                <button 
                    className={`tab-button ${selectedTab === 'mentors' ? 'active' : ''}`}
                    onClick={() => setSelectedTab('mentors')}
                >
                    <UserCheck size={20} />
                    Mentors
                </button>
                <button 
                    className={`tab-button ${selectedTab === 'floorwing' ? 'active' : ''}`}
                    onClick={() => setSelectedTab('floorwing')}
                >
                    <Crown size={20} />
                    Floor Wing
                </button>
            </div>

            <div className="tab-content">
                {selectedTab === 'students' && (
                    <div className="students-grid">
                        {floorData.students && floorData.students.length > 0 ? (
                            floorData.students.map((student, index) => (
                                <motion.div
                                    key={student.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.3, delay: index * 0.05 }}
                                >
                                    <GlassCard hoverable onClick={() => handleStudentClick(student)}>
                                        <div className="student-card-item">
                                            <div className="student-header">
                                                <div className="student-info">
                                                    <h3>{student.name || student.user__username}</h3>
                                                    <p className="student-email">{student.email || student.user__email}</p>
                                                </div>
                                                <span className={`student-role ${(student.role || 'student').toLowerCase()}`}>
                                                    {student.role || 'Student'}
                                                </span>
                                            </div>
                                            <div className="student-details">
                                                <div className="detail-row">
                                                    <span className="detail-label">Roll No:</span>
                                                    <span className="detail-value">{student.roll_no || 'N/A'}</span>
                                                </div>
                                                <div className="detail-row">
                                                    <span className="detail-label">Mentor:</span>
                                                    <span className="detail-value">
                                                        {student.mentor || student.assigned_mentor?.name || 'Not Assigned'}
                                                    </span>
                                                </div>
                                                <div className="detail-row">
                                                    <span className="detail-label">Submissions:</span>
                                                    <span className="detail-value">{student.submissions || student.submission_count || 0}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </GlassCard>
                                </motion.div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <Users size={64} />
                                <h3>No Students Yet</h3>
                                <p>No students have been assigned to this floor</p>
                            </div>
                        )}
                    </div>
                )}

                {selectedTab === 'mentors' && (
                    <div>
                        {assignmentMode === 'mentor' && (
                            <GlassCard style={{ marginBottom: '2rem' }}>
                                <div className="assignment-form">
                                    <div className="form-group">
                                        <label>Select a user to assign as mentor</label>
                                        <select 
                                            value={selectedUser}
                                            onChange={(e) => setSelectedUser(e.target.value)}
                                        >
                                            <option value="">Choose a student...</option>
                                            {getUnassignedUsers().map((user) => (
                                                <option key={user.id} value={user.id}>
                                                    {user.name || user.user__username} ({user.email || user.user__email})
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                    <div className="form-actions">
                                        <button 
                                            className="assign-button" 
                                            onClick={handleAssignMentor} 
                                            disabled={!selectedUser}
                                        >
                                            Assign Mentor
                                        </button>
                                        <button 
                                            className="cancel-button"
                                            onClick={() => { setAssignmentMode(null); setSelectedUser(''); }}
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            </GlassCard>
                        )}

                        {floorData.mentors && floorData.mentors.length > 0 ? (
                            <div className="mentors-list">
                                {floorData.mentors.map((mentor, index) => (
                                    <motion.div
                                        key={mentor.id}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ duration: 0.3, delay: index * 0.05 }}
                                    >
                                        <GlassCard hoverable>
                                            <div className="mentor-card-item">
                                                <div className="mentor-header">
                                                    <div className="mentor-icon">
                                                        <UserCheck size={24} />
                                                    </div>
                                                    <div className="mentor-info">
                                                        <h3>{mentor.name || mentor.user__username}</h3>
                                                        <p>{mentor.email || mentor.user__email}</p>
                                                    </div>
                                                </div>
                                                <div className="mentor-stats">
                                                    <div className="mentor-stat">
                                                        <div className="mentor-stat-value">
                                                            {mentor.assigned_students || 0}
                                                        </div>
                                                        <div className="mentor-stat-label">Students</div>
                                                    </div>
                                                    <div className="mentor-stat">
                                                        <div className="mentor-stat-value">
                                                            {mentor.total_submissions || 0}
                                                        </div>
                                                        <div className="mentor-stat-label">Submissions</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </GlassCard>
                                    </motion.div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <UserCheck size={64} />
                                <h3>No Mentors Assigned</h3>
                                <p>Assign mentors to manage and guide students on this floor</p>
                                {!assignmentMode && (
                                    <button 
                                        className="assign-button"
                                        onClick={() => setAssignmentMode('mentor')}
                                        style={{ marginTop: '1.5rem' }}
                                    >
                                        Assign First Mentor
                                    </button>
                                )}
                            </div>
                        )}

                        {floorData.mentors && floorData.mentors.length > 0 && !assignmentMode && (
                            <button 
                                className="assign-button"
                                onClick={() => setAssignmentMode('mentor')}
                                style={{ marginTop: '2rem', width: '100%', maxWidth: '300px', display: 'block', marginLeft: 'auto', marginRight: 'auto' }}
                            >
                                Assign Another Mentor
                            </button>
                        )}
                    </div>
                )}

                {selectedTab === 'floorwing' && (
                    <div className="floor-wing-section">
                        {floorData.floor_wing ? (
                            <GlassCard>
                                <div className="floor-wing-card">
                                    <div className="floor-wing-status">
                                        <Crown size={32} />
                                        <div className="floor-wing-status-text">
                                            <h3>Floor Wing Assigned</h3>
                                            <p>This floor is managed by a designated floor wing</p>
                                        </div>
                                    </div>
                                    
                                    <div className="student-details">
                                        <div className="detail-row">
                                            <span className="detail-label">Name:</span>
                                            <span className="detail-value">{floorData.floor_wing.name}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="detail-label">Email:</span>
                                            <span className="detail-value">{floorData.floor_wing.email}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="detail-label">Students Overseeing:</span>
                                            <span className="detail-value">{floorData.students?.length || 0}</span>
                                        </div>
                                        <div className="detail-row">
                                            <span className="detail-label">Mentors Managing:</span>
                                            <span className="detail-value">{floorData.mentors?.length || 0}</span>
                                        </div>
                                    </div>
                                </div>
                            </GlassCard>
                        ) : (
                            <>
                                {assignmentMode === 'floor_wing' ? (
                                    <GlassCard>
                                        <div className="assignment-form">
                                            <div className="floor-wing-status unassigned">
                                                <Crown size={32} />
                                                <div className="floor-wing-status-text">
                                                    <h3>Assign Floor Wing</h3>
                                                    <p>Select a student to become the floor wing for Floor {floor}</p>
                                                </div>
                                            </div>

                                            <div className="form-group">
                                                <label>Select a student</label>
                                                <select 
                                                    value={selectedUser}
                                                    onChange={(e) => setSelectedUser(e.target.value)}
                                                >
                                                    <option value="">Choose a student...</option>
                                                    {getUnassignedUsers().map((user) => (
                                                        <option key={user.id} value={user.id}>
                                                            {user.name || user.user__username} ({user.email || user.user__email})
                                                        </option>
                                                    ))}
                                                </select>
                                            </div>
                                            
                                            <div className="form-actions">
                                                <button 
                                                    className="assign-button" 
                                                    onClick={handleAssignFloorWing} 
                                                    disabled={!selectedUser}
                                                >
                                                    Assign Floor Wing
                                                </button>
                                                <button 
                                                    className="cancel-button"
                                                    onClick={() => { setAssignmentMode(null); setSelectedUser(''); }}
                                                >
                                                    Cancel
                                                </button>
                                            </div>
                                        </div>
                                    </GlassCard>
                                ) : (
                                    <div className="empty-state">
                                        <Crown size={64} />
                                        <h3>No Floor Wing Assigned</h3>
                                        <p>Assign a floor wing to manage mentors and students on this floor</p>
                                        <button 
                                            className="assign-button"
                                            onClick={() => setAssignmentMode('floor_wing')}
                                            style={{ marginTop: '1.5rem' }}
                                        >
                                            Assign Floor Wing
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                )}
            </div>

            {/* Student Detail Drawer */}
            <AnimatePresence>
                {selectedStudent && (
                    <StudentDetailDrawer
                        student={studentDetail}
                        loading={loadingStudent}
                        onClose={closeStudentDrawer}
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

// Student Detail Drawer Component
const StudentDetailDrawer = ({ student, loading, onClose }) => {
    return (
        <motion.div
            className="student-drawer-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
        >
            <motion.div
                className="student-drawer"
                initial={{ x: '100%' }}
                animate={{ x: 0 }}
                exit={{ x: '100%' }}
                transition={{ type: 'spring', damping: 30, stiffness: 300 }}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="drawer-header">
                    <div>
                        <h2>{student?.name || 'Loading...'}</h2>
                        {student?.email && <p className="drawer-subtitle">{student.email}</p>}
                    </div>
                    <button className="close-drawer-button" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                {loading ? (
                    <div className="floor-detail-loading">
                        <div className="spinner"></div>
                        <p>Loading details...</p>
                    </div>
                ) : student ? (
                    <div className="drawer-content">
                        {/* Quick Info Cards */}
                        <div className="info-cards-grid">
                            <div className="info-card">
                                <div className="info-card-label">Roll Number</div>
                                <div className="info-card-value">{student.roll_no || 'N/A'}</div>
                            </div>
                            <div className="info-card">
                                <div className="info-card-label">Floor</div>
                                <div className="info-card-value">{student.floor || 'N/A'}</div>
                            </div>
                        </div>

                        {/* Campus & Mentor */}
                        <div className="drawer-section">
                            <div className="info-item">
                                <div className="info-item-label">Campus</div>
                                <div className="info-item-value">{student.campus_name || 'N/A'}</div>
                            </div>
                            <div className="info-item">
                                <div className="info-item-label">Mentor</div>
                                <div className="info-item-value">
                                    {student.assigned_mentor?.name || 'Not Assigned'}
                                </div>
                            </div>
                        </div>

                        {/* Performance Overview */}
                        <div className="drawer-section">
                            <h3>Performance Overview</h3>
                            <div className="performance-grid">
                                <div className="performance-card">
                                    <div className="performance-label">XP Points</div>
                                    <div className="performance-value xp-value">{student.xp_points || 0}</div>
                                </div>
                                <div className="performance-card">
                                    <div className="performance-label">Status</div>
                                    <span className={`status-badge status-${student.status || 'behind'}`}>
                                        {student.status === 'on_track' ? 'On Track' : 
                                         student.status === 'at_risk' ? 'At Risk' : 'Behind'}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Overall Progress */}
                        {student.pillar_progress !== undefined && (
                            <div className="drawer-section">
                                <div className="section-header">
                                    <h3>Overall Progress</h3>
                                    <span className="progress-percentage">{student.pillar_progress}%</span>
                                </div>
                                <div className="progress-bar-modern">
                                    <div
                                        className="progress-fill-modern"
                                        style={{ width: `${student.pillar_progress}%` }}
                                    />
                                </div>
                            </div>
                        )}

                        {/* Pillar Progress */}
                        {student.pillar_details && Object.keys(student.pillar_details).length > 0 && (
                            <div className="drawer-section">
                                <h3>Pillar Progress</h3>
                                <div className="pillars-grid">
                                    {Object.entries(student.pillar_details).map(([pillar, progress]) => (
                                        <div key={pillar} className="pillar-card">
                                            <div className="pillar-header">
                                                <span className="pillar-name">{pillar}</span>
                                                <span className="pillar-percentage">{progress}%</span>
                                            </div>
                                            <div className="progress-bar-small">
                                                <div
                                                    className="progress-fill-small"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Submission Statistics */}
                        {student.submission_stats && (
                            <div className="drawer-section">
                                <h3>Submission Statistics</h3>
                                <div className="stats-grid">
                                    <div className="stat-card">
                                        <div className="stat-value">{student.submission_stats.total || 0}</div>
                                        <div className="stat-label">Total</div>
                                    </div>
                                    <div className="stat-card stat-approved">
                                        <div className="stat-value">{student.submission_stats.approved || 0}</div>
                                        <div className="stat-label">Approved</div>
                                    </div>
                                    <div className="stat-card stat-pending">
                                        <div className="stat-value">{student.submission_stats.pending || 0}</div>
                                        <div className="stat-label">Pending</div>
                                    </div>
                                    <div className="stat-card stat-rejected">
                                        <div className="stat-value">{student.submission_stats.rejected || 0}</div>
                                        <div className="stat-label">Rejected</div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="floor-detail-error">
                        <p>Failed to load student details</p>
                    </div>
                )}
            </motion.div>
        </motion.div>
    );
};

export default FloorDetail;
