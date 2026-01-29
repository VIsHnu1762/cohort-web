import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Code, Flame, Trophy, TrendingUp, Target, Award, 
  CheckCircle, Clock, XCircle, RefreshCw,
  Activity, Zap
} from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import Input from '../../components/Input';
import {
  syncLeetCodeProfile,
  getLeetCodeProfiles
} from '../../services/scd';
import { getUserProfile } from '../../services/profile';
import './SCD.css';

export const SCD = () => {
  const [leetcodeUsername, setLeetcodeUsername] = useState('');
  const [profileData, setProfileData] = useState(null);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [autoSynced, setAutoSynced] = useState(false);

  // Load existing profile and auto-sync on mount
  useEffect(() => {
    loadProfileAndAutoSync();
  }, []);

  const loadProfileAndAutoSync = async () => {
    try {
      
      // Get user profile to check for saved leetcode_id
      const userProfile = await getUserProfile();
      
      // Load existing SCD profile
      const profiles = await getLeetCodeProfiles();
      if (profiles && profiles.length > 0) {
        const latest = profiles[0];
        setProfileData(latest);
        setLeetcodeUsername(latest.leetcode_username || userProfile.leetcode_id || '');
      } else if (userProfile.leetcode_id) {
        // No SCD profile exists, but user has saved leetcode_id
        setLeetcodeUsername(userProfile.leetcode_id);
      }

      // Auto-sync if leetcode_id exists in profile and not already synced
      if (userProfile.leetcode_id && !autoSynced) {
        await performAutoSync(userProfile.leetcode_id);
      }
    } catch (err) {
      console.error('Error loading profile:', err);
    }
  };

  const performAutoSync = async (username) => {
    try {
      setSyncing(true);
      const response = await syncLeetCodeProfile(username.trim());
      setProfileData(response.profile);
      setAutoSynced(true);
      setSuccess('Profile automatically synced using your saved LeetCode ID!');
      setTimeout(() => setSuccess(''), 5000);
    } catch (err) {
      console.error('Auto-sync failed:', err);
      // Don't show error for auto-sync failure, user can manually sync
    } finally {
      setSyncing(false);
    }
  };

  const handleSync = async () => {
    console.log('Sync button clicked! Username:', leetcodeUsername);
    
    if (!leetcodeUsername || !leetcodeUsername.trim()) {
      setError('Please set your LeetCode username in Profile Settings first');
      return;
    }

    setSyncing(true);
    setError('');
    setSuccess('');

    try {
      const response = await syncLeetCodeProfile(leetcodeUsername.trim());
      setProfileData(response.profile);
      setSuccess(response.warnings ? 
        `Profile synced with warnings: ${response.warnings.join(', ')}` : 
        'Profile synced successfully! Your stats have been updated.');
      
      setTimeout(() => setSuccess(''), 8000);
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Session expired. Please logout and login again.');
      } else {
        const errorMsg = err.response?.data?.error || 'Failed to sync profile. LeetCode API may be down. Try again later.';
        setError(errorMsg);
      }
    } finally {
      setSyncing(false);
    }
  };

  // Get difficulty color
  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'easy':
        return '#4ade80';
      case 'medium':
        return '#fbbf24';
      case 'hard':
        return '#f87171';
      default:
        return '#6b7280';
    }
  };

  return (
    <div className="scd-container">
      {/* Header */}
      <motion.div
        className="scd-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="scd-title">Skill and Career Development</h1>
        <p className="scd-subtitle">
          Track your coding journey with LeetCode integration
        </p>
      </motion.div>

      {/* Error/Success Messages */}
      <AnimatePresence>
        {error && (
          <motion.div
            className="scd-alert scd-alert-error"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <XCircle size={20} />
            <span>{error}</span>
          </motion.div>
        )}
        {success && (
          <motion.div
            className="scd-alert scd-alert-success"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <CheckCircle size={20} />
            <span>{success}</span>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="scd-layout">
        {/* Main Content */}
        <div className="scd-main">
          {/* Profile Sync Section */}
          <GlassCard variant="heavy" className="scd-sync-card">
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              marginBottom: '1rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Code size={20} style={{ color: 'var(--primary-color)' }} />
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    LeetCode Account
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                    {leetcodeUsername || 'Not connected'}
                  </div>
                </div>
              </div>
              
              <button
                onClick={handleSync}
                disabled={syncing}
                style={{
                  padding: '0.65rem 1rem',
                  background: syncing ? 'rgba(255, 255, 255, 0.05)' : (leetcodeUsername ? 'var(--primary-color)' : 'rgba(255, 255, 255, 0.1)'),
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  cursor: syncing ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  color: syncing ? 'var(--text-secondary)' : (leetcodeUsername ? '#000' : 'var(--text-secondary)'),
                  fontSize: '0.9rem',
                  fontWeight: '600',
                  transition: 'all 0.3s ease',
                  opacity: syncing ? 0.5 : (leetcodeUsername ? 1 : 0.6)
                }}
                onMouseEnter={(e) => {
                  if (!syncing && leetcodeUsername) {
                    e.currentTarget.style.background = '#FFD700';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!syncing && leetcodeUsername) {
                    e.currentTarget.style.background = 'var(--primary-color)';
                  }
                }}
              >
                <RefreshCw size={16} className={syncing ? 'scd-spinning' : ''} />
                {syncing ? 'Syncing...' : 'Sync Now'}
              </button>
            </div>

            {!leetcodeUsername && (
              <p style={{ 
                fontSize: '0.85rem', 
                color: 'var(--text-secondary)',
                margin: 0
              }}>
                Set your LeetCode username in Profile Settings
              </p>
            )}

            {profileData && (
              <div style={{ 
                fontSize: '0.75rem', 
                color: 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <Activity size={12} />
                <span>Last synced: {new Date(profileData.last_synced).toLocaleString()}</span>
              </div>
            )}
          </GlassCard>

          {/* Circular Progress Stats */}
          {profileData && (
            <GlassCard variant="heavy" className="scd-stats-card">
              <div className="scd-stats-header">
                <Trophy size={32} className="scd-trophy-icon" />
                <h2 className="scd-section-title">Problem Solving Statistics</h2>
              </div>

              <div className="scd-circular-container">
                {/* Main Circular Progress */}
                <div className="scd-circular-progress">
                  <svg className="scd-progress-ring" width="320" height="320" viewBox="0 0 320 320">
                    {/* Gradient Definition */}
                    <defs>
                      <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ffcc00" />
                        <stop offset="50%" stopColor="#FFD966" />
                        <stop offset="100%" stopColor="#FFA726" />
                      </linearGradient>
                    </defs>
                    
                    {/* Background Circle */}
                    <circle
                      className="scd-progress-ring-bg"
                      cx="160"
                      cy="160"
                      r="140"
                      fill="none"
                      stroke="rgba(255, 255, 255, 0.08)"
                      strokeWidth="20"
                    />
                    
                    {/* Progress Circle */}
                    <motion.circle
                      className="scd-progress-ring-progress"
                      cx="160"
                      cy="160"
                      r="140"
                      fill="none"
                      stroke="url(#progressGradient)"
                      strokeWidth="20"
                      strokeLinecap="round"
                      strokeDasharray="879.6"
                      initial={{ strokeDashoffset: 879.6 }}
                      animate={{ 
                        strokeDashoffset: 879.6 - (879.6 * Math.min(profileData.total_solved / 3773, 1))
                      }}
                      transition={{ 
                        duration: 2.5, 
                        ease: [0.4, 0, 0.2, 1],
                        delay: 0.3
                      }}
                    />
                  </svg>
                  
                  {/* Center Content */}
                  <div className="scd-progress-center">
                    <motion.div
                      className="scd-total-problems"
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ 
                        delay: 0.8,
                        type: 'spring',
                        stiffness: 200,
                        damping: 15
                      }}
                    >
                      {profileData.total_solved}
                    </motion.div>
                    <motion.div 
                      className="scd-problems-label"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.2 }}
                    >
                      Problems Solved
                    </motion.div>
                    <motion.div 
                      className="scd-problems-progress"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.4 }}
                    >
                      {Math.round((profileData.total_solved / 3773) * 100)}% Complete
                    </motion.div>
                  </div>
                </div>

                {/* Difficulty Stats Grid */}
                <div className="scd-difficulty-stats">
                  <motion.div
                    className="scd-difficulty-card scd-easy"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    <div className="scd-fire-stat-icon scd-fire-stat-easy">
                      <Target size={24} />
                    </div>
                    <div className="scd-fire-stat-content">
                      <div className="scd-fire-stat-value">{profileData.easy_solved}</div>
                      <div className="scd-fire-stat-label">Easy</div>
                    </div>
                  </motion.div>

                  <motion.div
                    className="scd-difficulty-card scd-medium"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                  >
                    <div className="scd-difficulty-icon scd-icon-medium">
                      <Zap size={28} />
                    </div>
                    <div className="scd-difficulty-content">
                      <div className="scd-difficulty-value">{profileData.medium_solved}</div>
                      <div className="scd-difficulty-label">Medium</div>
                    </div>
                  </motion.div>

                  <motion.div
                    className="scd-difficulty-card scd-hard"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                  >
                    <div className="scd-difficulty-icon scd-icon-hard">
                      <Flame size={28} />
                    </div>
                    <div className="scd-difficulty-content">
                      <div className="scd-difficulty-value">{profileData.hard_solved}</div>
                      <div className="scd-difficulty-label">Hard</div>
                    </div>
                  </motion.div>

                  {profileData.ranking && (
                    <motion.div
                      className="scd-difficulty-card scd-ranking"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.6 }}
                    >
                      <div className="scd-difficulty-icon scd-icon-ranking">
                        <TrendingUp size={28} />
                      </div>
                      <div className="scd-difficulty-content">
                        <div className="scd-difficulty-value">#{profileData.ranking.toLocaleString()}</div>
                        <div className="scd-difficulty-label">Ranking</div>
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            </GlassCard>
          )}

          {/* Monthly Target & Streak Section */}
          {profileData && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
              {/* Monthly Target Card */}
              <GlassCard variant="medium">
                <div style={{ textAlign: 'center' }}>
                  <Target size={32} style={{ color: profileData.monthly_problems_count >= 10 ? '#4ade80' : '#fbbf24', marginBottom: '0.5rem' }} />
                  <h3 style={{ margin: '0.5rem 0', fontSize: '1.1rem' }}>Monthly Target</h3>
                  <div style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: 'bold', 
                    color: profileData.monthly_problems_count >= 10 ? '#4ade80' : '#fbbf24',
                    margin: '1rem 0'
                  }}>
                    {profileData.monthly_problems_count}/10
                  </div>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: 0 }}>
                    Problems this month
                  </p>
                  {profileData.monthly_problems_count >= 10 ? (
                    <div style={{ 
                      marginTop: '1rem', 
                      padding: '0.5rem', 
                      background: 'rgba(74, 222, 128, 0.1)',
                      borderRadius: '8px',
                      color: '#4ade80',
                      fontSize: '0.85rem'
                    }}>
                      <CheckCircle size={16} style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} />
                      Target achieved! 🎉
                    </div>
                  ) : (
                    <div style={{ 
                      marginTop: '1rem', 
                      padding: '0.5rem', 
                      background: 'rgba(251, 191, 36, 0.1)',
                      borderRadius: '8px',
                      color: '#fbbf24',
                      fontSize: '0.85rem'
                    }}>
                      {10 - profileData.monthly_problems_count} more to reach target
                    </div>
                  )}
                </div>
              </GlassCard>

              {/* Streak Card */}
              <GlassCard variant="medium">
                <div style={{ textAlign: 'center' }}>
                  <Flame size={32} style={{ color: profileData.streak > 0 ? '#ff6b35' : 'var(--text-secondary)', marginBottom: '0.5rem' }} />
                  <h3 style={{ margin: '0.5rem 0', fontSize: '1.1rem' }}>Current Streak</h3>
                  <div style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: 'bold', 
                    color: profileData.streak > 0 ? '#ff6b35' : 'var(--text-secondary)',
                    margin: '1rem 0'
                  }}>
                    {profileData.streak}
                    <span style={{ fontSize: '1.2rem', marginLeft: '0.5rem' }}>🔥</span>
                  </div>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: 0 }}>
                    Days streak
                  </p>
                  <div style={{ 
                    marginTop: '1rem', 
                    padding: '0.5rem', 
                    background: 'rgba(255, 255, 255, 0.03)',
                    borderRadius: '8px',
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)'
                  }}>
                    <Activity size={14} style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} />
                    {profileData.total_active_days} total active days
                  </div>
                </div>
              </GlassCard>
            </div>
          )}
          {/* LeetCode Calendar Heatmap */}
          {profileData && profileData.submission_calendar && Object.keys(profileData.submission_calendar).length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <GlassCard variant="heavy">
                <div style={{ padding: '1.5rem' }}>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between',
                    marginBottom: '1.5rem',
                    paddingBottom: '1rem',
                    borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <h3 style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: '0.5rem',
                      fontSize: '1.1rem',
                      margin: 0,
                      fontWeight: '600'
                    }}>
                      <Activity size={20} style={{ color: 'var(--primary-color)' }} />
                      Activity Calendar
                    </h3>
                    <div style={{ 
                      fontSize: '0.85rem',
                      color: 'var(--text-secondary)',
                      display: 'flex',
                      gap: '1.5rem'
                    }}>
                      {(() => {
                        const calendar = profileData.submission_calendar || {};
                        const totalSubmissions = Object.values(calendar).reduce((sum, count) => sum + parseInt(count || 0), 0);
                        return (
                          <>
                            <span><strong style={{ color: 'var(--primary-color)' }}>{totalSubmissions}</strong> submissions</span>
                          </>
                        );
                      })()}
                    </div>
                  </div>
                  
                  <div>
                  {(() => {
                    const calendar = profileData.submission_calendar || {};
                    
                    // Get color based on submission count
                    const getColor = (count) => {
                      if (count === 0) return 'rgba(255, 255, 255, 0.05)';
                      if (count <= 2) return 'rgba(74, 222, 128, 0.3)';
                      if (count <= 5) return 'rgba(74, 222, 128, 0.5)';
                      if (count <= 10) return 'rgba(74, 222, 128, 0.7)';
                      return 'rgba(74, 222, 128, 0.9)';
                    };
                    
                    // Group by months (last 12 months)
                    const now = new Date();
                    const months = [];
                    
                    for (let i = 11; i >= 0; i--) {
                      const monthDate = new Date(now.getFullYear(), now.getMonth() - i, 1);
                      const monthName = monthDate.toLocaleDateString('en-US', { month: 'short' });
                      const year = monthDate.getFullYear();
                      const month = monthDate.getMonth();
                      
                      // Get all days in this month
                      const daysInMonth = new Date(year, month + 1, 0).getDate();
                      const firstDay = new Date(year, month, 1).getDay(); // 0 = Sunday
                      
                      const days = [];
                      
                      // Add empty cells for days before month starts
                      for (let j = 0; j < firstDay; j++) {
                        days.push({ isEmpty: true });
                      }
                      
                      // Add actual days
                      for (let day = 1; day <= daysInMonth; day++) {
                        const date = new Date(year, month, day);
                        const midnightUTC = new Date(Date.UTC(year, month, day));
                        const dateTimestamp = Math.floor(midnightUTC.getTime() / 1000).toString();
                        
                        const localMidnight = new Date(date);
                        localMidnight.setHours(0, 0, 0, 0);
                        const localTimestamp = Math.floor(localMidnight.getTime() / 1000).toString();
                        
                        const count = parseInt(calendar[dateTimestamp]) || parseInt(calendar[localTimestamp]) || 0;
                        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                        
                        days.push({
                          date,
                          dateStr,
                          count,
                          day
                        });
                      }
                      
                      months.push({
                        monthName,
                        year,
                        days,
                        totalDays: daysInMonth
                      });
                    }
                    
                    return (
                      <div>
                        <div style={{ 
                          display: 'grid',
                          gridTemplateColumns: 'repeat(4, 1fr)',
                          gap: '1.5rem',
                          marginBottom: '1.5rem'
                        }}>
                          {months.map((monthData, monthIdx) => (
                            <div key={monthIdx} style={{
                              background: 'rgba(255, 255, 255, 0.02)',
                              borderRadius: '8px',
                              padding: '0.75rem'
                            }}>
                              <div style={{ 
                                fontSize: '0.75rem',
                                fontWeight: '600',
                                marginBottom: '0.5rem',
                                color: 'var(--text-primary)',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px'
                              }}>
                                {monthData.monthName}
                              </div>
                              
                              {/* Day labels */}
                              <div style={{ 
                                display: 'grid',
                                gridTemplateColumns: 'repeat(7, 1fr)',
                                gap: '2px',
                                marginBottom: '4px'
                              }}>
                                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, idx) => (
                                  <div key={idx} style={{
                                    fontSize: '0.6rem',
                                    textAlign: 'center',
                                    color: 'var(--text-secondary)',
                                    fontWeight: '600'
                                  }}>
                                    {day}
                                  </div>
                                ))}
                              </div>
                              
                              {/* Calendar grid */}
                              <div style={{ 
                                display: 'grid',
                                gridTemplateColumns: 'repeat(7, 1fr)',
                                gap: '2px'
                              }}>
                                {monthData.days.map((day, dayIdx) => (
                                  day.isEmpty ? (
                                    <div key={dayIdx} style={{ 
                                      width: '18px', 
                                      height: '18px',
                                      aspectRatio: '1'
                                    }} />
                                  ) : (
                                    <div
                                      key={dayIdx}
                                      title={`${day.dateStr}: ${day.count} ${day.count === 1 ? 'submission' : 'submissions'}`}
                                      style={{
                                        width: '18px',
                                        height: '18px',
                                        aspectRatio: '1',
                                        background: getColor(day.count),
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '3px',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s ease',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontSize: '0.55rem',
                                        color: day.count > 0 ? 'rgba(255, 255, 255, 0.7)' : 'rgba(255, 255, 255, 0.3)',
                                        fontWeight: '600',
                                        position: 'relative'
                                      }}
                                      onMouseEnter={(e) => {
                                        e.currentTarget.style.transform = 'scale(1.2)';
                                        e.currentTarget.style.border = '2px solid var(--primary-color)';
                                        e.currentTarget.style.zIndex = '10';
                                      }}
                                      onMouseLeave={(e) => {
                                        e.currentTarget.style.transform = 'scale(1)';
                                        e.currentTarget.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                                        e.currentTarget.style.zIndex = '1';
                                      }}
                                    >
                                      {day.day}
                                    </div>
                                  )
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        {/* Legend */}
                        <div style={{ 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center',
                          gap: '0.5rem',
                          fontSize: '0.7rem',
                          color: 'var(--text-secondary)',
                          paddingTop: '1rem',
                          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
                        }}>
                          <span style={{ fontWeight: '500' }}>Less</span>
                          <div style={{ 
                            width: '16px', 
                            height: '16px', 
                            background: 'rgba(255, 255, 255, 0.05)', 
                            borderRadius: '3px', 
                            border: '1px solid rgba(255, 255, 255, 0.1)' 
                          }} />
                          <div style={{ 
                            width: '16px', 
                            height: '16px', 
                            background: 'rgba(74, 222, 128, 0.3)', 
                            borderRadius: '3px', 
                            border: '1px solid rgba(255, 255, 255, 0.1)' 
                          }} />
                          <div style={{ 
                            width: '16px', 
                            height: '16px', 
                            background: 'rgba(74, 222, 128, 0.5)', 
                            borderRadius: '3px', 
                            border: '1px solid rgba(255, 255, 255, 0.1)' 
                          }} />
                          <div style={{ 
                            width: '16px', 
                            height: '16px', 
                            background: 'rgba(74, 222, 128, 0.7)', 
                            borderRadius: '3px', 
                            border: '1px solid rgba(255, 255, 255, 0.1)' 
                          }} />
                          <div style={{ 
                            width: '16px', 
                            height: '16px', 
                            background: 'rgba(74, 222, 128, 0.9)', 
                            borderRadius: '3px', 
                            border: '1px solid rgba(255, 255, 255, 0.1)' 
                          }} />
                          <span style={{ fontWeight: '500' }}>More</span>
                        </div>
                      </div>
                    );
                  })()}
                </div>
              </div>
              </GlassCard>
            </motion.div>
          )}        </div>

        {/* Sidebar */}
        <div className="scd-sidebar">
          {/* Recent Submissions */}
          {profileData && profileData.submissions && profileData.submissions.length > 0 && (
            <GlassCard variant="medium" className="scd-recent-card">
              <h3 className="scd-card-title">Recent Submissions</h3>

              <div className="scd-submissions-list">
                {profileData.submissions.slice(0, 10).map((submission, index) => (
                  <motion.div
                    key={submission.id}
                    className="scd-submission-item"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 + index * 0.05 }}
                  >
                    <div className="scd-submission-header">
                      <span className="scd-submission-problem">{submission.problem_title}</span>
                      <span 
                        className="scd-submission-difficulty"
                        style={{ color: getDifficultyColor(submission.difficulty) }}
                      >
                        {submission.difficulty}
                      </span>
                    </div>
                    <div className="scd-submission-footer">
                      <span className="scd-submission-status">{submission.status}</span>
                      <span className="scd-submission-date">
                        {new Date(submission.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </GlassCard>
          )}

          {/* Achievement Badge */}
          {profileData && profileData.total_solved > 0 && (
            <motion.div
              className="scd-achievement-badge"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              whileHover={{ scale: 1.05, rotate: 5 }}
            >
              <Award size={48} />
              <h4>
                {profileData.total_solved > 300 ? 'Coding Master' : 
                 profileData.total_solved > 100 ? 'Problem Solver' : 
                 'Rising Star'}
              </h4>
              <p>Keep pushing forward!</p>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SCD;
