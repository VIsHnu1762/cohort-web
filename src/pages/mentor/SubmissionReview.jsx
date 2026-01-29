import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Lightbulb, Heart, Trophy, Linkedin, Code, Filter, Search,
    CheckCircle, XCircle, Clock, AlertCircle, Eye, FileText,
    Calendar, ExternalLink, User, MessageSquare, Send, ChevronDown, Award, Coins
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import { getPillarSubmissions } from '../../services/mentorApi';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
import gamificationAPI from '../../services/gamification';
import StudentMonthlyReport from './StudentMonthlyReport';
import './SubmissionReview.css';

const PILLARS = [
    { id: 'all', label: 'All Pillars', icon: Filter, color: '#ffcc00' },
    { id: 'clt', label: 'CLT', icon: Lightbulb, color: '#ffcc00' },
    { id: 'sri', label: 'SRI', icon: Heart, color: '#ffcc00' },
    { id: 'cfc', label: 'CFC', icon: Trophy, color: '#FFC107' },
    { id: 'iipc', label: 'IIPC', icon: Linkedin, color: '#0A66C2' },
    { id: 'scd', label: 'SCD', icon: Code, color: '#FF5722' },
];

const STATUS_OPTIONS = [
    { value: 'all', label: 'All Status', color: '#757575' },
    { value: 'pending', label: 'Pending', color: '#FF9800' },
    { value: 'approved', label: 'Approved', color: '#4CAF50' },
    { value: 'rejected', label: 'Rejected', color: '#f44336' },
    { value: 'resubmit', label: 'Needs Resubmission', color: '#FFC107' },
];

function SubmissionReview({ selectedStudent }) {
    const [selectedPillar, setSelectedPillar] = useState('all');
    const [selectedStatus, setSelectedStatus] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [reviewComment, setReviewComment] = useState('');
    const [reviewStatus, setReviewStatus] = useState(null); // 'loading', 'success', 'error'
    const [reviewMessage, setReviewMessage] = useState('');
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showMonthlyReport, setShowMonthlyReport] = useState(false);
    
    // Gamification scoring state
    const [gamificationScore, setGamificationScore] = useState(0);
    const [currentEpisode, setCurrentEpisode] = useState(null);
    const [seasonProgress, setSeasonProgress] = useState(null);
    const [showScoreInput, setShowScoreInput] = useState(false);
    const [loadingGamification, setLoadingGamification] = useState(false);

    // Fetch real submissions from API
    useEffect(() => {
        if (selectedStudent) {
            fetchSubmissions();
            fetchStudentGamification();
        }
    }, [selectedStudent, selectedPillar]);

    const fetchStudentGamification = async () => {
        if (!selectedStudent?.id) return;
        
        try {
            setLoadingGamification(true);
            const response = await gamificationAPI.mentor.getStudentProgress(selectedStudent.id);
            console.log('📊 Student gamification data:', response.data);
            
            setSeasonProgress(response.data);
            
            // Find current episode
            const currentEp = response.data.episode_progress?.find(ep => 
                ep.status === 'in_progress' || ep.status === 'locked'
            );
            setCurrentEpisode(currentEp || response.data.episode_progress?.[0]);
        } catch (error) {
            console.error('Failed to fetch gamification data:', error);
        } finally {
            setLoadingGamification(false);
        }
    };

    const fetchSubmissions = async () => {
        if (!selectedStudent) {
            console.warn('⚠️ No student selected');
            return;
        }
        
        try {
            setLoading(true);
            setSubmissions([]); // Clear previous submissions
            
            console.log('🔍 Fetching submissions for student:', selectedStudent);
            console.log('  - Full student object:', JSON.stringify(selectedStudent, null, 2));
            
            const studentId = selectedStudent.id;
            if (!studentId) {
                console.error('❌ No student ID found!');
                setSubmissions([]);
                return;
            }
            
            console.log('  - Using student_id:', studentId);
            console.log('  - Pillar:', selectedPillar);
            
            const data = await getPillarSubmissions(selectedPillar, {
                status: 'all',
                student_id: studentId
            });
            
            console.log('📥 API Response:', data);
            console.log('📋 Submissions count:', data.submissions?.length || 0);
            
            if (data.submissions && data.submissions.length > 0) {
                console.log('✅ Found', data.submissions.length, 'submissions');
                console.log('📌 First submission:', data.submissions[0]);
                setSubmissions(data.submissions);
            } else {
                console.log('⚠️ No submissions found for this student');
                setSubmissions([]);
            }
        } catch (error) {
            console.error('❌ Error fetching submissions:', error);
            console.error('Error details:', error.message);
            setSubmissions([]);
        } finally {
            setLoading(false);
        }
    };

    // Use only real submissions - no mock data fallback
    const displaySubmissions = submissions;
    
    console.log('🎯 SubmissionReview State:');
    console.log('  - submissions.length:', submissions.length);
    console.log('  - loading:', loading);
    console.log('  - selectedStudent:', selectedStudent?.name);
    console.log('  - displaySubmissions:', displaySubmissions);

    // Filter submissions
    const filteredSubmissions = displaySubmissions.filter(submission => {
        const pillarMatch = selectedPillar === 'all' || submission.pillar === selectedPillar;
        const statusMatch = selectedStatus === 'all' || submission.status === selectedStatus;
        const searchMatch = searchQuery === '' ||
            submission.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            submission.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            submission.platform?.toLowerCase().includes(searchQuery.toLowerCase());
        return pillarMatch && statusMatch && searchMatch;
    });

    const getStatusBadge = (status) => {
        const statusConfig = {
            pending: { label: 'Pending', color: '#FF9800', icon: Clock },
            approved: { label: 'Approved', color: '#4CAF50', icon: CheckCircle },
            rejected: { label: 'Rejected', color: '#f44336', icon: XCircle },
            resubmit: { label: 'Resubmit', color: '#FFC107', icon: AlertCircle },
        };
        const config = statusConfig[status] || statusConfig.pending;
        const Icon = config.icon;
        return (
            <div className="status-badge" style={{ '--status-color': config.color }}>
                <Icon size={14} />
                <span>{config.label}</span>
            </div>
        );
    };

    const getPillarIcon = (pillarId) => {
        const pillar = PILLARS.find(p => p.id === pillarId);
        if (!pillar) return null;
        const Icon = pillar.icon;
        return (
            <div className="pillar-icon-small" style={{ backgroundColor: `${pillar.color}20`, color: pillar.color }}>
                <Icon size={18} />
            </div>
        );
    };

    // Map pillar to gamification task type
    const mapPillarToTaskType = (pillar) => {
        const taskMap = {
            'clt': 'clt',
            'cfc': 'cfc_task1', // or cfc_task2, cfc_task3 depending on submission
            'iipc': 'iipc_task1', // or iipc_task2
            'sri': 'sri',
            'scd': 'scd_streak'
        };
        return taskMap[pillar];
    };

    const handleReview = async (submission, action) => {
        console.log('🔵 handleReview called!');
        console.log('  Submission:', submission);
        console.log('  Action:', action);
        console.log('  Comment:', reviewComment);
        console.log('  Gamification Score:', gamificationScore);
        
        if (!reviewComment.trim() && action !== 'Approved') {
            setReviewMessage('Please add a comment for your review');
            setTimeout(() => setReviewMessage(''), 3000);
            return;
        }
        
        // Validate score input for approval
        if (action === 'Approved' && showScoreInput && (!gamificationScore || gamificationScore <= 0)) {
            setReviewMessage('Please enter a valid score for this submission');
            setTimeout(() => setReviewMessage(''), 3000);
            return;
        }

        setReviewStatus('loading');
        
        // Map frontend action to backend action
        const actionMap = {
            'Approved': 'approve',
            'Rejected': 'reject',
            'Resubmission Requested': 'resubmit'
        };
        
        const backendAction = actionMap[action];
        
        // Prepare the review payload
        const reviewPayload = {
            pillar: submission.pillar,
            submission_id: submission.dbId || submission.id,
            submission_type: submission.modelType || 'clt', // Default to clt for now
            action: backendAction,
            comment: reviewComment || 'No comment provided'
        };
        
        console.log('📤 Sending review payload:', reviewPayload);
        console.log('📋 Submission object:', submission);
        
        try {
            const token = localStorage.getItem('accessToken');
            console.log('🔑 Token exists:', !!token);
            
            const response = await fetch(`${API_BASE_URL}/mentor/review/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(reviewPayload)
            });
            
            console.log('📡 Response status:', response.status);
            console.log('📡 Response ok:', response.ok);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to submit review');
            }
            
            const result = await response.json();
            console.log(`✅ ${action} submission:`, submission.id, 'Response:', result);
            console.log('🔄 Status changed from', submission.status, 'to', result.status);
            
            // If approved and score provided, update gamification
            if (action === 'Approved' && showScoreInput && gamificationScore > 0) {
                try {
                    console.log('🎯 Updating gamification score...');
                    const taskType = mapPillarToTaskType(submission.pillar);
                    if (taskType && currentEpisode) {
                        await gamificationAPI.mentor.approveTask(
                            selectedStudent.id,
                            currentEpisode.id,
                            taskType
                        );
                        console.log('✅ Gamification score updated!');
                        setReviewMessage(`Submission approved and ${gamificationScore} points awarded!`);
                    } else {
                        setReviewMessage(`Submission ${action.toLowerCase()} successfully!`);
                    }
                } catch (gamError) {
                    console.error('Failed to update gamification:', gamError);
                    // Don't fail the review if gamification fails
                    setReviewMessage(`Submission approved (gamification update pending)`);
                }
            } else {
                setReviewMessage(`Submission ${action.toLowerCase()} successfully!`);
            }
            
            setReviewStatus('success');
            console.log('🔃 Refreshing submissions...');
            console.log('Current submissions count:', submissions.length);
            
            // Refresh submissions from API
            await fetchSubmissions();
            
            console.log('✅ Submissions refreshed!');
            console.log('New submissions count:', submissions.length);
            
            // Close modal after short delay
            setTimeout(() => {
                setSelectedSubmission(null);
                setReviewComment('');
                setReviewStatus(null);
                setReviewMessage('');
            }, 2000);
        } catch (error) {
            console.error('Review error:', error);
            setReviewStatus('error');
            setReviewMessage(error.message || 'Failed to submit review. Please try again.');
            setTimeout(() => {
                setReviewStatus(null);
                setReviewMessage('');
            }, 3000);
        }
    };

    return (
        <div className="submission-review">
            {showMonthlyReport ? (
                <StudentMonthlyReport 
                    student={selectedStudent} 
                    onBack={() => setShowMonthlyReport(false)}
                />
            ) : (
                <>
            {/* Student Profile Overview */}
            <motion.div
                className="student-profile-overview"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <GlassCard>
                    <div className="profile-overview-content">
                        <div className="profile-avatar-large">
                            {selectedStudent.name.charAt(0)}
                        </div>
                        <div className="profile-details">
                            <h2 className="profile-name">{selectedStudent.name}</h2>
                            <p className="profile-roll">{selectedStudent.rollNo}</p>
                            <p className="profile-email">{selectedStudent.email}</p>
                            <Button 
                                onClick={() => setShowMonthlyReport(true)}
                                style={{ marginTop: '0.5rem' }}
                            >
                                <Calendar size={16} />
                                View Monthly Report
                            </Button>
                        </div>
                        <div className="profile-stats-grid">
                            <div className="profile-stat-item">
                                <div className="stat-value">{displaySubmissions.length}</div>
                                <div className="stat-label">Total Submissions</div>
                            </div>
                            <div className="profile-stat-item pending">
                                <div className="stat-value">{displaySubmissions.filter(s => s.status === 'pending').length}</div>
                                <div className="stat-label">Pending Review</div>
                            </div>
                            <div className="profile-stat-item approved">
                                <div className="stat-value">{displaySubmissions.filter(s => s.status === 'approved').length}</div>
                                <div className="stat-label">Approved</div>
                            </div>
                            <div className="profile-stat-item rejected">
                                <div className="stat-value">{displaySubmissions.filter(s => s.status === 'rejected').length}</div>
                                <div className="stat-label">Rejected</div>
                            </div>
                        </div>
                    </div>
                </GlassCard>
            </motion.div>

            {/* Submission Statistics Overview */}
            <motion.div
                className="statistics-overview"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <div className="stats-header">
                    <h3 className="stats-title">Filter by Pillar</h3>
                    <div className="stats-actions">
                        <select
                            className="compact-status-filter"
                            value={selectedStatus}
                            onChange={(e) => setSelectedStatus(e.target.value)}
                        >
                            {STATUS_OPTIONS.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                        <div className="compact-search-box">
                            <Search size={16} />
                            <input
                                type="text"
                                placeholder="Search submissions..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </div>
                </div>
                <div className="pillar-chips">
                    {/* All Pillars Chip */}
                    <button
                        className={`pillar-chip ${selectedPillar === 'all' ? 'active' : ''}`}
                        onClick={() => setSelectedPillar('all')}
                    >
                        <Filter size={18} />
                        <div className="chip-content">
                            <span className="chip-label">All Pillars</span>
                            <div className="chip-stats">
                                <span className="chip-total">{displaySubmissions.length}</span>
                                {displaySubmissions.filter(s => s.status === 'pending').length > 0 && (
                                    <span className="chip-pending">{displaySubmissions.filter(s => s.status === 'pending').length} pending</span>
                                )}
                            </div>
                        </div>
                    </button>
                    
                    {PILLARS.filter(p => p.id !== 'all').map(pillar => {
                        const Icon = pillar.icon;
                        const pillarSubmissions = displaySubmissions.filter(s => s.pillar === pillar.id);
                        const pendingCount = pillarSubmissions.filter(s => s.status === 'pending').length;
                        const isActive = selectedPillar === pillar.id;
                        return (
                            <button
                                key={pillar.id}
                                className={`pillar-chip ${isActive ? 'active' : ''}`}
                                onClick={() => setSelectedPillar(pillar.id)}
                                style={{ '--chip-color': pillar.color }}
                            >
                                <Icon size={18} />
                                <div className="chip-content">
                                    <span className="chip-label">{pillar.label}</span>
                                    <div className="chip-stats">
                                        <span className="chip-total">{pillarSubmissions.length}</span>
                                        {pendingCount > 0 && (
                                            <span className="chip-pending">{pendingCount} pending</span>
                                        )}
                                    </div>
                                </div>
                            </button>
                        );
                    })}
                </div>
            </motion.div>

            {/* Review Card - Show when submission is selected */}
            {selectedSubmission && (
                <motion.div
                    className="review-card-container"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 20 }}
                >
                    <GlassCard>
                        <div className="review-card-content">
                            {/* Close Button */}
                            <button
                                className="review-close-btn"
                                onClick={() => {
                                    setSelectedSubmission(null);
                                    setReviewComment('');
                                    setReviewStatus(null);
                                    setReviewMessage('');
                                }}
                                disabled={reviewStatus === 'loading'}
                            >
                                <XCircle size={20} />
                            </button>

                            {/* Status Messages */}
                            {reviewMessage && (
                                <motion.div
                                    className={`review-alert review-alert-${reviewStatus}`}
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                >
                                    {reviewStatus === 'success' && <CheckCircle size={18} />}
                                    {reviewStatus === 'error' && <XCircle size={18} />}
                                    {reviewStatus === null && <AlertCircle size={18} />}
                                    <span>{reviewMessage}</span>
                                </motion.div>
                            )}

                            {/* Card Header */}
                            <div className="review-card-header">
                                <div>
                                    <div className="review-title-row">
                                        {getPillarIcon(selectedSubmission.pillar)}
                                        <h2>{selectedSubmission.title}</h2>
                                    </div>
                                    <p className="review-platform">{selectedSubmission.platform}</p>
                                </div>
                                {getStatusBadge(selectedSubmission.status)}
                            </div>

                            {/* Student Info */}
                            <div className="review-section">
                                <h3 className="review-section-title">
                                    <User size={18} />
                                    Student Information
                                </h3>
                                <div className="student-info-grid">
                                    <div className="info-item">
                                        <span className="info-label">Name</span>
                                        <span className="info-value">{selectedSubmission.student.name}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="info-label">Roll No</span>
                                        <span className="info-value">{selectedSubmission.student.rollNo}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="info-label">Email</span>
                                        <span className="info-value">{selectedSubmission.student.email}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Submission Details */}
                            <div className="review-section">
                                <h3 className="review-section-title">
                                    <FileText size={18} />
                                    Submission Details
                                </h3>
                                <div className="detail-grid">
                                    <div className="detail-item">
                                        <span className="detail-label">Submitted On</span>
                                        <span className="detail-value">
                                            {new Date(selectedSubmission.submittedDate).toLocaleDateString('en-US', {
                                                year: 'numeric',
                                                month: 'long',
                                                day: 'numeric'
                                            })}
                                        </span>
                                    </div>
                                    {selectedSubmission.duration && (
                                        <div className="detail-item">
                                            <span className="detail-label">Duration</span>
                                            <span className="detail-value">{selectedSubmission.duration}</span>
                                        </div>
                                    )}
                                    {selectedSubmission.mode && (
                                        <div className="detail-item">
                                            <span className="detail-label">Mode</span>
                                            <span className="detail-value">{selectedSubmission.mode}</span>
                                        </div>
                                    )}
                                </div>
                                <div className="detail-description">
                                    <span className="detail-label">Description</span>
                                    <p className="detail-value">{selectedSubmission.description}</p>
                                </div>
                                {selectedSubmission.evidence && (
                                    <a
                                        href={selectedSubmission.evidence}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="evidence-link"
                                    >
                                        <ExternalLink size={16} />
                                        <span>View Evidence / Certificate</span>
                                    </a>
                                )}
                                {!selectedSubmission.evidence && (
                                    <div className="evidence-link disabled" style={{ cursor: 'not-allowed', opacity: 0.5 }}>
                                        <ExternalLink size={16} />
                                        <span>No Evidence Available</span>
                                    </div>
                                )}
                            </div>

                            {/* Review Actions */}
                            <div className="review-section">
                                <h3 className="review-section-title">
                                    <MessageSquare size={18} />
                                    Mentor Review & Feedback
                                </h3>
                                <textarea
                                    className="review-textarea"
                                    placeholder="Add your feedback or comments for the student... (Required for reject/resubmit)"
                                    value={reviewComment}
                                    onChange={(e) => setReviewComment(e.target.value)}
                                    rows={4}
                                    disabled={reviewStatus === 'loading'}
                                />
                                <p className="review-hint">
                                    Your feedback will be sent to the student along with your decision.
                                </p>
                            </div>

                            {/* Gamification Score Allotment */}
                            <div className="review-section gamification-scoring">
                                <div className="scoring-header">
                                    <h3 className="review-section-title">
                                        <Award size={18} />
                                        Gamification Score Allotment
                                    </h3>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={showScoreInput}
                                            onChange={(e) => setShowScoreInput(e.target.checked)}
                                            disabled={reviewStatus === 'loading'}
                                        />
                                        <span className="toggle-slider"></span>
                                        <span className="toggle-label">Enable Scoring</span>
                                    </label>
                                </div>

                                {/* Season Progress Info */}
                                {seasonProgress && (
                                    <div className="season-progress-info">
                                        <div className="progress-stat">
                                            <span className="progress-label">Current Episode</span>
                                            <span className="progress-value">
                                                Episode {currentEpisode?.episode_number || 1} of 4
                                            </span>
                                        </div>
                                        <div className="progress-stat">
                                            <span className="progress-label">Episode Progress</span>
                                            <span className="progress-value">
                                                {currentEpisode?.completion_percentage || 0}%
                                            </span>
                                        </div>
                                        <div className="progress-stat highlight">
                                            <span className="progress-label">Season Score (Cumulative)</span>
                                            <span className="progress-value">
                                                {seasonProgress.season_score?.total_score || 0} / 1500
                                            </span>
                                        </div>
                                    </div>
                                )}
                                
                                {showScoreInput && (
                                    <motion.div
                                        initial={{ opacity: 0, height: 0 }}
                                        animate={{ opacity: 1, height: 'auto' }}
                                        exit={{ opacity: 0, height: 0 }}
                                        className="score-input-container"
                                    >
                                        <div className="score-info-banner">
                                            <Award size={16} />
                                            <p>
                                                Approving this <strong>{selectedSubmission.pillar.toUpperCase()}</strong> task 
                                                will mark it complete in <strong>Episode {currentEpisode?.episode_number || 1}</strong> and 
                                                add points to the <strong>cumulative season score</strong> (max 1500 points).
                                            </p>
                                        </div>

                                        <div className="score-input-group">
                                            <div className="score-input-wrapper">
                                                <Coins size={20} className="score-icon" />
                                                <input
                                                    type="number"
                                                    className="score-input"
                                                    placeholder="Auto-calculated"
                                                    value={gamificationScore}
                                                    onChange={(e) => setGamificationScore(Number(e.target.value))}
                                                    min="0"
                                                    max="1500"
                                                    disabled={reviewStatus === 'loading'}
                                                />
                                                <span className="score-suffix">points</span>
                                            </div>
                                            <div className="score-helper-buttons">
                                                <button
                                                    type="button"
                                                    className="score-preset-btn"
                                                    onClick={() => setGamificationScore(50)}
                                                    disabled={reviewStatus === 'loading'}
                                                >
                                                    50
                                                </button>
                                                <button
                                                    type="button"
                                                    className="score-preset-btn"
                                                    onClick={() => setGamificationScore(100)}
                                                    disabled={reviewStatus === 'loading'}
                                                >
                                                    100
                                                </button>
                                                <button
                                                    type="button"
                                                    className="score-preset-btn"
                                                    onClick={() => setGamificationScore(200)}
                                                    disabled={reviewStatus === 'loading'}
                                                >
                                                    200
                                                </button>
                                            </div>
                                        </div>
                                        <p className="score-hint">
                                            <Award size={14} />
                                            Task completion is tracked per episode. All episode scores contribute to the season total.
                                        </p>
                                    </motion.div>
                                )}
                            </div>

                            {/* Action Buttons */}
                            <div className="review-actions">
                                <Button
                                    variant="secondary"
                                    onClick={() => handleReview(selectedSubmission, 'Rejected')}
                                    className="reject-btn"
                                    disabled={reviewStatus === 'loading'}
                                >
                                    {reviewStatus === 'loading' ? (
                                        <>
                                            <Clock size={16} className="spinning" />
                                            <span>Processing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <XCircle size={16} />
                                            <span>Reject</span>
                                        </>
                                    )}
                                </Button>
                                <Button
                                    variant="secondary"
                                    onClick={() => handleReview(selectedSubmission, 'Resubmission Requested')}
                                    className="resubmit-btn"
                                    disabled={reviewStatus === 'loading'}
                                >
                                    <AlertCircle size={16} />
                                    <span>Request Resubmission</span>
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => handleReview(selectedSubmission, 'Approved')}
                                    className="approve-btn"
                                    disabled={reviewStatus === 'loading'}
                                >
                                    <CheckCircle size={16} />
                                    <span>Approve</span>
                                </Button>
                            </div>
                        </div>
                    </GlassCard>
                </motion.div>
            )}

            {/* Submissions Grid */}
            {!selectedSubmission && (
                <motion.div
                    className="submissions-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                >
                    {loading ? (
                        <GlassCard>
                            <div className="no-submissions">
                                <Clock size={64} opacity={0.3} className="spinning" />
                                <h3>Loading Submissions...</h3>
                                <p>Fetching data from server...</p>
                            </div>
                        </GlassCard>
                    ) : filteredSubmissions.length === 0 ? (
                        <GlassCard>
                            <div className="no-submissions">
                                <FileText size={64} opacity={0.3} />
                                <h3>No Submissions Found</h3>
                                <p>This student hasn't submitted anything for {selectedPillar === 'all' ? 'any pillar' : selectedPillar.toUpperCase()} yet.</p>
                            </div>
                        </GlassCard>
                    ) : (
                    filteredSubmissions.map((submission, index) => (
                        <motion.div
                            key={submission.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * index }}
                        >
                            <GlassCard hoverable>
                                <div className="submission-card">
                                    <div className="submission-card-header">
                                        <div className="submission-header-left">
                                            {getPillarIcon(submission.pillar)}
                                            <div className="submission-info">
                                                <h3 className="submission-title">{submission.title}</h3>
                                                <p className="submission-platform">
                                                    <ExternalLink size={12} />
                                                    {submission.platform}
                                                </p>
                                            </div>
                                        </div>
                                        {getStatusBadge(submission.status)}
                                    </div>

                                    <p className="submission-description">{submission.description}</p>

                                    <div className="submission-footer">
                                        <div className="submission-meta">
                                            <div className="meta-item">
                                                <Calendar size={14} />
                                                <span>{new Date(submission.submittedDate).toLocaleDateString()}</span>
                                            </div>
                                            {submission.duration && (
                                                <div className="meta-item">
                                                    <Clock size={14} />
                                                    <span>{submission.duration}</span>
                                                </div>
                                            )}
                                        </div>
                                        <div className="submission-actions">
                                            <Button
                                                variant="secondary"
                                                size="small"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    window.open(submission.evidence, '_blank');
                                                }}
                                                style={{ gap: '0.5rem' }}
                                            >
                                                <ExternalLink size={14} />
                                                <span>Evidence</span>
                                            </Button>
                                            <Button
                                                variant="primary"
                                                size="small"
                                                onClick={() => setSelectedSubmission(submission)}
                                                style={{ gap: '0.5rem' }}
                                            >
                                                <Eye size={14} />
                                                <span>Review</span>
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </GlassCard>
                        </motion.div>
                    ))
                )}
            </motion.div>
            )}
            </>
            )}
        </div>
    );
}

export default SubmissionReview;
