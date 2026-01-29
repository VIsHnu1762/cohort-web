import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Create axios instance with auth token
const adminAxios = axios.create({
  baseURL: `${API_BASE_URL}/admin`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
adminAxios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
adminAxios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Admin API Service
 * Complete enterprise admin panel API integration
 */

// ===== DASHBOARD STATS =====
export const getDashboardStats = async () => {
  const response = await adminAxios.get('/stats');
  return response.data;
};

// ===== STUDENT MANAGEMENT =====
export const getStudents = async (params = {}) => {
  const response = await adminAxios.get('/students', { params });
  return response.data;
};

export const getStudent = async (studentId) => {
  const response = await adminAxios.get(`/students/${studentId}`);
  return response.data;
};

export const createStudent = async (studentData) => {
  const response = await adminAxios.post('/students', studentData);
  return response.data;
};

export const updateStudent = async (studentId, studentData) => {
  const response = await adminAxios.put(`/students/${studentId}`, studentData);
  return response.data;
};

export const deleteStudent = async (studentId) => {
  const response = await adminAxios.delete(`/students/${studentId}`);
  return response.data;
};

export const moveStudentToFloor = async (studentId, floorId) => {
  const response = await adminAxios.post(`/students/${studentId}/move`, { floor_id: floorId });
  return response.data;
};

// ===== MENTOR MANAGEMENT =====
export const getMentors = async (params = {}) => {
  const response = await adminAxios.get('/mentors', { params });
  return response.data;
};

export const getMentor = async (mentorId) => {
  const response = await adminAxios.get(`/mentors/${mentorId}`);
  return response.data;
};

export const createMentor = async (mentorData) => {
  const response = await adminAxios.post('/mentors', mentorData);
  return response.data;
};

export const updateMentor = async (mentorId, mentorData) => {
  const response = await adminAxios.put(`/mentors/${mentorId}`, mentorData);
  return response.data;
};

export const deleteMentor = async (mentorId) => {
  const response = await adminAxios.delete(`/mentors/${mentorId}`);
  return response.data;
};

export const getMentorStats = async (mentorId) => {
  const response = await adminAxios.get(`/mentors/${mentorId}/stats`);
  return response.data;
};

export const assignMentorToFloor = async (mentorId, floorId) => {
  const response = await adminAxios.post(`/mentors/${mentorId}/assign-floor`, { floor_id: floorId });
  return response.data;
};

export const getMentorStudents = async (mentorId) => {
  const response = await adminAxios.get(`/mentors/${mentorId}/students`);
  return response.data;
};

// ===== FLOOR MANAGEMENT =====
export const getFloors = async () => {
  const response = await adminAxios.get('/floors');
  return response.data;
};

export const getFloor = async (floorId) => {
  const response = await adminAxios.get(`/floors/${floorId}`);
  return response.data;
};

export const createFloor = async (floorData) => {
  const response = await adminAxios.post('/floors', floorData);
  return response.data;
};

export const updateFloor = async (floorId, floorData) => {
  const response = await adminAxios.put(`/floors/${floorId}`, floorData);
  return response.data;
};

export const deleteFloor = async (floorId) => {
  const response = await adminAxios.delete(`/floors/${floorId}`);
  return response.data;
};

export const getFloorStats = async (floorId) => {
  const response = await adminAxios.get(`/floors/${floorId}/stats`);
  return response.data;
};

// ===== SUBMISSION MANAGEMENT =====
export const getSubmissions = async (params = {}) => {
  const response = await adminAxios.get('/submissions', { params });
  return response.data;
};

export const getSubmission = async (submissionId) => {
  const response = await adminAxios.get(`/submissions/${submissionId}`);
  return response.data;
};

export const approveSubmission = async (submissionId, data = {}) => {
  const response = await adminAxios.post(`/submissions/${submissionId}/approve`, data);
  return response.data;
};

export const rejectSubmission = async (submissionId, data = {}) => {
  const response = await adminAxios.post(`/submissions/${submissionId}/reject`, data);
  return response.data;
};

export const getSubmissionStats = async (params = {}) => {
  const response = await adminAxios.get('/submissions/stats', { params });
  return response.data;
};

// ===== LEADERBOARD =====
export const getLeaderboard = async (params = {}) => {
  const response = await adminAxios.get('/leaderboard', { params });
  return response.data;
};

// ===== PILLAR RULES =====
export const getPillarRules = async (pillar) => {
  const response = await adminAxios.get(`/pillar-rules/${pillar}`);
  return response.data;
};

export const updatePillarRules = async (pillar, rulesData) => {
  const response = await adminAxios.put(`/pillar-rules/${pillar}`, rulesData);
  return response.data;
};

export const getAllPillarRules = async () => {
  const response = await adminAxios.get('/pillar-rules');
  return response.data;
};

// ===== NOTIFICATIONS & ANNOUNCEMENTS =====
export const getNotifications = async (params = {}) => {
  const response = await adminAxios.get('/notifications', { params });
  return response.data;
};

export const createNotification = async (notificationData) => {
  const response = await adminAxios.post('/notifications', notificationData);
  return response.data;
};

export const sendAnnouncement = async (announcementData) => {
  const response = await adminAxios.post('/announcements', announcementData);
  return response.data;
};

// ===== ROLES & PERMISSIONS =====
export const getRoles = async () => {
  const response = await adminAxios.get('/roles');
  return response.data;
};

export const getRole = async (roleId) => {
  const response = await adminAxios.get(`/roles/${roleId}`);
  return response.data;
};

export const updateRole = async (roleId, roleData) => {
  const response = await adminAxios.put(`/roles/${roleId}`, roleData);
  return response.data;
};

export const assignRole = async (userId, roleId) => {
  const response = await adminAxios.post('/roles/assign', { user_id: userId, role_id: roleId });
  return response.data;
};

// ===== SETTINGS =====
export const getSettings = async () => {
  const response = await adminAxios.get('/settings');
  return response.data;
};

export const updateSettings = async (settingsData) => {
  const response = await adminAxios.put('/settings', settingsData);
  return response.data;
};

export const uploadLogo = async (formData) => {
  const response = await adminAxios.post('/settings/logo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// ===== ANALYTICS =====
export const getAnalytics = async (params = {}) => {
  const response = await adminAxios.get('/analytics', { params });
  return response.data;
};

export const getPillarAnalytics = async (pillar) => {
  const response = await adminAxios.get(`/analytics/pillars/${pillar}`);
  return response.data;
};

export const getFloorAnalytics = async () => {
  const response = await adminAxios.get('/analytics/floors');
  return response.data;
};

export const getMentorAnalytics = async () => {
  const response = await adminAxios.get('/analytics/mentors');
  return response.data;
};

export const getXPDistribution = async () => {
  const response = await adminAxios.get('/analytics/xp-distribution');
  return response.data;
};

// ===== ACTIVITY LOGS =====
export const getActivityLogs = async (params = {}) => {
  const response = await adminAxios.get('/activity-logs', { params });
  return response.data;
};

// ===== CAMPUS/FLOOR HIERARCHY =====
export const getCampusOverview = async (campus) => {
  const token = localStorage.getItem('accessToken');
  const response = await axios.get(`${API_BASE_URL}/profiles/admin/campus/${campus}/`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export const getFloorDetail = async (campus, floor) => {
  const token = localStorage.getItem('accessToken');
  const response = await axios.get(`${API_BASE_URL}/profiles/admin/campus/${campus}/floor/${floor}/`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export const getStudentDetail = async (studentId) => {
  try {
    const token = localStorage.getItem('accessToken');
    const response = await axios.get(`${API_BASE_URL}/profiles/admin/student/${studentId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('getStudentDetail - Error:', error.response?.data || error.message);
    throw error;
  }
};

export const assignFloorWing = async (campus, floor, userId) => {
  const response = await axios.post(`${API_BASE_URL}/profiles/admin/assign-floor-wing/`, {
    campus,
    floor,
    user_id: userId
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`
    }
  });
  return response.data;
};

export const assignMentor = async (campus, floor, userId) => {
  const response = await axios.post(`${API_BASE_URL}/profiles/admin/assign-mentor/`, {
    campus,
    floor,
    user_id: userId
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`
    }
  });
  return response.data;
};

export default {
  getDashboardStats,
  getStudents,
  getStudent,
  createStudent,
  updateStudent,
  deleteStudent,
  moveStudentToFloor,
  getMentors,
  getMentor,
  createMentor,
  updateMentor,
  deleteMentor,
  getMentorStats,
  assignMentorToFloor,
  getMentorStudents,
  getFloors,
  getFloor,
  createFloor,
  updateFloor,
  deleteFloor,
  getFloorStats,
  getSubmissions,
  getSubmission,
  approveSubmission,
  rejectSubmission,
  getSubmissionStats,
  getLeaderboard,
  getPillarRules,
  updatePillarRules,
  getAllPillarRules,
  getNotifications,
  createNotification,
  sendAnnouncement,
  getRoles,
  getRole,
  updateRole,
  assignRole,
  getSettings,
  updateSettings,
  uploadLogo,
  getAnalytics,
  getPillarAnalytics,
  getFloorAnalytics,
  getMentorAnalytics,
  getXPDistribution,
  getActivityLogs,
  getCampusOverview,
  getFloorDetail,
  getStudentDetail,
  assignFloorWing,
  assignMentor,
};
