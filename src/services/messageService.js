import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Get auth token from localStorage
const getAuthToken = () => {
    return localStorage.getItem('access_token');
};

// Configure axios instance with auth headers
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
});

axiosInstance.interceptors.request.use((config) => {
    const token = getAuthToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

/**
 * Message Service - Handles communication between mentors and students
 */
const messageService = {
    /**
     * Send a message from mentor to student
     * @param {number} recipientId - Student ID
     * @param {string} content - Message content
     * @param {string} messageType - 'general', 'completion', or 'pending'
     */
    sendMessage: async (recipientId, content, messageType = 'general') => {
        try {
            const response = await axiosInstance.post('/communication/messages/', {
                recipient: recipientId,
                content: content,
                message_type: messageType,
            });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    },

    /**
     * Get all messages (sent or received based on user role)
     */
    getMessages: async () => {
        try {
            const response = await axiosInstance.get('/communication/messages/');
            return response.data;
        } catch (error) {
            console.error('Error fetching messages:', error);
            throw error;
        }
    },

    /**
     * Get unread messages for students
     */
    getUnreadMessages: async () => {
        try {
            const response = await axiosInstance.get('/communication/messages/unread/');
            return response.data;
        } catch (error) {
            console.error('Error fetching unread messages:', error);
            throw error;
        }
    },

    /**
     * Mark a message as read
     * @param {number} messageId - Message ID
     */
    markAsRead: async (messageId) => {
        try {
            const response = await axiosInstance.post(`/communication/messages/${messageId}/mark_read/`);
            return response.data;
        } catch (error) {
            console.error('Error marking message as read:', error);
            throw error;
        }
    },

    /**
     * Mark all messages as read
     */
    markAllAsRead: async () => {
        try {
            const response = await axiosInstance.post('/communication/messages/mark_all_read/');
            return response.data;
        } catch (error) {
            console.error('Error marking all messages as read:', error);
            throw error;
        }
    },
};

export default messageService;
