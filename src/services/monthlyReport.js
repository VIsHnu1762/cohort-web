import api from './api';

const monthlyReportService = {
  getReport: async (month, year) => {
    const params = month && year ? `?month=${month}&year=${year}` : '';
    const response = await api.get(`/dashboard/monthly-report/${params}`);
    return response.data;
  },
  
  getAvailableMonths: async () => {
    const response = await api.get('/dashboard/available-months/');
    return response.data;
  },

  // For mentors to view student reports
  getStudentReport: async (studentId, month, year) => {
    const params = month && year ? `?month=${month}&year=${year}` : '';
    const response = await api.get(`/mentor/student/${studentId}/monthly-report/${params}`);
    return response.data;
  },

  getAvailableMonthsForStudent: async (studentId) => {
    const response = await api.get(`/mentor/student/${studentId}/available-months/`);
    return response.data;
  },
};

export default monthlyReportService;

