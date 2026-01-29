import axios from 'axios';

const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'}/iipc`;

// Create a dedicated axios instance for IIPC
const iipcAxios = axios.create({
  baseURL: API_BASE_URL,
});

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('accessToken');
};

// Configure axios with auth header
const getAuthHeaders = () => ({
  headers: {
    Authorization: `Bearer ${getAuthToken()}`,
  },
});

// Add response interceptor to handle auth errors (only for iipcAxios instance)
iipcAxios.interceptors.response.use(
  (response) => {
    console.log('IIPC API Response:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('IIPC API Error:', error.config?.url, error.response?.status);
    if (error.response?.status === 401) {
      // Token is invalid or expired
      console.error('Authentication failed - token invalid or expired');
      console.error('Please logout and login again to get a fresh token');
    }
    return Promise.reject(error);
  }
);

// ==================== LinkedIn Post Verification ====================

/**
 * Get all LinkedIn post verifications for current user
 */
export const getLinkedInPosts = async () => {
  const response = await iipcAxios.get('/posts/', getAuthHeaders());
  return response.data;
};

/**
 * Get a specific LinkedIn post verification
 */
export const getLinkedInPost = async (id) => {
  const response = await iipcAxios.get(`/posts/${id}/`, getAuthHeaders());
  return response.data;
};

/**
 * Create a new LinkedIn post verification
 */
export const createLinkedInPost = async (postData) => {
  const response = await iipcAxios.post(
    '/posts/',
    postData,
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Update a LinkedIn post verification
 */
export const updateLinkedInPost = async (id, postData) => {
  const response = await iipcAxios.patch(
    `/posts/${id}/`,
    postData,
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Submit a LinkedIn post verification for review
 */
export const submitPostForReview = async (id) => {
  const response = await iipcAxios.post(
    `/posts/${id}/submit/`,
    {},
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Get LinkedIn post verification statistics
 */
export const getPostStats = async () => {
  const response = await iipcAxios.get('/posts/stats/', getAuthHeaders());
  return response.data;
};

// ==================== LinkedIn Connection Verification ====================

/**
 * Get all LinkedIn connection verifications for current user
 */
export const getLinkedInConnections = async () => {
  const response = await iipcAxios.get('/connections/', getAuthHeaders());
  return response.data;
};

/**
 * Get a specific LinkedIn connection verification
 */
export const getLinkedInConnection = async (id) => {
  const response = await iipcAxios.get(
    `/connections/${id}/`,
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Create a new LinkedIn connection verification
 */
export const createLinkedInConnection = async (connectionData) => {
  const response = await iipcAxios.post(
    '/connections/',
    connectionData,
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Update a LinkedIn connection verification
 */
export const updateLinkedInConnection = async (id, connectionData) => {
  const response = await iipcAxios.patch(
    `/connections/${id}/`,
    connectionData,
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Submit a LinkedIn connection verification for review
 */
export const submitConnectionForReview = async (id) => {
  const response = await iipcAxios.post(
    `/connections/${id}/submit/`,
    {},
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Connect LinkedIn profile - New endpoint for profile connection
 */
export const connectLinkedInProfile = async (profileUrl, totalConnections) => {
  const response = await iipcAxios.post(
    '/connections/connect_profile/',
    {
      profile_url: profileUrl,
      total_connections: totalConnections,
    },
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Get LinkedIn connection verification statistics
 */
export const getConnectionStats = async () => {
  const response = await iipcAxios.get(
    '/connections/stats/',
    getAuthHeaders()
  );
  return response.data;
};

/**
 * Get all IIPC statistics (combined posts + connections)
 */
export const getAllStats = async () => {
  const response = await iipcAxios.get(
    '/connections/all_stats/',
    getAuthHeaders()
  );
  return response.data;
};

// ==================== LinkedIn OAuth ====================

/**
 * Get LinkedIn OAuth authorization URL
 */
export const getLinkedInAuthUrl = async () => {
  const response = await iipcAxios.get('/connections/linkedin_auth_url/');
  return response.data;
};

/**
 * Handle LinkedIn OAuth callback - exchange code for profile data
 */
export const handleLinkedInCallback = async (code, state) => {
  const response = await iipcAxios.post(
    '/connections/linkedin_callback/',
    {
      code,
      state,
    },
    getAuthHeaders()
  );
  return response.data;
};

export default {
  // Post methods
  getLinkedInPosts,
  getLinkedInPost,
  createLinkedInPost,
  updateLinkedInPost,
  submitPostForReview,
  getPostStats,
  
  // Connection methods
  getLinkedInConnections,
  getLinkedInConnection,
  createLinkedInConnection,
  updateLinkedInConnection,
  submitConnectionForReview,
  connectLinkedInProfile,
  getConnectionStats,
  getAllStats,
  
  // OAuth methods
  getLinkedInAuthUrl,
  handleLinkedInCallback,
};
