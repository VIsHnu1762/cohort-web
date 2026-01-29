import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'}/cfc`;

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('accessToken');
};

// Create axios instance with auth header
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ==================== HACKATHON REGISTRATIONS ====================

export const getHackathonRegistrations = async () => {
  const response = await axiosInstance.get('/hackathon-registrations/');
  return response.data;
};

export const getUpcomingHackathons = async () => {
  const response = await axiosInstance.get('/hackathon-registrations/upcoming/');
  return response.data;
};

export const createHackathonRegistration = async (data) => {
  const response = await axiosInstance.post('/hackathon-registrations/', data);
  return response.data;
};

export const updateHackathonRegistration = async (id, data) => {
  const response = await axiosInstance.put(`/hackathon-registrations/${id}/`, data);
  return response.data;
};

export const deleteHackathonRegistration = async (id) => {
  const response = await axiosInstance.delete(`/hackathon-registrations/${id}/`);
  return response.data;
};

export const markRegistrationCompleted = async (id) => {
  const response = await axiosInstance.post(`/hackathon-registrations/${id}/mark_completed/`);
  return response.data;
};

export const createSubmissionFromRegistration = async (id) => {
  const response = await axiosInstance.post(`/hackathon-registrations/${id}/create_submission/`);
  return response.data;
};

// ==================== HACKATHON SUBMISSIONS ====================

export const getHackathonSubmissions = async () => {
  const response = await axiosInstance.get('/hackathons/');
  return response.data;
};

export const getHackathonSubmission = async (id) => {
  const response = await axiosInstance.get(`/hackathons/${id}/`);
  return response.data;
};

export const createHackathonSubmission = async (data) => {
  const response = await axiosInstance.post('/hackathons/', data);
  return response.data;
};

export const updateHackathonSubmission = async (id, data) => {
  const response = await axiosInstance.put(`/hackathons/${id}/`, data);
  return response.data;
};

export const submitHackathonForReview = async (id) => {
  const response = await axiosInstance.post(`/hackathons/${id}/submit/`);
  return response.data;
};

export const getHackathonStats = async () => {
  const response = await axiosInstance.get('/hackathons/stats/');
  return response.data;
};

export const validateHackathonRepo = async (githubUrl) => {
  const response = await axiosInstance.post('/hackathons/validate_repo/', { github_url: githubUrl });
  return response.data;
};

// ==================== BMC VIDEO SUBMISSIONS ====================

export const getBMCVideoSubmissions = async () => {
  const response = await axiosInstance.get('/bmc-videos/');
  return response.data;
};

export const getBMCVideoSubmission = async (id) => {
  const response = await axiosInstance.get(`/bmc-videos/${id}/`);
  return response.data;
};

export const createBMCVideoSubmission = async (data) => {
  const response = await axiosInstance.post('/bmc-videos/', data);
  return response.data;
};

export const updateBMCVideoSubmission = async (id, data) => {
  const response = await axiosInstance.put(`/bmc-videos/${id}/`, data);
  return response.data;
};

export const submitBMCVideoForReview = async (id) => {
  const response = await axiosInstance.post(`/bmc-videos/${id}/submit/`);
  return response.data;
};

export const getBMCVideoStats = async () => {
  const response = await axiosInstance.get('/bmc-videos/stats/');
  return response.data;
};

export const checkVideoDuration = async (videoUrl) => {
  const response = await axiosInstance.post('/bmc-videos/check_duration/', { video_url: videoUrl });
  return response.data;
};

// ==================== INTERNSHIP SUBMISSIONS ====================

export const getInternshipSubmissions = async () => {
  const response = await axiosInstance.get('/internships/');
  return response.data;
};

export const getInternshipSubmission = async (id) => {
  const response = await axiosInstance.get(`/internships/${id}/`);
  return response.data;
};

export const createInternshipSubmission = async (data) => {
  const response = await axiosInstance.post('/internships/', data);
  return response.data;
};

export const updateInternshipSubmission = async (id, data) => {
  const response = await axiosInstance.put(`/internships/${id}/`, data);
  return response.data;
};

export const submitInternshipForReview = async (id) => {
  const response = await axiosInstance.post(`/internships/${id}/submit/`);
  return response.data;
};

export const updateInternshipStatus = async (id, status) => {
  const response = await axiosInstance.post(`/internships/${id}/update_status/`, {
    internship_status: status,
  });
  return response.data;
};

export const getInternshipStats = async () => {
  const response = await axiosInstance.get('/internships/stats/');
  return response.data;
};

// ==================== GENAI PROJECT SUBMISSIONS ====================

export const getGenAIProjectSubmissions = async () => {
  const response = await axiosInstance.get('/genai-projects/');
  return response.data;
};

export const getGenAIProjectSubmission = async (id) => {
  const response = await axiosInstance.get(`/genai-projects/${id}/`);
  return response.data;
};

export const createGenAIProjectSubmission = async (data) => {
  const response = await axiosInstance.post('/genai-projects/', data);
  return response.data;
};

export const updateGenAIProjectSubmission = async (id, data) => {
  const response = await axiosInstance.put(`/genai-projects/${id}/`, data);
  return response.data;
};

export const submitGenAIProjectForReview = async (id) => {
  const response = await axiosInstance.post(`/genai-projects/${id}/submit/`);
  return response.data;
};

export const getGenAIProjectStats = async () => {
  const response = await axiosInstance.get('/genai-projects/stats/');
  return response.data;
};

export const validateGithubRepo = async (githubUrl) => {
  const response = await axiosInstance.post('/genai-projects/validate_repo/', { github_url: githubUrl });
  return response.data;
};

// ==================== UTILITY FUNCTIONS ====================

export const getAllStats = async () => {
  try {
    const [hackathonStats, bmcStats, internshipStats, genaiStats] = await Promise.all([
      getHackathonStats(),
      getBMCVideoStats(),
      getInternshipStats(),
      getGenAIProjectStats(),
    ]);

    return {
      hackathon: hackathonStats,
      bmc: bmcStats,
      internship: internshipStats,
      genai: genaiStats,
    };
  } catch (error) {
    console.error('Error fetching all stats:', error);
    throw error;
  }
};

export default {
  // Hackathon
  getHackathonSubmissions,
  getHackathonSubmission,
  createHackathonSubmission,
  updateHackathonSubmission,
  submitHackathonForReview,
  getHackathonStats,
  validateHackathonRepo,
  // BMC Video
  getBMCVideoSubmissions,
  getBMCVideoSubmission,
  createBMCVideoSubmission,
  updateBMCVideoSubmission,
  submitBMCVideoForReview,
  getBMCVideoStats,
  checkVideoDuration,
  // Internship
  getInternshipSubmissions,
  getInternshipSubmission,
  createInternshipSubmission,
  updateInternshipSubmission,
  submitInternshipForReview,
  updateInternshipStatus,
  getInternshipStats,
  // GenAI
  getGenAIProjectSubmissions,
  getGenAIProjectSubmission,
  createGenAIProjectSubmission,
  updateGenAIProjectSubmission,
  submitGenAIProjectForReview,
  getGenAIProjectStats,
  validateGithubRepo,
  // Utility
  getAllStats,
};
