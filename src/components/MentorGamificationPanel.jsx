import React, { useState, useEffect } from 'react';
import { Trophy, Medal, Award, TrendingUp, Users, Crown } from 'lucide-react';
import gamificationAPI from '../services/gamification';
import './MentorGamificationPanel.css';

const MentorGamificationPanel = () => {
  const [loading, setLoading] = useState(true);
  const [leaderboardData, setLeaderboardData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLeaderboardData();
  }, []);

  const fetchLeaderboardData = async () => {
    try {
      setLoading(true);
      const response = await gamificationAPI.getFullLeaderboard();
      setLeaderboardData(response.data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch leaderboard data:', err);
      setError(err.response?.data?.detail || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="mentor-gamification-panel loading">
        <div className="loading-spinner">Loading leaderboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mentor-gamification-panel error">
        <p>{error}</p>
      </div>
    );
  }

  if (!leaderboardData) return null;

  const { top_ranks, percentiles, total_students } = leaderboardData;

  const getRankIcon = (rank) => {
    switch(rank) {
      case 1: return <Crown size={24} className="rank-icon gold" />;
      case 2: return <Medal size={24} className="rank-icon silver" />;
      case 3: return <Medal size={24} className="rank-icon bronze" />;
      default: return <Trophy size={20} className="rank-icon default" />;
    }
  };

  const getRankClass = (rank) => {
    switch(rank) {
      case 1: return 'rank-gold';
      case 2: return 'rank-silver';
      case 3: return 'rank-bronze';
      default: return '';
    }
  };

  return (
    <div className="mentor-gamification-panel">
      {/* Header Stats */}
      <div className="gamification-header">
        <div className="header-stat">
          <Users size={20} />
          <div className="stat-content">
            <span className="stat-label">Total Students</span>
            <span className="stat-value">{total_students}</span>
          </div>
        </div>
        <div className="header-stat">
          <Trophy size={20} />
          <div className="stat-content">
            <span className="stat-label">Ranked</span>
            <span className="stat-value">{top_ranks.length}</span>
          </div>
        </div>
        <div className="header-stat">
          <TrendingUp size={20} />
          <div className="stat-content">
            <span className="stat-label">In Progress</span>
            <span className="stat-value">{percentiles.length}</span>
          </div>
        </div>
      </div>

      {/* Full Leaderboard */}
      <div className="leaderboard-section">
        <h3 className="section-title">
          <Trophy size={20} />
          Complete Leaderboard
        </h3>

        {/* Top Ranks */}
        {top_ranks.length > 0 && (
          <div className="leaderboard-list">
            <div className="leaderboard-header">
              <span>Rank</span>
              <span>Student</span>
              <span>Score</span>
              <span>Title</span>
            </div>
            {top_ranks.map((entry) => (
              <div 
                key={entry.id} 
                className={`leaderboard-item ${getRankClass(entry.rank)}`}
              >
                <div className="rank-cell">
                  {getRankIcon(entry.rank)}
                  <span className="rank-number">#{entry.rank}</span>
                </div>
                <div className="student-cell">
                  <div className="student-avatar">
                    {entry.student_name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'ST'}
                  </div>
                  <div className="student-info">
                    <span className="student-name">{entry.student_name}</span>
                    <span className="student-username">@{entry.student_username}</span>
                  </div>
                </div>
                <div className="score-cell">
                  <span className="score-value">{entry.season_score}</span>
                  <span className="score-max">/1500</span>
                </div>
                <div className="title-cell">
                  <span className="rank-title">{entry.rank_title}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Percentile Students */}
        {percentiles.length > 0 && (
          <div className="percentile-section">
            <h4 className="subsection-title">
              <Award size={18} />
              Students by Percentile
            </h4>
            <div className="percentile-list">
              <div className="leaderboard-header">
                <span>Percentile</span>
                <span>Student</span>
                <span>Score</span>
                <span>Status</span>
              </div>
              {percentiles.map((entry, index) => (
                <div key={index} className="leaderboard-item percentile-item">
                  <div className="percentile-cell">
                    <Award size={18} className="percentile-icon" />
                    <span className="percentile-value">{entry.percentile}</span>
                  </div>
                  <div className="student-cell">
                    <div className="student-avatar">
                      {entry.student_name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'ST'}
                    </div>
                    <div className="student-info">
                      <span className="student-name">{entry.student_name}</span>
                      <span className="student-username">@{entry.student_username}</span>
                    </div>
                  </div>
                  <div className="score-cell">
                    <span className="score-value">{entry.season_score}</span>
                    <span className="score-max">/1500</span>
                  </div>
                  <div className="status-cell">
                    <span className="status-badge">Completed</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {top_ranks.length === 0 && percentiles.length === 0 && (
          <div className="empty-state">
            <Trophy size={48} />
            <p>No students have completed the season yet</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MentorGamificationPanel;
