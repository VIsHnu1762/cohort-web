import api from './api';

/**
 * Dashboard API Service
 * Fetches aggregated statistics from all 5 pillars
 */

const dashboardService = {
  /**
   * Get dashboard statistics for all pillars
   * @returns {Promise} - Dashboard data with overall stats, pillar stats, activities, and notifications
   */
  getStats: async () => {
    const response = await api.get('/dashboard/stats/');
    return response.data;
  },
};

export default dashboardService;
