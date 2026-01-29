/**
 * Mentor API Service
 * Handles all API calls for mentor-related operations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Helper function to get auth headers
const getAuthHeaders = () => {
    const token = localStorage.getItem('accessToken');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
    };
};

// Helper function to handle API responses
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Request failed' }));
        throw new Error(error.error || error.detail || 'Request failed');
    }
    return response.json();
};

/**
 * Get all submissions for a specific pillar
 * @param {string} pillar - Pillar ID (cfc, clt, sri, iipc, scd, all)
 * @param {object} filters - Filter options
 * @returns {Promise<object>} Submissions and total count
 */
export const getPillarSubmissions = async (pillar, filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.status && filters.status !== 'all') {
        params.append('status', filters.status);
    }
    if (filters.search) {
        params.append('search', filters.search);
    }
    if (filters.year && filters.year !== 'all') {
        params.append('year', filters.year);
    }
    if (filters.sort) {
        params.append('sort', filters.sort);
    }
    if (filters.student_id) {
        params.append('student_id', filters.student_id);
    }

    const url = `${API_BASE_URL}/mentor/pillar/${pillar}/submissions/?${params.toString()}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: getAuthHeaders(),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Error fetching submissions:', error);
        throw error;
    }
};

/**
 * Get statistics for a specific pillar
 * @param {string} pillar - Pillar ID (cfc, clt, sri, iipc, scd, all)
 * @returns {Promise<object>} Statistics object with total, pending, approved, rejected
 */
export const getPillarStats = async (pillar) => {
    const url = `${API_BASE_URL}/mentor/pillar/${pillar}/stats/`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: getAuthHeaders(),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Error fetching stats:', error);
        throw error;
    }
};

/**
 * Review a submission (approve or reject)
 * @param {object} reviewData - Review data
 * @returns {Promise<object>} Response with message and updated status
 */
export const reviewSubmission = async (reviewData) => {
    const url = `${API_BASE_URL}/mentor/review/`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(reviewData),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Error reviewing submission:', error);
        throw error;
    }
};

/**
 * Get detailed information about a specific submission
 * @param {string} pillar - Pillar ID
 * @param {string} submissionType - Type of submission
 * @param {number} submissionId - Submission ID
 * @returns {Promise<object>} Detailed submission data
 */
export const getSubmissionDetail = async (pillar, submissionType, submissionId) => {
    const url = `${API_BASE_URL}/mentor/submission/${pillar}/${submissionType}/${submissionId}/`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: getAuthHeaders(),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Error fetching submission detail:', error);
        throw error;
    }
};

/**
 * Map submission type from pillar
 * Helper to determine the submission type for API calls
 */
export const getSubmissionType = (pillar, submission) => {
    // Check if submission has a type field from backend
    if (submission.submissionType) {
        return submission.submissionType;
    }
    
    // Default mapping based on pillar
    const typeMap = {
        'cfc': 'hackathon', // Could also be bmc, internship, genai
        'clt': 'clt',
        'sri': 'sri',
        'iipc': 'linkedin',
        'scd': 'leetcode',
    };
    
    return typeMap[pillar] || pillar;
};
