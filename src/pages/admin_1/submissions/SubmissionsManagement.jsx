import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    FileCheck, Clock, CheckCircle, XCircle, Filter,
    Search, Eye, Calendar, User, Award, AlertCircle
} from 'lucide-react';
import StatCard from '../../../components/admin/StatCard';
import DataTable from '../../../components/admin/DataTable';
import Modal from '../../../components/admin/Modal';
import { submissionsData, mentorsData, studentsData } from '../../../data/mockAdminData';


const SubmissionsManagement = () => {
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [filterStatus, setFilterStatus] = useState('All');
    const [filterPillar, setFilterPillar] = useState('All');
    const [filterMentor, setFilterMentor] = useState('All');
    const [dateRange, setDateRange] = useState('All');

    // Get unique values for filters
    const pillars = ['All', 'CLT', 'SRI', 'CFC', 'IIPC', 'SCD'];
    const statuses = ['All', 'Pending', 'Approved', 'Rejected'];
    const mentorOptions = ['All', ...mentorsData.map(m => m.name)];
    const dateRanges = ['All', 'Today', 'This Week', 'This Month', 'Last 3 Months'];

    // Calculate stats
    const totalSubmissions = submissionsData.length;
    const pendingCount = submissionsData.filter(s => s.status === 'Pending').length;
    const approvedCount = submissionsData.filter(s => s.status === 'Approved').length;
    const rejectedCount = submissionsData.filter(s => s.status === 'Rejected').length;

    // Filter submissions
    const filteredSubmissions = submissionsData.filter(submission => {
        const matchesStatus = filterStatus === 'All' || submission.status === filterStatus;
        const matchesPillar = filterPillar === 'All' || submission.pillar === filterPillar;
        const matchesMentor = filterMentor === 'All' ||
            mentorsData.find(m => m.id === submission.mentorId)?.name === filterMentor;
        return matchesStatus && matchesPillar && matchesMentor;
    });

    // Get student name
    const getStudentName = (studentId) => {
        return studentsData.find(s => s.id === studentId)?.name || 'Unknown';
    };

    // Get mentor name
    const getMentorName = (mentorId) => {
        return mentorsData.find(m => m.id === mentorId)?.name || 'Unknown';
    };

    // Status badge component
    const StatusBadge = ({ status }) => {
        const colors = {
            Pending: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400',
            Approved: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
            Rejected: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
        };
        return (
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
                {status}
            </span>
        );
    };

    // Table columns configuration
    const columns = [
        {
            key: 'student',
            label: 'Student',
            sortable: true,
            render: (row) => (
                <div className="flex items-center gap-2">
                    <User size={16} className="text-gray-400" />
                    <span className="font-medium">{getStudentName(row.studentId)}</span>
                </div>
            )
        },
        {
            key: 'pillar',
            label: 'Pillar',
            sortable: true,
            render: (row) => (
                <span className="px-2 py-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 rounded text-sm font-medium">
                    {row.pillar}
                </span>
            )
        },
        {
            key: 'submittedAt',
            label: 'Submitted',
            sortable: true,
            render: (row) => (
                <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
                    <Calendar size={14} />
                    {new Date(row.submittedAt).toLocaleDateString()}
                </div>
            )
        },
        {
            key: 'mentor',
            label: 'Mentor',
            sortable: true,
            render: (row) => (
                <span className="text-sm text-gray-700 dark:text-gray-300">
                    {getMentorName(row.mentorId)}
                </span>
            )
        },
        {
            key: 'status',
            label: 'Status',
            sortable: true,
            render: (row) => <StatusBadge status={row.status} />
        },
        {
            key: 'xpAwarded',
            label: 'XP',
            sortable: true,
            render: (row) => (
                <div className="flex items-center gap-1">
                    <Award size={14} className="text-purple-500" />
                    <span className="font-semibold text-purple-600 dark:text-purple-400">
                        {row.xpAwarded || 0}
                    </span>
                </div>
            )
        }
    ];

    // Handle row click to open detail modal
    const handleRowClick = (submission) => {
        setSelectedSubmission(submission);
        setIsModalOpen(true);
    };

    // Mock approve/reject handlers
    const handleApprove = () => {
        console.log('Approving submission:', selectedSubmission.id);
        setIsModalOpen(false);
    };

    const handleReject = () => {
        console.log('Rejecting submission:', selectedSubmission.id);
        setIsModalOpen(false);
    };

    return (
        <div className="p-6 min-h-screen">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            Submissions Management
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            Review and manage student pillar submissions
                        </p>
                    </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <StatCard
                        title="Total Submissions"
                        value={totalSubmissions}
                        icon={FileCheck}
                        iconColor="bg-indigo-600"
                    />
                    <StatCard
                        title="Pending Review"
                        value={pendingCount}
                        icon={Clock}
                        iconColor="bg-amber-600"
                        trend={{ value: -12.3, isPositive: false }}
                        trendLabel="vs last week"
                    />
                    <StatCard
                        title="Approved"
                        value={approvedCount}
                        icon={CheckCircle}
                        iconColor="bg-green-600"
                    />
                    <StatCard
                        title="Rejected"
                        value={rejectedCount}
                        icon={XCircle}
                        iconColor="bg-red-600"
                    />
                </div>
            </div>

            {/* Filters */}
            <div className="glass-card p-4 mb-6">
                <div className="flex items-center gap-2 mb-4">
                    <Filter size={20} className="text-gray-600 dark:text-gray-400" />
                    <h3 className="font-semibold text-gray-900 dark:text-white">Filters</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Status
                        </label>
                        <select
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value)}
                            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                        >
                            {statuses.map(status => (
                                <option key={status} value={status}>{status}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Pillar
                        </label>
                        <select
                            value={filterPillar}
                            onChange={(e) => setFilterPillar(e.target.value)}
                            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                        >
                            {pillars.map(pillar => (
                                <option key={pillar} value={pillar}>{pillar}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Mentor
                        </label>
                        <select
                            value={filterMentor}
                            onChange={(e) => setFilterMentor(e.target.value)}
                            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                        >
                            {mentorOptions.map(mentor => (
                                <option key={mentor} value={mentor}>{mentor}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Date Range
                        </label>
                        <select
                            value={dateRange}
                            onChange={(e) => setDateRange(e.target.value)}
                            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                        >
                            {dateRanges.map(range => (
                                <option key={range} value={range}>{range}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Submissions Table */}
            <DataTable
                columns={columns}
                data={filteredSubmissions}
                onRowClick={handleRowClick}
                searchable={true}
                sortable={true}
                pageSize={15}
            />

            {/* Submission Detail Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Submission Details"
                size="lg"
            >
                {selectedSubmission && (
                    <div className="space-y-6">
                        {/* Header Info */}
                        <div className="flex items-start justify-between">
                            <div>
                                <div className="flex items-center gap-3 mb-2">
                                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                                        {getStudentName(selectedSubmission.studentId)}
                                    </h3>
                                    <StatusBadge status={selectedSubmission.status} />
                                </div>
                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                    Submitted on {new Date(selectedSubmission.submittedAt).toLocaleDateString()} at{' '}
                                    {new Date(selectedSubmission.submittedAt).toLocaleTimeString()}
                                </p>
                            </div>
                            <div className="text-right">
                                <span className="px-4 py-2 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 rounded-lg font-bold text-lg">
                                    {selectedSubmission.pillar}
                                </span>
                            </div>
                        </div>

                        {/* Submission Details */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Assigned Mentor</p>
                                <p className="font-semibold text-gray-900 dark:text-white">
                                    {getMentorName(selectedSubmission.mentorId)}
                                </p>
                            </div>
                            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">XP Awarded</p>
                                <div className="flex items-center gap-2">
                                    <Award className="text-purple-500" size={20} />
                                    <p className="font-semibold text-purple-600 dark:text-purple-400 text-lg">
                                        {selectedSubmission.xpAwarded || 0} XP
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Evidence Section */}
                        <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                                <FileCheck size={18} />
                                Submission Evidence
                            </h4>
                            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                                    {selectedSubmission.description}
                                </p>
                                {selectedSubmission.evidenceUrl && (
                                    <div className="mt-3">
                                        <a
                                            href={selectedSubmission.evidenceUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                                        >
                                            <Eye size={16} />
                                            View Evidence
                                        </a>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Timeline */}
                        {selectedSubmission.timeline && (
                            <div>
                                <h4 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                                    <Clock size={18} />
                                    Activity Timeline
                                </h4>
                                <div className="space-y-3">
                                    {selectedSubmission.timeline.map((event, idx) => (
                                        <div key={idx} className="flex items-start gap-3">
                                            <div className={`w-2 h-2 rounded-full mt-2 ${event.type === 'submitted' ? 'bg-blue-500' :
                                                event.type === 'reviewed' ? 'bg-purple-500' :
                                                    event.type === 'approved' ? 'bg-green-500' :
                                                        'bg-red-500'
                                                }`} />
                                            <div className="flex-1">
                                                <p className="text-sm font-medium text-gray-900 dark:text-white">
                                                    {event.action}
                                                </p>
                                                <p className="text-xs text-gray-600 dark:text-gray-400">
                                                    {new Date(event.timestamp).toLocaleString()}
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Feedback Section */}
                        {selectedSubmission.feedback && (
                            <div>
                                <h4 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                                    <AlertCircle size={18} />
                                    Mentor Feedback
                                </h4>
                                <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
                                    <p className="text-gray-700 dark:text-gray-300">
                                        {selectedSubmission.feedback}
                                    </p>
                                </div>
                            </div>
                        )}

                        {/* Actions */}
                        {selectedSubmission.status === 'Pending' && (
                            <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                                <button
                                    onClick={handleApprove}
                                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                                >
                                    <CheckCircle size={18} />
                                    Approve Submission
                                </button>
                                <button
                                    onClick={handleReject}
                                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                                >
                                    <XCircle size={18} />
                                    Reject Submission
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </Modal>
        </div>
    );
};

export default SubmissionsManagement;
