/**
 * Gamification API Service
 * Handles all gamification-related API calls
 */
import api from './api';

const gamificationAPI = {
  // Dashboard
  getStudentOverview: () => api.get('/gamification/dashboard/student_overview/'),
  
  // Seasons
  getCurrentSeason: () => api.get('/gamification/seasons/current/'),
  getAllSeasons: () => api.get('/gamification/seasons/'),
  
  // Episodes
  getCurrentEpisode: () => api.get('/gamification/episode-progress/current/'),
  getEpisodeProgress: () => api.get('/gamification/episode-progress/'),
  
  // Scores
  getCurrentSeasonScore: () => api.get('/gamification/season-scores/current/'),
  getAllSeasonScores: () => api.get('/gamification/season-scores/'),
  getLegacyScore: () => api.get('/gamification/legacy-scores/my_score/'),
  
  // Vault Wallet
  getMyWallet: () => api.get('/gamification/vault-wallets/my_wallet/'),
  
  // SCD Streak
  getCurrentStreak: () => api.get('/gamification/scd-streaks/current/'),
  syncStreak: () => api.post('/gamification/scd-streaks/sync/'),
  
  // Leaderboard
  getCurrentLeaderboard: () => api.get('/gamification/leaderboard/current_season/'),
  getFullLeaderboard: () => api.get('/gamification/leaderboard/full_leaderboard/'),
  getMyPosition: () => api.get('/gamification/leaderboard/my_position/'),
  
  // Titles
  getAllTitles: () => api.get('/gamification/titles/'),
  getTitles: () => api.get('/gamification/titles/'),
  getMyTitles: () => api.get('/gamification/user-titles/'),
  redeemTitle: (titleId) => api.post(`/gamification/titles/${titleId}/redeem/`),
  equipTitle: (titleId) => api.post(`/gamification/titles/${titleId}/equip/`),
  
  // Progress Notifications
  getBatchStats: () => api.get('/gamification/progress-notifications/batch_stats/'),
  getMyComparison: () => api.get('/gamification/progress-notifications/my_comparison/'),
  
  // Mentor APIs
  mentor: {
    approveTask: (studentId, episodeId, taskType) => 
      api.post('/gamification/mentor/approve-task/', {
        student_id: studentId,
        episode_id: episodeId,
        task_type: taskType
      }),
    
    getStudentProgress: (studentId) => 
      api.get(`/gamification/mentor/student-progress/${studentId}/`),
    
    finalizeSeason: (studentId) => 
      api.post(`/gamification/mentor/finalize-season/${studentId}/`)
  }
};

export default gamificationAPI;
