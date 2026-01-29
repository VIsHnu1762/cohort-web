import api from './api';

const jobsService = {
  /**
   * Get all jobs and internships for freshers in India
   */
  getOpportunities: async () => {
    const response = await api.get('/hackathons/jobs/');
    return response.data;
  },
};

export default jobsService;
