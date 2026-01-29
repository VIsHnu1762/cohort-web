import api from './api';

const floorWingAnnouncementService = {
    // Get all announcements for floor wing
    getAnnouncements: async () => {
        const response = await api.get('/profiles/floor-wing/announcements/');
        return response.data;
    },

    // Get announcement statistics
    getStats: async () => {
        const response = await api.get('/profiles/floor-wing/announcements/stats/');
        return response.data;
    },

    // Get single announcement
    getAnnouncement: async (id) => {
        const response = await api.get(`/profiles/floor-wing/announcements/${id}/`);
        return response.data;
    },

    // Create new announcement
    createAnnouncement: async (data) => {
        const response = await api.post('/profiles/floor-wing/announcements/', data);
        return response.data;
    },

    // Update announcement
    updateAnnouncement: async (id, data) => {
        const response = await api.patch(`/profiles/floor-wing/announcements/${id}/`, data);
        return response.data;
    },

    // Delete announcement
    deleteAnnouncement: async (id) => {
        const response = await api.delete(`/profiles/floor-wing/announcements/${id}/`);
        return response.data;
    },

    // Publish draft announcement
    publishAnnouncement: async (id) => {
        const response = await api.patch(`/profiles/floor-wing/announcements/${id}/`, {
            status: 'published'
        });
        return response.data;
    }
};

const studentAnnouncementService = {
    // Get announcements for student
    getAnnouncements: async () => {
        const response = await api.get('/profiles/student/announcements/');
        return response.data;
    },

    // Mark announcement as read
    markAsRead: async (id) => {
        const response = await api.post(`/profiles/student/announcements/${id}/mark_read/`);
        return response.data;
    },

    // Get unread count
    getUnreadCount: async () => {
        const response = await api.get('/profiles/student/announcements/unread_count/');
        return response.data;
    }
};

export { floorWingAnnouncementService, studentAnnouncementService };
