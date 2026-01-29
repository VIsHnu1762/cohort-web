import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Search, Filter, Plus, UserCheck, Users, TrendingUp,
    Award, Clock, ChevronRight, Mail, Phone, MapPin, Edit, Trash2
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import StatCard from '../../../components/admin/StatCard';
import Modal from '../../../components/admin/Modal';
import ChartWrapper from '../../../components/admin/ChartWrapper';
import { mentorsData, studentsData } from '../../../data/mockAdminData';
import './MentorManagement.css';

const MentorManagement = () => {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedMentor, setSelectedMentor] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

    // Filter mentors
    const filteredMentors = mentorsData.filter(mentor => {
        const matchesSearch = mentor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            mentor.email.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesSearch;
    });

    // Get students for selected mentor
    const getMentorStudents = (mentorId) => {
        return studentsData.filter(student => student.mentorId === mentorId);
    };

    // Open mentor detail modal
    const handleMentorClick = (mentor) => {
        setSelectedMentor(mentor);
        setIsModalOpen(true);
    };

    // Mentor performance data for chart
    const getMentorPerformanceData = (mentor) => [
        { month: 'Aug', approvals: 18 },
        { month: 'Sep', approvals: 24 },
        { month: 'Oct', approvals: 28 },
        { month: 'Nov', approvals: 32 },
        { month: 'Dec', approvals: 15 },
    ];

    return (
        <div className="mentor-management-page">
            <div style={{ padding: '0 2rem' }}>
                {/* Header */}
                <div className="mb-6">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h1 className="page-title-mentor">
                                Mentor Management
                            </h1>
                            <p className="page-subtitle-mentor">
                                Manage mentors, assign students, and track performance
                            </p>
                        </div>
                        <button
                            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            onClick={() => {/* Add mentor logic */ }}
                        >
                            <Plus size={20} />
                            Add Mentor
                        </button>
                    </div>

                    {/* Stats - Dashboard Style */}
                    <div className="mentor-stats-dashboard">
                        <motion.div
                            className="mentor-stat-card-dashboard"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                        >
                            <div className="stat-icon-dashboard" style={{ backgroundColor: 'rgba(247, 201, 72, 0.2)' }}>
                                <UserCheck size={24} style={{ color: '#ffcc00' }} />
                            </div>
                            <div className="stat-content-dashboard">
                                <span className="stat-value-dashboard">{mentorsData.length}</span>
                                <span className="stat-label-dashboard">Total Mentors</span>
                            </div>
                        </motion.div>

                        <motion.div
                            className="mentor-stat-card-dashboard"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                        >
                            <div className="stat-icon-dashboard" style={{ backgroundColor: 'rgba(229, 57, 53, 0.2)' }}>
                                <TrendingUp size={24} style={{ color: '#ffcc00' }} />
                            </div>
                            <div className="stat-content-dashboard">
                                <span className="stat-value-dashboard">{(mentorsData.reduce((sum, m) => sum + m.approvalRate, 0) / mentorsData.length).toFixed(1)}%</span>
                                <span className="stat-label-dashboard">Avg Approval Rate</span>
                            </div>
                        </motion.div>

                        <motion.div
                            className="mentor-stat-card-dashboard"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="stat-icon-dashboard" style={{ backgroundColor: 'rgba(255, 193, 7, 0.2)' }}>
                                <Users size={24} style={{ color: '#FFC107' }} />
                            </div>
                            <div className="stat-content-dashboard">
                                <span className="stat-value-dashboard">{mentorsData.reduce((sum, m) => sum + m.studentsCount, 0)}</span>
                                <span className="stat-label-dashboard">Total Students</span>
                            </div>
                        </motion.div>

                        <motion.div
                            className="mentor-stat-card-dashboard"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 }}
                        >
                            <div className="stat-icon-dashboard" style={{ backgroundColor: 'rgba(76, 175, 80, 0.2)' }}>
                                <Clock size={24} style={{ color: '#4CAF50' }} />
                            </div>
                            <div className="stat-content-dashboard">
                                <span className="stat-value-dashboard">2.5h</span>
                                <span className="stat-label-dashboard">Avg Response Time</span>
                            </div>
                        </motion.div>
                    </div>

                    {/* Filters */}
                    <div className="glass-card p-4">
                        <div className="flex flex-col md:flex-row gap-4">
                            {/* Search */}
                            <div className="flex-1 relative">
                                <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search mentors..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                />
                            </div>

                            {/* View Toggle */}
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setViewMode('grid')}
                                    className={`px-4 py-2 rounded-lg transition-colors ${viewMode === 'grid'
                                        ? 'bg-indigo-600 text-white'
                                        : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
                                        }`}
                                >
                                    Grid
                                </button>
                                <button
                                    onClick={() => setViewMode('list')}
                                    className={`px-4 py-2 rounded-lg transition-colors ${viewMode === 'list'
                                        ? 'bg-indigo-600 text-white'
                                        : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
                                        }`}
                                >
                                    List
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Mentors Grid/List */}
                {viewMode === 'grid' ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredMentors.map((mentor, index) => (
                            <motion.div
                                key={mentor.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                                className="glass-card p-6 cursor-pointer hover:shadow-lg transition-shadow"
                                onClick={() => handleMentorClick(mentor)}
                            >
                                {/* Avatar & Name */}
                                <div className="flex items-start gap-4 mb-4">
                                    <img
                                        src={mentor.avatar}
                                        alt={mentor.name}
                                        className="w-16 h-16 rounded-full"
                                    />
                                    <div className="flex-1">
                                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                            {mentor.name}
                                        </h3>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            {mentor.department}
                                        </p>
                                        <div className="flex items-center gap-1 mt-1">
                                            <span className="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 text-xs rounded-full">
                                                {mentor.floor}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* Stats */}
                                <div className="grid grid-cols-2 gap-4 mb-4">
                                    <div>
                                        <p className="text-xs text-gray-500 dark:text-gray-400">Students</p>
                                        <p className="text-xl font-bold text-gray-900 dark:text-white">
                                            {mentor.studentsCount}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-500 dark:text-gray-400">Approval Rate</p>
                                        <p className="text-xl font-bold text-green-600 dark:text-green-400">
                                            {mentor.approvalRate}%
                                        </p>
                                    </div>
                                </div>

                                {/* Contact & Actions */}
                                <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                                    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                                        <Mail size={14} />
                                        <span className="truncate">{mentor.email}</span>
                                    </div>
                                    <ChevronRight size={20} className="text-gray-400" />
                                </div>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="glass-card overflow-hidden">
                        <table className="w-full">
                            <thead className="bg-gray-50 dark:bg-gray-800">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Mentor
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Department
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Floor
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Students
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Approval Rate
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                                {filteredMentors.map((mentor) => (
                                    <tr
                                        key={mentor.id}
                                        className="hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer"
                                        onClick={() => handleMentorClick(mentor)}
                                    >
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-3">
                                                <img
                                                    src={mentor.avatar}
                                                    alt={mentor.name}
                                                    className="w-10 h-10 rounded-full"
                                                />
                                                <div>
                                                    <p className="font-medium text-gray-900 dark:text-white">
                                                        {mentor.name}
                                                    </p>
                                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                                        {mentor.email}
                                                    </p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                                            {mentor.department}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="px-2 py-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 text-xs rounded-full">
                                                {mentor.floor}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                                            {mentor.studentsCount}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="text-sm font-semibold text-green-600 dark:text-green-400">
                                                {mentor.approvalRate}%
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                            <div className="flex items-center gap-2">
                                                <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
                                                    <Edit size={16} className="text-gray-600 dark:text-gray-400" />
                                                </button>
                                                <button className="p-2 hover:bg-red-100 dark:hover:bg-red-900/20 rounded-lg transition-colors">
                                                    <Trash2 size={16} className="text-red-600 dark:text-red-400" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* Mentor Detail Modal */}
                <Modal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    title={selectedMentor?.name || 'Mentor Details'}
                    size="xl"
                >
                    {selectedMentor && (
                        <div className="space-y-6">
                            {/* Basic Info */}
                            <div className="flex items-start gap-6">
                                <img
                                    src={selectedMentor.avatar}
                                    alt={selectedMentor.name}
                                    className="w-24 h-24 rounded-full"
                                />
                                <div className="flex-1">
                                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                        {selectedMentor.name}
                                    </h2>
                                    <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                                        <div className="flex items-center gap-2">
                                            <Mail size={16} />
                                            {selectedMentor.email}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <MapPin size={16} />
                                            {selectedMentor.department} • {selectedMentor.floor}
                                        </div>
                                    </div>
                                    <div className="flex gap-2 mt-3">
                                        {selectedMentor.specialization.map((spec, i) => (
                                            <span
                                                key={i}
                                                className="px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 text-xs rounded-full"
                                            >
                                                {spec}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Performance Stats */}
                            <div className="grid grid-cols-4 gap-4">
                                <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                                        {selectedMentor.studentsCount}
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">Students</p>
                                </div>
                                <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                                        {selectedMentor.approvalRate}%
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">Approval Rate</p>
                                </div>
                                <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                                        {selectedMentor.totalApprovals}
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">Approvals</p>
                                </div>
                                <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">
                                        {selectedMentor.avgVerificationTime}
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">Avg Time</p>
                                </div>
                            </div>

                            {/* Performance Chart */}
                            <ChartWrapper title="Monthly Approval Trend" height="250px">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={getMentorPerformanceData(selectedMentor)}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
                                        <XAxis dataKey="month" stroke="#9CA3AF" style={{ fontSize: '12px' }} />
                                        <YAxis stroke="#9CA3AF" style={{ fontSize: '12px' }} />
                                        <Tooltip
                                            contentStyle={{
                                                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                                border: '1px solid #374151',
                                                borderRadius: '8px',
                                                color: '#fff'
                                            }}
                                        />
                                        <Bar dataKey="approvals" fill="#4F46E5" radius={[8, 8, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </ChartWrapper>

                            {/* Assigned Students */}
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                    Assigned Students ({selectedMentor.studentsCount})
                                </h3>
                                <div className="grid grid-cols-2 gap-3 max-h-60 overflow-y-auto">
                                    {getMentorStudents(selectedMentor.id).map(student => (
                                        <div
                                            key={student.id}
                                            className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
                                        >
                                            <div className="flex items-center justify-between">
                                                <div>
                                                    <p className="font-medium text-gray-900 dark:text-white">
                                                        {student.name}
                                                    </p>
                                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                                        {student.xp} XP
                                                    </p>
                                                </div>
                                                <div className="text-right">
                                                    <div className="w-8 h-8 bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400 rounded-full flex items-center justify-center text-sm font-bold">
                                                        #{student.rank}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Actions */}
                            <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                                <button className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                                    Reassign Students
                                </button>
                                <button className="flex-1 px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                                    View Floor Details
                                </button>
                                <button className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
                                    Remove Mentor
                                </button>
                            </div>
                        </div>
                    )}
                </Modal>
            </div>
        </div>
    );
}; export default MentorManagement;
