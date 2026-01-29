import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Send, Bell, Users, Target, Calendar, Trash2, 
    Eye, CheckCircle, AlertCircle, Megaphone, Filter
} from 'lucide-react';
import StatCard from '../../../components/admin/StatCard';
import DataTable from '../../../components/admin/DataTable';
import Modal from '../../../components/admin/Modal';
import { notificationsData, studentsData, mentorsData, floorsData } from '../../../data/mockAdminData';

const CommunicationCenter = () => {
    const [activeTab, setActiveTab] = useState('compose'); // 'compose' or 'history'
    const [announcement, setAnnouncement] = useState({
        title: '',
        message: '',
        targetAudience: 'All',
        priority: 'Normal',
        sendEmail: true,
        sendInApp: true
    });
    const [selectedNotification, setSelectedNotification] = useState(null);
    const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
    const [filterPriority, setFilterPriority] = useState('All');

    // Calculate stats
    const totalNotifications = notificationsData.length;
    const unreadCount = notificationsData.filter(n => !n.read).length;
    const todayCount = notificationsData.filter(n => {
        const today = new Date().toDateString();
        return new Date(n.timestamp).toDateString() === today;
    }).length;

    // Filter notifications
    const filteredNotifications = filterPriority === 'All' 
        ? notificationsData 
        : notificationsData.filter(n => n.priority === filterPriority);

    // Get recipient count based on target
    const getRecipientCount = (target) => {
        switch(target) {
            case 'All':
                return studentsData.length + mentorsData.length;
            case 'Students':
                return studentsData.length;
            case 'Mentors':
                return mentorsData.length;
            case 'Floor A':
            case 'Floor B':
            case 'Floor C':
            case 'Floor D':
                const floor = floorsData.find(f => f.name === target);
                return floor?.studentCount || 0;
            default:
                return 0;
        }
    };

    // Handle send announcement
    const handleSendAnnouncement = () => {
        if (!announcement.title || !announcement.message) {
            alert('Please fill in all required fields');
            return;
        }

        const recipientCount = getRecipientCount(announcement.targetAudience);
        
        if (confirm(`Send announcement to ${recipientCount} recipients?`)) {
            console.log('Sending announcement:', announcement);
            // Reset form
            setAnnouncement({
                title: '',
                message: '',
                targetAudience: 'All',
                priority: 'Normal',
                sendEmail: true,
                sendInApp: true
            });
            alert('Announcement sent successfully!');
        }
    };

    // Priority badge
    const PriorityBadge = ({ priority }) => {
        const colors = {
            High: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
            Normal: 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
            Low: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400'
        };
        return (
            <span className={`px-2 py-1 rounded text-xs font-medium ${colors[priority]}`}>
                {priority}
            </span>
        );
    };

    // Table columns
    const columns = [
        {
            key: 'title',
            label: 'Title',
            sortable: true,
            render: (row) => (
                <div className="flex items-center gap-2">
                    <Bell size={16} className="text-gray-400" />
                    <span className="font-medium">{row.title}</span>
                </div>
            )
        },
        {
            key: 'message',
            label: 'Message',
            render: (row) => (
                <span className="text-sm text-gray-600 dark:text-gray-400 truncate max-w-xs">
                    {row.message.substring(0, 60)}...
                </span>
            )
        },
        {
            key: 'timestamp',
            label: 'Sent',
            sortable: true,
            render: (row) => (
                <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
                    <Calendar size={14} />
                    {new Date(row.timestamp).toLocaleDateString()}
                </div>
            )
        },
        {
            key: 'priority',
            label: 'Priority',
            sortable: true,
            render: (row) => <PriorityBadge priority={row.priority} />
        },
        {
            key: 'read',
            label: 'Status',
            render: (row) => (
                <div className="flex items-center gap-1">
                    {row.read ? (
                        <CheckCircle size={16} className="text-green-500" />
                    ) : (
                        <AlertCircle size={16} className="text-amber-500" />
                    )}
                    <span className="text-sm">{row.read ? 'Read' : 'Unread'}</span>
                </div>
            )
        }
    ];

    return (
        <div className="p-6 min-h-screen">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            Communication Center
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            Send announcements and manage notifications
                        </p>
                    </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <StatCard
                        title="Total Sent"
                        value={totalNotifications}
                        icon={Megaphone}
                        iconColor="bg-indigo-600"
                    />
                    <StatCard
                        title="Unread"
                        value={unreadCount}
                        icon={AlertCircle}
                        iconColor="bg-amber-600"
                    />
                    <StatCard
                        title="Sent Today"
                        value={todayCount}
                        icon={Calendar}
                        iconColor="bg-green-600"
                    />
                    <StatCard
                        title="Total Users"
                        value={studentsData.length + mentorsData.length}
                        icon={Users}
                        iconColor="bg-purple-600"
                    />
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-6">
                <button
                    onClick={() => setActiveTab('compose')}
                    className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
                        activeTab === 'compose'
                            ? 'bg-indigo-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                    }`}
                >
                    <div className="flex items-center justify-center gap-2">
                        <Send size={18} />
                        Compose Announcement
                    </div>
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
                        activeTab === 'history'
                            ? 'bg-indigo-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                    }`}
                >
                    <div className="flex items-center justify-center gap-2">
                        <Bell size={18} />
                        Notification History
                    </div>
                </button>
            </div>

            {/* Compose Tab */}
            {activeTab === 'compose' && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-6"
                >
                    <div className="space-y-6">
                        {/* Title */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Announcement Title *
                            </label>
                            <input
                                type="text"
                                value={announcement.title}
                                onChange={(e) => setAnnouncement({ ...announcement, title: e.target.value })}
                                className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 text-lg"
                                placeholder="Enter announcement title..."
                            />
                        </div>

                        {/* Message */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Message *
                            </label>
                            <textarea
                                value={announcement.message}
                                onChange={(e) => setAnnouncement({ ...announcement, message: e.target.value })}
                                rows={6}
                                className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="Write your announcement message here..."
                            />
                            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                {announcement.message.length} characters
                            </p>
                        </div>

                        {/* Target Audience and Priority */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Target Audience
                                </label>
                                <select
                                    value={announcement.targetAudience}
                                    onChange={(e) => setAnnouncement({ ...announcement, targetAudience: e.target.value })}
                                    className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                >
                                    <option value="All">All Users ({studentsData.length + mentorsData.length})</option>
                                    <option value="Students">Students Only ({studentsData.length})</option>
                                    <option value="Mentors">Mentors Only ({mentorsData.length})</option>
                                    {floorsData.map(floor => (
                                        <option key={floor.id} value={floor.name}>
                                            {floor.name} ({floor.studentCount} students)
                                        </option>
                                    ))}
                                </select>
                                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                    <Target size={14} className="inline mr-1" />
                                    {getRecipientCount(announcement.targetAudience)} recipients
                                </p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Priority Level
                                </label>
                                <select
                                    value={announcement.priority}
                                    onChange={(e) => setAnnouncement({ ...announcement, priority: e.target.value })}
                                    className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                >
                                    <option value="High">High Priority</option>
                                    <option value="Normal">Normal Priority</option>
                                    <option value="Low">Low Priority</option>
                                </select>
                            </div>
                        </div>

                        {/* Delivery Options */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                                Delivery Options
                            </label>
                            <div className="space-y-2">
                                <div className="flex items-center gap-3">
                                    <input
                                        type="checkbox"
                                        id="sendInApp"
                                        checked={announcement.sendInApp}
                                        onChange={(e) => setAnnouncement({ ...announcement, sendInApp: e.target.checked })}
                                        className="w-4 h-4 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500"
                                    />
                                    <label htmlFor="sendInApp" className="text-sm text-gray-700 dark:text-gray-300">
                                        Send as in-app notification
                                    </label>
                                </div>
                                <div className="flex items-center gap-3">
                                    <input
                                        type="checkbox"
                                        id="sendEmail"
                                        checked={announcement.sendEmail}
                                        onChange={(e) => setAnnouncement({ ...announcement, sendEmail: e.target.checked })}
                                        className="w-4 h-4 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500"
                                    />
                                    <label htmlFor="sendEmail" className="text-sm text-gray-700 dark:text-gray-300">
                                        Send email notification
                                    </label>
                                </div>
                            </div>
                        </div>

                        {/* Send Button */}
                        <div className="flex gap-3 pt-4">
                            <button
                                onClick={handleSendAnnouncement}
                                className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
                                disabled={!announcement.title || !announcement.message}
                            >
                                <Send size={20} />
                                Send Announcement
                            </button>
                            <button
                                onClick={() => setAnnouncement({
                                    title: '',
                                    message: '',
                                    targetAudience: 'All',
                                    priority: 'Normal',
                                    sendEmail: true,
                                    sendInApp: true
                                })}
                                className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors font-medium"
                            >
                                Clear
                            </button>
                        </div>
                    </div>
                </motion.div>
            )}

            {/* History Tab */}
            {activeTab === 'history' && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    {/* Filter */}
                    <div className="glass-card p-4 mb-6">
                        <div className="flex items-center gap-4">
                            <Filter size={20} className="text-gray-600 dark:text-gray-400" />
                            <select
                                value={filterPriority}
                                onChange={(e) => setFilterPriority(e.target.value)}
                                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="All">All Priorities</option>
                                <option value="High">High Priority</option>
                                <option value="Normal">Normal Priority</option>
                                <option value="Low">Low Priority</option>
                            </select>
                        </div>
                    </div>

                    {/* Notifications Table */}
                    <DataTable
                        columns={columns}
                        data={filteredNotifications}
                        onRowClick={(notification) => {
                            setSelectedNotification(notification);
                            setIsDetailModalOpen(true);
                        }}
                        searchable={true}
                        sortable={true}
                        pageSize={10}
                    />
                </motion.div>
            )}

            {/* Notification Detail Modal */}
            <Modal
                isOpen={isDetailModalOpen}
                onClose={() => setIsDetailModalOpen(false)}
                title="Notification Details"
                size="md"
            >
                {selectedNotification && (
                    <div className="space-y-4">
                        <div className="flex items-start justify-between">
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                                {selectedNotification.title}
                            </h3>
                            <PriorityBadge priority={selectedNotification.priority} />
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                                {selectedNotification.message}
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400">Sent</p>
                                <p className="font-medium text-gray-900 dark:text-white">
                                    {new Date(selectedNotification.timestamp).toLocaleString()}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
                                <div className="flex items-center gap-2">
                                    {selectedNotification.read ? (
                                        <>
                                            <CheckCircle size={16} className="text-green-500" />
                                            <span className="font-medium text-gray-900 dark:text-white">Read</span>
                                        </>
                                    ) : (
                                        <>
                                            <AlertCircle size={16} className="text-amber-500" />
                                            <span className="font-medium text-gray-900 dark:text-white">Unread</span>
                                        </>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </Modal>
        </div>
    );
};

export default CommunicationCenter;
