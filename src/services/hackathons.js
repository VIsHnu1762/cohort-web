import api from './api';

const hackathonService = {
  /**
   * Get all upcoming hackathons
   */
  getHackathons: async () => {
    const response = await api.get('/hackathons/list/');
    return response.data;
  },
};

export default hackathonService;
