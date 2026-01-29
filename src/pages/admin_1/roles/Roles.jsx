import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Shield, Users, Edit2, Check, X } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import './Roles.css';

const Roles = () => {
    const [roles, setRoles] = useState([
        {
            id: 1,
            name: 'Admin',
            userCount: 2,
            permissions: ['Full System Access', 'User Management', 'Content Management', 'Settings'],
            color: '#F44336'
        },
        {
            id: 2,
            name: 'Mentor',
            userCount: 12,
            permissions: ['View Students', 'Approve Submissions', 'Send Notifications'],
            color: '#2196F3'
        },
        {
            id: 3,
            name: 'Student',
            userCount: 150,
            permissions: ['Submit Work', 'View Progress', 'Access Resources'],
            color: '#4CAF50'
        },
        {
            id: 4,
            name: 'Floor Wing',
            userCount: 8,
            permissions: ['Manage Floor', 'View Floor Students', 'Generate Reports'],
            color: '#FF9800'
        }
    ]);

    return (
        <div className="roles-page">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div>
                    <h1 className="page-title">
                        <Shield size={32} />
                        Roles & Permissions
                    </h1>
                    <p className="page-subtitle">Manage user roles and their access permissions</p>
                </div>
                <Button variant="primary">
                    Add New Role
                </Button>
            </motion.div>

            <div className="roles-grid">
                {roles.map((role, index) => (
                    <motion.div
                        key={role.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 + index * 0.1 }}
                    >
                        <GlassCard>
                            <div className="role-card">
                                <div className="role-header">
                                    <div
                                        className="role-icon"
                                        style={{
                                            background: `${role.color}20`,
                                            color: role.color
                                        }}
                                    >
                                        <Shield size={24} />
                                    </div>
                                    <div className="role-info">
                                        <h3 className="role-name">{role.name}</h3>
                                        <p className="role-users">
                                            <Users size={14} />
                                            {role.userCount} users
                                        </p>
                                    </div>
                                    <button className="edit-btn">
                                        <Edit2 size={18} />
                                    </button>
                                </div>

                                <div className="permissions-section">
                                    <h4 className="permissions-title">Permissions</h4>
                                    <ul className="permissions-list">
                                        {role.permissions.map((permission, idx) => (
                                            <li key={idx} className="permission-item">
                                                <Check size={16} style={{ color: role.color }} />
                                                {permission}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default Roles;
