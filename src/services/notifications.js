import api from './api';

// Get all notifications
export const getNotifications = async () => {
    const response = await api.get('/dashboard/notifications/');
    return response.data;
};

// Mark notification as read
export const markNotificationRead = async (notificationId) => {
    const response = await api.post(`/dashboard/notifications/${notificationId}/mark-read/`);
    return response.data;
};

// Delete a notification
export const deleteNotification = async (notificationId) => {
    const response = await api.delete(`/dashboard/notifications/${notificationId}/mark-read/`);
    return response.data;
};

// Delete all read notifications
export const deleteReadNotifications = async () => {
    const response = await api.delete('/dashboard/notifications/');
    return response.data;
};
