import api from './api';

// Get all announcements (mentor - their own, student - from their mentor)
export const getAnnouncements = async () => {
    try {
        const response = await api.get('/mentor/announcements/');
        return response.data;
    } catch (error) {
        console.error('Error fetching announcements:', error);
        throw error;
    }
};

// Create a new announcement (mentor only)
export const createAnnouncement = async (announcementData) => {
    try {
        const response = await api.post('/mentor/announcements/', announcementData);
        return response.data;
    } catch (error) {
        console.error('Error creating announcement:', error);
        throw error;
    }
};

// Update an announcement (mentor only)
export const updateAnnouncement = async (announcementId, announcementData) => {
    try {
        const response = await api.put(`/mentor/announcements/${announcementId}/`, announcementData);
        return response.data;
    } catch (error) {
        console.error('Error updating announcement:', error);
        throw error;
    }
};

// Delete an announcement (mentor only)
export const deleteAnnouncement = async (announcementId) => {
    try {
        await api.delete(`/mentor/announcements/${announcementId}/`);
    } catch (error) {
        console.error('Error deleting announcement:', error);
        throw error;
    }
};

// Get student announcements (student only)
export const getStudentAnnouncements = async () => {
    try {
        const response = await api.get('/dashboard/announcements/');
        return response.data;
    } catch (error) {
        console.error('Error fetching student announcements:', error);
        throw error;
    }
};

// Mark announcement as read (student only)
export const markAnnouncementAsRead = async (announcementId) => {
    try {
        const response = await api.post(`/dashboard/announcements/${announcementId}/mark-read/`);
        return response.data;
    } catch (error) {
        console.error('Error marking announcement as read:', error);
        throw error;
    }
};
