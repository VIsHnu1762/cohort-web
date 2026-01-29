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

            <div className="floor-detail-content">
                <div className="tabs">
                    <button 
                        className={`tab ${selectedTab === 'students' ? 'active' : ''}`}
                        onClick={() => setSelectedTab('students')}
                    >
                        <Users size={18} />
                        Students
                    </button>
                    <button 
                        className={`tab ${selectedTab === 'mentors' ? 'active' : ''}`}
                        onClick={() => setSelectedTab('mentors')}
                    >
                        <UserCheck size={18} />
                        Mentors
                    </button>
                    <button 
                        className={`tab ${selectedTab === 'floorwing' ? 'active' : ''}`}
                        onClick={() => setSelectedTab('floorwing')}
                    >
                        <Crown size={18} />
                        Floor Wing
                    </button>
                </div>

                <div className="tab-content">
                    {selectedTab === 'students' && (
                        <GlassCard>
                            <div className="section-header">
                                <h3>Students on Floor {floor}</h3>
                            </div>
                            <div className="students-list">
                                {floorData.students && floorData.students.length > 0 ? (
                                    floorData.students.map((student) => (
                                        <motion.div
                                            key={student.id}
                                            className="student-item"
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            onClick={() => handleStudentClick(student)}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <div className="student-info">
                                                <div className="student-name">{student.name || student.user__username}</div>
                                                <div className="student-email">{student.email || student.user__email}</div>
                                            </div>
                                            <div className="student-details">
                                                <span className="mentor-badge">
                                                    {student.mentor ? `Mentor: ${student.mentor}` : 'No Mentor'}
                                                </span>
                                                <span className="submission-count">
                                                    {student.submissions || student.submission_count || 0} submissions
                                                </span>
                                            </div>
                                        </motion.div>
                                    ))
                                ) : (
                                    <div className="empty-state">
                                        <Users size={48} />
                                        <p>No students on this floor</p>
                                    </div>
                                )}
                            </div>
                        </GlassCard>
                    )}

                    {selectedTab === 'mentors' && (
                        <GlassCard>
                            <div className="section-header">
                                <h3>Mentors on Floor {floor}</h3>
                                <button
                                    className="assign-button"
                                    onClick={() => setAssignmentMode('mentor')}
                                >
                                    Assign Mentor
                                </button>
                            </div>

                            {assignmentMode === 'mentor' && (
                                <div className="assignment-panel">
                                    <h4>Assign Mentor to Floor {floor}</h4>
                                    <select 
                                        value={selectedUser}
                                        onChange={(e) => setSelectedUser(e.target.value)}
                                        className="user-select"
                                    >
                                        <option value="">Select a user...</option>
                                        {getUnassignedUsers().map((user) => (
                                            <option key={user.id} value={user.id}>
                                                {user.name || user.user__username} ({user.email || user.user__email})
                                            </option>
                                        ))}
                                    </select>
                                    <div className="assignment-actions">
                                        <button onClick={handleAssignMentor} disabled={!selectedUser}>
                                            Confirm Assignment
                                        </button>
                                        <button onClick={() => { setAssignmentMode(null); setSelectedUser(''); }}>
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            )}

                            <div className="mentors-list">
                                {floorData.mentors && floorData.mentors.length > 0 ? (
                                    floorData.mentors.map((mentor) => (
                                        <motion.div
                                            key={mentor.id}
                                            className="mentor-item"
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                        >
                                            <div className="mentor-info">
                                                <div className="mentor-name">{mentor.name || mentor.user__username}</div>
                                                <div className="mentor-email">{mentor.email || mentor.user__email}</div>
                                            </div>
                                            <div className="mentor-stats">
                                                <span className="student-count">
                                                    {mentor.assigned_students || 0} students
                                                </span>
                                            </div>
                                        </motion.div>
                                    ))
                                ) : (
                                    <div className="empty-state">
                                        <UserCheck size={48} />
                                        <p>No mentors assigned to this floor</p>
                                        <button 
                                            className="assign-button-primary"
                                            onClick={() => setAssignmentMode('mentor')}
                                        >
                                            Assign First Mentor
                                        </button>
                                    </div>
                                )}
                            </div>
                        </GlassCard>
                    )}

                    {selectedTab === 'floorwing' && (
                        <GlassCard>
                            <div className="section-header">
                                <h3>Floor Wing</h3>
                                {!floorData.floor_wing && (
                                    <button 
                                        className="assign-button"
                                        onClick={() => setAssignmentMode('floor_wing')}
                                    >
                                        Assign Floor Wing
                                    </button>
                                )}
                            </div>

                            {assignmentMode === 'floor_wing' && (
                                <div className="assignment-panel">
                                    <h4>Assign Floor Wing to Floor {floor}</h4>
                                    <select 
                                        value={selectedUser}
                                        onChange={(e) => setSelectedUser(e.target.value)}
                                        className="user-select"
                                    >
                                        <option value="">Select a user...</option>
                                        {getUnassignedUsers().map((user) => (
                                            <option key={user.id} value={user.id}>
                                                {user.name || user.user__username} ({user.email || user.user__email})
                                            </option>
                                        ))}
                                    </select>
                                    <div className="assignment-actions">
                                        <button onClick={handleAssignFloorWing} disabled={!selectedUser}>
                                            Confirm Assignment
                                        </button>
                                        <button onClick={() => { setAssignmentMode(null); setSelectedUser(''); }}>
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            )}

                            {floorData.floor_wing ? (
                                <motion.div
                                    className="floor-wing-card"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                >
                                    <div className="floor-wing-icon">
                                        <Crown size={48} />
                                    </div>
                                    <div className="floor-wing-info">
                                        <div className="floor-wing-name">{floorData.floor_wing.name}</div>
                                        <div className="floor-wing-email">{floorData.floor_wing.email}</div>
                                    </div>
                                    <div className="floor-wing-stats">
                                        <div className="stat-item">
                                            <TrendingUp size={20} />
                                            <span>Managing {floorData.mentors?.length || 0} mentors</span>
                                        </div>
                                        <div className="stat-item">
                                            <Users size={20} />
                                            <span>Overseeing {floorData.students?.length || 0} students</span>
                                        </div>
                                    </div>
                                </motion.div>
                            ) : (
                                <div className="empty-state">
                                    <Crown size={48} />
                                    <p>No floor wing assigned</p>
                                    <p className="empty-state-hint">
                                        Assign a floor wing to manage mentors and students on this floor
                                    </p>
                                    <button 
                                        className="assign-button-primary"
                                        onClick={() => setAssignmentMode('floor_wing')}
                                    >
                                        Assign Floor Wing
                                    </button>
                                </div>
                            )}
                        </GlassCard>
                    )}
                </div>
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
            className="drawer-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
        >
            <motion.div
                className="drawer-content"
                initial={{ x: '100%' }}
                animate={{ x: 0 }}
                exit={{ x: '100%' }}
                transition={{ type: 'spring', damping: 25 }}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="drawer-header">
                    <div>
                        <h2>{student?.name || 'Loading...'}</h2>
                        <p>{student?.email || ''}</p>
                    </div>
                    <button className="close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                <div className="drawer-body">
                    {loading ? (
                        <div className="drawer-loading">
                            <div className="spinner"></div>
                            <p>Loading student details...</p>
                        </div>
                    ) : student ? (
                        <>
                            {/* Student Details */}
                            <section className="drawer-section">
                                <h3>Student Information</h3>
                                <div className="info-grid">
                                    <div className="info-item">
                                        <label>Roll No</label>
                                        <span>{student.roll_no}</span>
                                    </div>
                                    <div className="info-item">
                                        <label>Campus</label>
                                        <span>{student.campus_name}</span>
                                    </div>
                                    <div className="info-item">
                                        <label>Floor</label>
                                        <span>Floor {student.floor}</span>
                                    </div>
                                    <div className="info-item">
                                        <label>Current Mentor</label>
                                        <span>{student.assigned_mentor?.name || 'Not Assigned'}</span>
                                    </div>
                                    <div className="info-item">
                                        <label>XP Points</label>
                                        <span className="xp-badge">{student.xp_points} XP</span>
                                    </div>
                                    <div className="info-item">
                                        <label>Status</label>
                                        <span className={`status-badge status-${student.status}`}>
                                            {student.status === 'on_track' ? 'On Track' : 
                                             student.status === 'at_risk' ? 'At Risk' : 'Behind'}
                                        </span>
                                    </div>
                                </div>
                            </section>

                            {/* Overall Progress */}
                            <section className="drawer-section">
                                <h3>Overall Progress</h3>
                                <div className="progress-container">
                                    <div className="progress-bar-large">
                                        <div
                                            className="progress-fill-large"
                                            style={{ width: `${student.pillar_progress}%` }}
                                        />
                                    </div>
                                    <span className="progress-percentage">{student.pillar_progress}%</span>
                                </div>
                            </section>

                            {/* Pillar Progress */}
                            {student.pillar_details && Object.keys(student.pillar_details).length > 0 && (
                                <section className="drawer-section">
                                    <h3>Pillar Progress</h3>
                                    {Object.entries(student.pillar_details).map(([pillar, progress]) => (
                                        <div key={pillar} className="pillar-progress-item">
                                            <span className="pillar-name">{pillar}</span>
                                            <div className="progress-bar-small">
                                                <div
                                                    className="progress-fill-small"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                            <span className="pillar-percentage">{progress}%</span>
                                        </div>
                                    ))}
                                </section>
                            )}

                            {/* Submission Stats */}
                            {student.submission_stats && (
                                <section className="drawer-section">
                                    <h3>Submission Statistics</h3>
                                    <div className="stats-grid">
                                        <div className="stat-card">
                                            <label>Total</label>
                                            <span className="stat-value">{student.submission_stats.total}</span>
                                        </div>
                                        <div className="stat-card">
                                            <label>Approved</label>
                                            <span className="stat-value stat-approved">{student.submission_stats.approved}</span>
                                        </div>
                                        <div className="stat-card">
                                            <label>Pending</label>
                                            <span className="stat-value stat-pending">{student.submission_stats.pending}</span>
                                        </div>
                                        <div className="stat-card">
                                            <label>Rejected</label>
                                            <span className="stat-value stat-rejected">{student.submission_stats.rejected}</span>
                                        </div>
                                    </div>
                                </section>
                            )}
                        </>
                    ) : (
                        <div className="drawer-error">
                            <p>Failed to load student details</p>
                        </div>
                    )}
                </div>
            </motion.div>
        </motion.div>
    );
};

export default FloorDetail;
