import axios from 'axios';

const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'}/profiles`;

// Create axios instance with interceptors
const profileAxios = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
profileAxios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor for error handling
profileAxios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Get current user's profile
 */
export const getUserProfile = async () => {
  const response = await profileAxios.get('/me/');
  return response.data;
};

/**
 * Update user profile
 * @param {Object} data - Profile data to update
 * @param {string} data.leetcode_id - LeetCode username
 * @param {string} data.github_id - GitHub username
 * @param {string} data.linkedin_id - LinkedIn profile URL or ID
 */
export const updateUserProfile = async (data) => {
  const response = await profileAxios.patch('/me/', data);
  return response.data;
};

export default {
  getUserProfile,
  updateUserProfile,
};
