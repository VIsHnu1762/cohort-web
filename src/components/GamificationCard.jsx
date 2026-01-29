import React, { useState, useEffect } from 'react';
import { Trophy, Target, Flame, Award, Coins } from 'lucide-react';
import gamificationAPI from '../services/gamification';
import './GamificationCard.css';

const GamificationCard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGamificationData();
  }, []);

  const fetchGamificationData = async () => {
    try {
      setLoading(true);
      const response = await gamificationAPI.getStudentOverview();
      setData(response.data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch gamification data:', err);
      // Set default data if API fails
      setData({
        current_season: null,
        current_episode: null,
        episode_progress: 0,
        season_score: 0,
        legacy_score: 0,
        vault_wallet: 0,
        scd_streak: 0,
        leaderboard_position: '-',
        equipped_title: null
      });
      setError(null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return null;

  const { 
    current_season, 
    current_episode, 
    episode_progress,
    season_score, 
    legacy_score, 
    vault_wallet, 
    scd_streak,
    leaderboard_position,
    equipped_title 
  } = data;

  const scorePercentage = ((season_score?.total_score || 0) / 1500) * 100;
  const episodeCompletion = episode_progress?.completion_percentage || 0;

  return (
    <>
      {/* Integrated Score Banner */}
      <div className="achievement-banner">
        <div className="achievement-row">
          <div className="achievement-item">
            <div className="achievement-icon">
              <Trophy size={20} />
            </div>
            <div className="achievement-details">
              <span className="achievement-label">Season Score</span>
              <span className="achievement-value">{season_score?.total_score || 0}/1500</span>
            </div>
          </div>

          <div className="achievement-item">
            <div className="achievement-icon legacy">
              <Award size={20} />
            </div>
            <div className="achievement-details">
              <span className="achievement-label">Legacy Score</span>
              <span className="achievement-value">{legacy_score?.total_legacy_points || 0}</span>
            </div>
          </div>

          <div className="achievement-item">
            <div className="achievement-icon streak">
              <Flame size={20} />
            </div>
            <div className="achievement-details">
              <span className="achievement-label">Streak</span>
              <span className="achievement-value">{scd_streak?.current_streak || 0} days</span>
            </div>
          </div>

          <div className="achievement-item">
            <div className="achievement-icon rank">
              <Target size={20} />
            </div>
            <div className="achievement-details">
              <span className="achievement-label">Rank</span>
              <span className="achievement-value">{leaderboard_position || 'N/A'}</span>
            </div>
          </div>

          <div className="achievement-item">
            <div className="achievement-icon credits">
              <Coins size={20} />
            </div>
            <div className="achievement-details">
              <span className="achievement-label">Credits</span>
              <span className="achievement-value">{vault_wallet?.available_credits || 0}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Current Progress Card */}
      <div className="progress-summary-card">
        <div className="progress-header">
          <div>
            <h3>Current Progress</h3>
            <p className="progress-subtitle">{current_season?.name || 'No Active Season'}</p>
          </div>
          {equipped_title && (
            <span className="title-badge">{equipped_title}</span>
          )}
        </div>

        <div className="progress-bars-container">
          <div className="progress-bar-item">
            <div className="progress-bar-header">
              <span>Episode {current_episode?.episode_number || 1}</span>
              <span className="progress-percentage">{Math.round(episodeCompletion)}%</span>
            </div>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill episode" 
                style={{ width: `${episodeCompletion}%` }}
              ></div>
            </div>
          </div>

          <div className="progress-bar-item">
            <div className="progress-bar-header">
              <span>Season Score</span>
              <span className="progress-percentage">{Math.round(scorePercentage)}%</span>
            </div>
            <div className="progress-bar-track">
              <div 
                className="progress-bar-fill score" 
                style={{ width: `${scorePercentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Task Checklist */}
        {episode_progress && current_episode && (
          <div className="task-checklist">
            <h4>Episode {current_episode.episode_number} Tasks</h4>
            <div className="task-list">
              {current_episode.episode_number === 1 && (
                <>
                  <TaskCheckItem label="CLT Submission" completed={episode_progress.clt_completed} />
                  <TaskCheckItem label="Daily Practice" completed={episode_progress.scd_streak_active} />
                </>
              )}
              {current_episode.episode_number === 2 && (
                <>
                  <TaskCheckItem label="CFC Task 1" completed={episode_progress.cfc_task1_completed} />
                  <TaskCheckItem label="IIPC Task 1" completed={episode_progress.iipc_task1_completed} />
                  <TaskCheckItem label="Daily Practice" completed={episode_progress.scd_streak_active} />
                </>
              )}
              {current_episode.episode_number === 3 && (
                <>
                  <TaskCheckItem label="CFC Task 2" completed={episode_progress.cfc_task2_completed} />
                  <TaskCheckItem label="IIPC Task 2" completed={episode_progress.iipc_task2_completed} />
                  <TaskCheckItem label="Daily Practice" completed={episode_progress.scd_streak_active} />
                </>
              )}
              {current_episode.episode_number === 4 && (
                <>
                  <TaskCheckItem label="CFC Task 3" completed={episode_progress.cfc_task3_completed} />
                  <TaskCheckItem label="SRI Activity" completed={episode_progress.sri_completed} />
                  <TaskCheckItem label="Daily Practice" completed={episode_progress.scd_streak_active} />
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
};

const TaskCheckItem = ({ label, completed }) => (
  <div className={`task-check-item ${completed ? 'completed' : ''}`}>
    <div className="task-check-box">
      {completed && <span>✓</span>}
    </div>
    <span className="task-check-label">{label}</span>
  </div>
);

export default GamificationCard;
