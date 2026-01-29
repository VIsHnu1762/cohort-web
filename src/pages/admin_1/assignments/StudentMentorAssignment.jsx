import React, { useState, useEffect } from 'react';
import { Users, UserCheck, RefreshCw, Search, AlertCircle, CheckCircle } from 'lucide-react';
import './StudentMentorAssignment.css';

const StudentMentorAssignment = () => {
    const [students, setStudents] = useState([]);
    const [mentors, setMentors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [filterMentor, setFilterMentor] = useState('all');
    const [selectedStudents, setSelectedStudents] = useState([]);
    const [showBulkAssign, setShowBulkAssign] = useState(false);
    const [bulkMentorId, setBulkMentorId] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('accessToken');
            
            console.log('Fetching users with token:', token ? 'Present' : 'Missing');
            
            // Fetch all users
            const usersResponse = await fetch('http://localhost:8000/api/admin/users/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('Users API response status:', usersResponse.status);
            
            if (!usersResponse.ok) {
                const errorData = await usersResponse.json().catch(() => ({ error: 'Failed to fetch' }));
                console.error('API Error:', errorData);
                throw new Error(errorData.error || `HTTP ${usersResponse.status}`);
            }
            
            const usersData = await usersResponse.json();
            console.log('Fetched users:', usersData.length);
            
            // Separate students and mentors
            const studentsList = usersData.filter(u => !u.is_staff && !u.is_superuser);
            const mentorsList = usersData.filter(u => u.is_staff && !u.is_superuser);
            
            console.log('Students:', studentsList.length, 'Mentors:', mentorsList.length);
            
            setStudents(studentsList);
            setMentors(mentorsList);
        } catch (error) {
            console.error('Error fetching data:', error);
            setErrorMessage(error.message || 'Failed to load data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const assignMentorToStudent = async (studentId, mentorId) => {
        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch('http://localhost:8000/api/admin/assign-mentor/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    student_id: studentId,
                    mentor_id: mentorId
                })
            });
            
            if (!response.ok) throw new Error('Failed to assign mentor');
            
            setSuccessMessage('Mentor assigned successfully!');
            setTimeout(() => setSuccessMessage(''), 3000);
            fetchData(); // Refresh data
        } catch (error) {
            console.error('Error assigning mentor:', error);
            setErrorMessage('Failed to assign mentor. Please try again.');
            setTimeout(() => setErrorMessage(''), 3000);
        }
    };

    const handleBulkAssign = async () => {
        if (!bulkMentorId || selectedStudents.length === 0) {
            setErrorMessage('Please select students and a mentor');
            setTimeout(() => setErrorMessage(''), 3000);
            return;
        }

        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch('http://localhost:8000/api/admin/bulk-assign-mentor/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    student_ids: selectedStudents,
                    mentor_id: parseInt(bulkMentorId)
                })
            });
            
            if (!response.ok) throw new Error('Failed to bulk assign');
            
            setSuccessMessage(`Successfully assigned ${selectedStudents.length} students!`);
            setSelectedStudents([]);
            setShowBulkAssign(false);
            setBulkMentorId('');
            setTimeout(() => setSuccessMessage(''), 3000);
            fetchData();
        } catch (error) {
            console.error('Error bulk assigning:', error);
            setErrorMessage('Failed to bulk assign. Please try again.');
            setTimeout(() => setErrorMessage(''), 3000);
        }
    };

    const autoAssign = async () => {
        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch('http://localhost:8000/api/admin/auto-assign-mentors/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) throw new Error('Failed to auto-assign');
            
            const data = await response.json();
            setSuccessMessage(data.message || 'Auto-assignment completed!');
            setTimeout(() => setSuccessMessage(''), 3000);
            fetchData();
        } catch (error) {
            console.error('Error auto-assigning:', error);
            setErrorMessage('Failed to auto-assign. Please try again.');
            setTimeout(() => setErrorMessage(''), 3000);
        }
    };

    const toggleStudentSelection = (studentId) => {
        setSelectedStudents(prev => 
            prev.includes(studentId)
                ? prev.filter(id => id !== studentId)
                : [...prev, studentId]
        );
    };

    const filteredStudents = students.filter(student => {
        const matchesSearch = student.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
                            student.email.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesMentor = filterMentor === 'all' || 
                            (filterMentor === 'unassigned' && !student.assigned_mentor) ||
                            student.assigned_mentor?.id === parseInt(filterMentor);
        return matchesSearch && matchesMentor;
    });

    const getMentorById = (mentorId) => mentors.find(m => m.id === mentorId);

    const getMentorStats = () => {
        return mentors.map(mentor => ({
            ...mentor,
            studentCount: students.filter(s => s.assigned_mentor?.id === mentor.id).length
        }));
    };

    if (loading) {
        return (
            <div className="assignment-loading">
                <div className="loading-spinner"></div>
                <p>Loading assignment data...</p>
            </div>
        );
    }

    return (
        <div className="student-mentor-assignment">
            <div className="assignment-header">
                <div className="header-content">
                    <Users size={32} className="header-icon" />
                    <div>
                        <h1>Student-Mentor Assignment</h1>
                        <p>Manage and assign mentors to students</p>
                    </div>
                </div>
                
                <div className="header-actions">
                    <button className="btn btn-secondary" onClick={fetchData}>
                        <RefreshCw size={18} />
                        Refresh
                    </button>
                    <button className="btn btn-primary" onClick={autoAssign}>
                        <UserCheck size={18} />
                        Auto-Assign All
                    </button>
                </div>
            </div>

            {/* Messages */}
            {successMessage && (
                <div className="message message-success">
                    <CheckCircle size={20} />
                    {successMessage}
                </div>
            )}
            {errorMessage && (
                <div className="message message-error">
                    <AlertCircle size={20} />
                    {errorMessage}
                </div>
            )}

            {/* Mentor Stats */}
            <div className="mentor-stats">
                <h2>Mentor Overview</h2>
                <div className="stats-grid">
                    {getMentorStats().map(mentor => (
                        <div key={mentor.id} className="stat-card">
                            <div className="stat-header">
                                <UserCheck size={24} />
                                <h3>{mentor.username}</h3>
                            </div>
                            <p className="stat-email">{mentor.email}</p>
                            <div className="stat-count">
                                <span className="count">{mentor.studentCount}</span>
                                <span className="label">Assigned Students</span>
                            </div>
                        </div>
                    ))}
                    {mentors.length === 0 && (
                        <div className="stat-card empty">
                            <AlertCircle size={24} />
                            <p>No mentors available</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Filters and Search */}
            <div className="assignment-controls">
                <div className="search-box">
                    <Search size={20} />
                    <input
                        type="text"
                        placeholder="Search students by name or email..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>

                <select 
                    value={filterMentor} 
                    onChange={(e) => setFilterMentor(e.target.value)}
                    className="filter-select"
                >
                    <option value="all">All Students</option>
                    <option value="unassigned">Unassigned Only</option>
                    {mentors.map(mentor => (
                        <option key={mentor.id} value={mentor.id}>
                            {mentor.username}'s Students
                        </option>
                    ))}
                </select>

                {selectedStudents.length > 0 && (
                    <button 
                        className="btn btn-bulk"
                        onClick={() => setShowBulkAssign(true)}
                    >
                        Bulk Assign ({selectedStudents.length})
                    </button>
                )}
            </div>

            {/* Bulk Assign Modal */}
            {showBulkAssign && (
                <div className="modal-overlay" onClick={() => setShowBulkAssign(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h3>Bulk Assign Mentor</h3>
                        <p>Assign {selectedStudents.length} selected student(s) to:</p>
                        <select 
                            value={bulkMentorId} 
                            onChange={(e) => setBulkMentorId(e.target.value)}
                            className="modal-select"
                        >
                            <option value="">Select a mentor...</option>
                            {mentors.map(mentor => (
                                <option key={mentor.id} value={mentor.id}>
                                    {mentor.username} ({mentor.email})
                                </option>
                            ))}
                        </select>
                        <div className="modal-actions">
                            <button 
                                className="btn btn-secondary" 
                                onClick={() => setShowBulkAssign(false)}
                            >
                                Cancel
                            </button>
                            <button 
                                className="btn btn-primary" 
                                onClick={handleBulkAssign}
                            >
                                Assign
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Students Table */}
            <div className="students-table-container">
                <table className="students-table">
                    <thead>
                        <tr>
                            <th>
                                <input
                                    type="checkbox"
                                    checked={selectedStudents.length === filteredStudents.length && filteredStudents.length > 0}
                                    onChange={(e) => {
                                        if (e.target.checked) {
                                            setSelectedStudents(filteredStudents.map(s => s.id));
                                        } else {
                                            setSelectedStudents([]);
                                        }
                                    }}
                                />
                            </th>
                            <th>Student</th>
                            <th>Email</th>
                            <th>Assigned Mentor</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredStudents.map(student => (
                            <tr key={student.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={selectedStudents.includes(student.id)}
                                        onChange={() => toggleStudentSelection(student.id)}
                                    />
                                </td>
                                <td>
                                    <div className="student-info">
                                        <div className="student-avatar">
                                            {student.username[0].toUpperCase()}
                                        </div>
                                        <span>{student.username}</span>
                                    </div>
                                </td>
                                <td>{student.email}</td>
                                <td>
                                    {student.assigned_mentor ? (
                                        <span className="mentor-badge">
                                            {getMentorById(student.assigned_mentor.id)?.username || 'Unknown'}
                                        </span>
                                    ) : (
                                        <span className="unassigned-badge">Unassigned</span>
                                    )}
                                </td>
                                <td>
                                    <select
                                        value={student.assigned_mentor?.id || ''}
                                        onChange={(e) => assignMentorToStudent(student.id, e.target.value)}
                                        className="action-select"
                                    >
                                        <option value="">Select Mentor...</option>
                                        {mentors.map(mentor => (
                                            <option key={mentor.id} value={mentor.id}>
                                                {mentor.username}
                                            </option>
                                        ))}
                                    </select>
                                </td>
                            </tr>
                        ))}
                        {filteredStudents.length === 0 && (
                            <tr>
                                <td colSpan="5" className="empty-message">
                                    No students found matching your filters
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default StudentMentorAssignment;
