/**
 * SCD (Skill and Career Development) API Service
 * Handles all LeetCode profile and submission related API calls
 */

import axios from 'axios';

// Create dedicated axios instance for SCD
const scdAxios = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'}/scd`
});

// Add request interceptor for authentication
scdAxios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
scdAxios.interceptors.response.use(
  response => response,
  error => {
    console.error('SCD API Error:', error.response || error);
    if (error.response?.data) {
      console.error('Error details:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// LeetCode Profile API calls

/**
 * Get all LeetCode profiles for the current user
 */
export const getLeetCodeProfiles = async () => {
  const response = await scdAxios.get('/profiles/');
  return response.data;
};

/**
 * Get a specific LeetCode profile by ID
 */
export const getLeetCodeProfile = async (profileId) => {
  const response = await scdAxios.get(`/profiles/${profileId}/`);
  return response.data;
};

/**
 * Create a new LeetCode profile
 */
export const createLeetCodeProfile = async (profileData) => {
  const response = await scdAxios.post('/profiles/', profileData);
  return response.data;
};

/**
 * Update an existing LeetCode profile
 */
export const updateLeetCodeProfile = async (profileId, profileData) => {
  const response = await scdAxios.patch(`/profiles/${profileId}/`, profileData);
  return response.data;
};

/**
 * Delete a LeetCode profile
 */
export const deleteLeetCodeProfile = async (profileId) => {
  const response = await scdAxios.delete(`/profiles/${profileId}/`);
  return response.data;
};

/**
 * Sync LeetCode profile data from LeetCode API
 * @param {string} leetcodeUsername - LeetCode username to sync
 */
export const syncLeetCodeProfile = async (leetcodeUsername) => {
  const response = await scdAxios.post('/profiles/sync/', {
    leetcode_username: leetcodeUsername
  });
  return response.data;
};

/**
 * Submit LeetCode profile for mentor review
 * @param {number} profileId - Profile ID
 * @param {string} screenshotUrl - Google Drive link to screenshot
 */
export const submitProfileForReview = async (profileId, screenshotUrl) => {
  const response = await scdAxios.post(`/profiles/${profileId}/submit/`, {
    screenshot_url: screenshotUrl
  });
  return response.data;
};

/**
 * Get user's LeetCode profile statistics
 */
export const getProfileStats = async () => {
  const response = await scdAxios.get('/profiles/stats/');
  return response.data;
};

export default {
  getLeetCodeProfiles,
  getLeetCodeProfile,
  createLeetCodeProfile,
  updateLeetCodeProfile,
  deleteLeetCodeProfile,
  syncLeetCodeProfile,
  submitProfileForReview,
  getProfileStats
};
