import React from 'react';
import { motion } from 'framer-motion';
import {
    Users, X, Filter, Search, CheckCircle, Clock, AlertCircle,
    Megaphone, Calendar, Trash2, Edit, UserPlus, ArrowRight
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import { floorWingAnnouncementService } from '../../services/announcement';

// Students View Component
export function StudentsView({
    students,
    mentors,
    filter,
    onFilterChange,
    searchTerm,
    onSearchChange,
    selectedStudents,
    onToggleSelection,
    onAssign,
    onBulkAssign,
    onStudentClick
}) {
    return (
        <motion.div
            key="students"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
        >
            <GlassCard>
                <div className="section-header">
                    <h2 className="section-title">
                        <Users size={24} />
                        Student Management
                    </h2>
                    <motion.button 
                        className="assign-students-btn"
                        onClick={() => onFilterChange('unassigned')}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <UserPlus size={18} />
                        Assign Students
                    </motion.button>
                </div>

                {/* Filters and Search */}
                <div className="students-controls">
                    <div className="filter-buttons">
                        <motion.button
                            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                            onClick={() => onFilterChange('all')}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            All
                        </motion.button>
                        <motion.button
                            className={`filter-btn ${filter === 'at_risk' ? 'active' : ''}`}
                            onClick={() => onFilterChange('at_risk')}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <AlertCircle size={16} />
                            At Risk
                        </motion.button>
                        <motion.button
                            className={`filter-btn ${filter === 'low_progress' ? 'active' : ''}`}
                            onClick={() => onFilterChange('low_progress')}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Low Progress
                        </motion.button>
                    </div>
                    <div className="search-box">
                        <Search size={18} />
                        <input
                            type="text"
                            placeholder="Search by name, roll no..."
                            value={searchTerm}
                            onChange={(e) => onSearchChange(e.target.value)}
                        />
                    </div>
                </div>

                {/* Assignment Mode Banner */}
                {filter === 'unassigned' && (
                    <div className="assignment-mode-banner">
                        <div className="banner-content">
                            <div className="banner-icon">
                                <UserPlus size={24} />
                            </div>
                            <div className="banner-text">
                                <h3>Assignment Mode</h3>
                                <p>Showing {students.length} unassigned student{students.length !== 1 ? 's' : ''}. Select students and assign them to mentors below.</p>
                            </div>
                        </div>
                        <motion.button 
                            className="exit-assignment-btn"
                            onClick={() => onFilterChange('all')}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Exit
                        </motion.button>
                    </div>
                )}

                {/* Bulk Actions */}
                {selectedStudents.length > 0 && (
                    <div className="bulk-actions-bar">
                        <span>{selectedStudents.length} student{selectedStudents.length > 1 ? 's' : ''} selected</span>
                        <select
                            className="bulk-select"
                            onChange={(e) => {
                                if (e.target.value) {
                                    onBulkAssign(parseInt(e.target.value));
                                    e.target.value = '';
                                }
                            }}
                        >
                            <option value="">Assign to mentor...</option>
                            {mentors.map(mentor => (
                                <option key={mentor.id} value={mentor.id}>
                                    {mentor.name} ({mentor.assigned_students_count || 0} students)
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Students Table */}
                {students.length > 0 ? (
                    <div className="table-container">
                        <table className="students-table">
                            <thead>
                                <tr>
                                    <th style={{ width: '50px' }}>
                                        <input
                                            type="checkbox"
                                            className="student-checkbox"
                                            onChange={(e) => {
                                                // Select/deselect all logic here
                                            }}
                                        />
                                    </th>
                                    <th>Student</th>
                                    <th>Mentor</th>
                                    <th style={{ width: '200px' }}>Progress</th>
                                    <th style={{ width: '100px' }}>Status</th>
                                    <th style={{ width: '150px' }}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {students.map(student => (
                                    <tr key={student.id}>
                                        <td>
                                            <input
                                                type="checkbox"
                                                className="student-checkbox"
                                                checked={selectedStudents.includes(student.id)}
                                                onChange={() => onToggleSelection(student.id)}
                                            />
                                        </td>
                                        <td>
                                            <div className="student-info">
                                                <span className="student-name">{student.name}</span>
                                                <span className="student-email">{student.roll_no || student.email}</span>
                                            </div>
                                        </td>
                                        <td>
                                            {student.assigned_mentor_name || <span className="text-muted">—</span>}
                                        </td>
                                        <td>
                                            <div className="pillar-dots">
                                                <span className={`pillar-dot ${(student.pillar_details?.cfc || 0) > 50 ? 'completed' : (student.pillar_details?.cfc || 0) > 0 ? 'partial' : 'empty'}`} title="CFC"></span>
                                                <span className={`pillar-dot ${(student.pillar_details?.clt || 0) > 50 ? 'completed' : (student.pillar_details?.clt || 0) > 0 ? 'partial' : 'empty'}`} title="CLT"></span>
                                                <span className={`pillar-dot ${(student.pillar_details?.sri || 0) > 50 ? 'completed' : (student.pillar_details?.sri || 0) > 0 ? 'partial' : 'empty'}`} title="SRI"></span>
                                                <span className={`pillar-dot ${(student.pillar_details?.iipc || 0) > 50 ? 'completed' : (student.pillar_details?.iipc || 0) > 0 ? 'partial' : 'empty'}`} title="IIPC"></span>
                                                <span className={`pillar-dot ${(student.pillar_details?.scd || 0) > 50 ? 'completed' : (student.pillar_details?.scd || 0) > 0 ? 'partial' : 'empty'}`} title="SCD"></span>
                                            </div>
                                        </td>
                                        <td>
                                            <span className={`status-badge ${student.status || 'on_track'}`}>
                                                {student.status === 'at_risk' ? 'At Risk' :
                                                 student.status === 'moderate' ? 'Moderate' : 'On Track'}
                                            </span>
                                        </td>
                                        <td>
                                            <div className="action-buttons-cell">
                                                {filter === 'unassigned' ? (
                                                    <select
                                                        className="inline-mentor-select"
                                                        onChange={(e) => {
                                                            if (e.target.value) {
                                                                onAssign(student.id, parseInt(e.target.value));
                                                            }
                                                        }}
                                                        defaultValue=""
                                                    >
                                                        <option value="">Assign to...</option>
                                                        {mentors.map(mentor => (
                                                            <option key={mentor.id} value={mentor.id}>
                                                                {mentor.name} ({mentor.assigned_students_count || 0})
                                                            </option>
                                                        ))}
                                                    </select>
                                                ) : (
                                                    <button
                                                        className="action-button"
                                                        onClick={() => onStudentClick(student)}
                                                    >
                                                        View
                                                    </button>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className="empty-state">
                        {filter === 'unassigned' ? (
                            <>
                                <CheckCircle size={48} style={{ color: '#4CAF50', opacity: 0.8 }} />
                                <p>All students have been assigned!</p>
                                <span className="empty-state-hint">
                                    Great work! All students on your floor have mentors assigned.
                                </span>
                            </>
                        ) : (
                            <>
                                <Users size={48} opacity={0.5} />
                                <p>No students found</p>
                                <span className="empty-state-hint">
                                    {filter !== 'all' ? 'Try changing your filter' : 'Students will appear here once assigned to your floor'}
                                </span>
                            </>
                        )}
                    </div>
                )}
            </GlassCard>
        </motion.div>
    );
}

// Mentors View Component
export function MentorsView({ mentors }) {
    return (
        <motion.div
            key="mentors"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
        >
            <GlassCard>
                <h2 className="section-title">
                    <CheckCircle size={24} />
                    Mentor Management
                </h2>
                {mentors && mentors.length > 0 ? (
                    <div className="mentors-grid">
                        {mentors.map((mentor, index) => (
                            <motion.div 
                                key={mentor.id} 
                                className="mentor-card-detailed"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="mentor-card-header">
                                    <div>
                                        <h3>{mentor.name}</h3>
                                        <p className="mentor-email">{mentor.email}</p>
                                    </div>
                                    <span className={`workload-badge ${mentor.workload_status || 'balanced'}`}>
                                        {mentor.workload_status === 'low' ? 'Low' :
                                         mentor.workload_status === 'overloaded' ? 'Overloaded' : 'Balanced'}
                                    </span>
                                </div>
                                <div className="mentor-card-stats">
                                    <div className="stat-item">
                                        <Users size={20} />
                                        <div>
                                            <strong>{mentor.assigned_students_count || 0}</strong>
                                            <span>Students</span>
                                        </div>
                                    </div>
                                    <div className="stat-item">
                                        <Clock size={20} />
                                        <div>
                                            <strong>{mentor.pending_reviews || 0}</strong>
                                            <span>Pending</span>
                                        </div>
                                    </div>
                                    <div className="stat-item">
                                        <CheckCircle size={20} />
                                        <div>
                                            <strong>{mentor.approval_rate || 0}%</strong>
                                            <span>Approved</span>
                                        </div>
                                    </div>
                                </div>
                                {mentor.last_active && (
                                    <div className="last-active">
                                        Last active: {new Date(mentor.last_active).toLocaleDateString()}
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="empty-state">
                        <CheckCircle size={48} opacity={0.5} />
                        <p>No mentors assigned</p>
                        <span className="empty-state-hint">
                            Mentor information will appear here once mentors are assigned to this floor
                        </span>
                    </div>
                )}
            </GlassCard>
        </motion.div>
    );
}

// Announcements View Component
export function AnnouncementsView({ announcements, onRefresh, onCreate }) {
    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this announcement?')) {
            try {
                await floorWingAnnouncementService.deleteAnnouncement(id);
                onRefresh();
            } catch (error) {
                console.error('Failed to delete:', error);
                alert('Failed to delete announcement');
            }
        }
    };

    return (
        <motion.div
            key="announcements"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
        >
            <GlassCard>
                <div className="section-header">
                    <h2 className="section-title">
                        <Megaphone size={24} />
                        Floor Announcements
                    </h2>
                    <motion.button 
                        className="create-announcement-btn" 
                        onClick={onCreate}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <Megaphone size={18} />
                        New Announcement
                    </motion.button>
                </div>

                {announcements && announcements.length > 0 ? (
                    <div className="announcements-list">
                        {announcements.map((announcement, index) => (
                            <motion.div 
                                key={announcement.id} 
                                className={`announcement-card priority-${announcement.priority}`}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                <div className="announcement-header">
                                    <div className="announcement-title-section">
                                        <h3 className="announcement-title">{announcement.title}</h3>
                                        <div className="announcement-meta">
                                            <span className={`priority-badge ${announcement.priority}`}>
                                                {announcement.priority === 'urgent' ? '🔴 Urgent' :
                                                 announcement.priority === 'important' ? '🟠 Important' : '🔵 Normal'}
                                            </span>
                                            <span className="announcement-date">
                                                <Calendar size={14} />
                                                {new Date(announcement.created_at).toLocaleDateString()}
                                            </span>
                                            {announcement.expires_at && (
                                                <span className="expiry-date">
                                                    Expires: {new Date(announcement.expires_at).toLocaleDateString()}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="announcement-actions">
                                        <button
                                            className="icon-btn delete"
                                            onClick={() => handleDelete(announcement.id)}
                                            title="Delete announcement"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                                <p className="announcement-message">{announcement.message}</p>
                                <div className="announcement-footer">
                                    <span className="read-status">
                                        📖 Read by: {announcement.read_count || 0} students
                                    </span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="empty-state">
                        <Megaphone size={48} opacity={0.5} />
                        <p>No announcements yet</p>
                        <span className="empty-state-hint">
                            Create your first announcement to communicate with students on this floor
                        </span>
                        <button className="empty-state-action" onClick={onCreate}>
                            Create Announcement
                        </button>
                    </div>
                )}
            </GlassCard>
        </motion.div>
    );
}

// Student Detail Drawer Component
export function StudentDetailDrawer({ student, mentors, onClose, onAssign }) {
    const [selectedMentor, setSelectedMentor] = React.useState('');


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
                        <h2>{student.name}</h2>
                        <p>{student.email}</p>
                    </div>
                    <button className="close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                <div className="drawer-body">
                    {/* Student Details */}
                    <section className="drawer-section">
                        <h3>Student Information</h3>
                        <div className="info-grid">
                            <div className="info-item">
                                <label>Roll No</label>
                                <span>{student.roll_no}</span>
                            </div>
                            <div className="info-item">
                                <label>Current Mentor</label>
                                <span>{student.assigned_mentor_name || 'Not Assigned'}</span>
                            </div>
                            <div className="info-item">
                                <label>Overall Progress</label>
                                <span>{student.pillar_progress || 0}%</span>
                            </div>
                            <div className="info-item">
                                <label>Status</label>
                                <span className={`status-badge ${student.status}`}>
                                    {student.status === 'on_track' ? 'On Track' : student.status}
                                </span>
                            </div>
                        </div>
                    </section>

                    {/* Pillar Progress */}
                    {student.pillar_details && (
                        <section className="drawer-section">
                            <h3>Pillar Progress</h3>
                            {Object.entries(student.pillar_details).map(([pillar, progress]) => (
                                <div key={pillar} className="pillar-progress-item">
                                    <span>{pillar.toUpperCase()}</span>
                                    <div className="progress-bar-small">
                                        <div
                                            className="progress-fill-small"
                                            style={{ width: `${progress}%` }}
                                        />
                                    </div>
                                    <span>{progress}%</span>
                                </div>
                            ))}
                        </section>
                    )}

                    {/* Reassign Mentor */}
                    <section className="drawer-section">
                        <h3>Reassign Mentor</h3>
                        <select
                            className="mentor-select"
                            value={selectedMentor}
                            onChange={(e) => setSelectedMentor(e.target.value)}
                        >
                            <option value="">Select a mentor...</option>
                            {mentors.map(mentor => (
                                <option key={mentor.id} value={mentor.id}>
                                    {mentor.name} ({mentor.assigned_students_count || 0} students)
                                </option>
                            ))}
                        </select>
                        <Button
                            variant="primary"
                            fullWidth
                            disabled={!selectedMentor}
                            onClick={() => {
                                if (selectedMentor) {
                                    onAssign(student.id, parseInt(selectedMentor));
                                    onClose();
                                }
                            }}
                        >
                            Assign Mentor
                        </Button>
                    </section>
                </div>
            </motion.div>
        </motion.div>
    );
}

// Announcement Modal Component
export function AnnouncementModal({ form, onChange, onSubmit, onClose }) {
    const handleChange = (field, value) => {
        onChange({ ...form, [field]: value });
    };

    return (
        <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
        >
            <motion.div
                className="modal-content"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="modal-header">
                    <h2><Megaphone size={24} /> Create Announcement</h2>
                    <button className="close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={onSubmit} className="modal-body">
                    <div className="form-group">
                        <label>Title *</label>
                        <input
                            type="text"
                            value={form.title}
                            onChange={(e) => handleChange('title', e.target.value)}
                            placeholder="Announcement title"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Message *</label>
                        <textarea
                            value={form.message}
                            onChange={(e) => handleChange('message', e.target.value)}
                            placeholder="Write your announcement here..."
                            rows={6}
                            required
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Priority</label>
                            <select
                                value={form.priority}
                                onChange={(e) => handleChange('priority', e.target.value)}
                            >
                                <option value="normal">Normal</option>
                                <option value="important">Important</option>
                                <option value="urgent">Urgent</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Status</label>
                            <select
                                value={form.status}
                                onChange={(e) => handleChange('status', e.target.value)}
                            >
                                <option value="published">Publish Now</option>
                                <option value="draft">Save as Draft</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Expires At (Optional)</label>
                        <input
                            type="datetime-local"
                            value={form.expires_at}
                            onChange={(e) => handleChange('expires_at', e.target.value)}
                        />
                    </div>

                    <div className="modal-actions">
                        <Button type="button" variant="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button type="submit" variant="primary">
                            {form.status === 'draft' ? 'Save Draft' : 'Publish Announcement'}
                        </Button>
                    </div>
                </form>
            </motion.div>
        </motion.div>
    );
}
