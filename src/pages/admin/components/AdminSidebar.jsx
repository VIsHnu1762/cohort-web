import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    LayoutDashboard, Users, UserCheck, Trophy, Bell, Shield, Settings,
    ChevronLeft, ChevronRight, UserCog
} from 'lucide-react';
import snsctLogo from '../../../assets/snsct.jpeg';
import snscasLogo from '../../../assets/snscas.jpeg';
import './AdminSidebar.css';

const ADMIN_NAV_ITEMS = [
    { path: '/admin-dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/students', label: 'Total Students', icon: Users },
    { path: '/admin/mentors', label: 'Mentors Details', icon: UserCheck },
    { path: '/admin/assignments', label: 'Assign Mentors', icon: UserCog },
    { path: '/admin/leaderboard', label: 'Leaderboard', icon: Trophy },
    { path: '/admin/notifications', label: 'Notifications', icon: Bell },
    { path: '/admin/roles', label: 'Roles', icon: Shield },
    { path: '/admin/settings', label: 'Settings', icon: Settings },
];

const AdminSidebar = ({ isCollapsed, setIsCollapsed }) => {
    const location = useLocation();

    return (
        <motion.aside
            className={`admin-sidebar ${isCollapsed ? 'admin-sidebar--collapsed' : ''}`}
            initial={false}
            animate={{ width: isCollapsed ? '80px' : '260px' }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
            <div className="admin-sidebar-header">
                {!isCollapsed && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="admin-sidebar-logo"
                    >
                        <div className="admin-college-logos">
                            <img src={snsctLogo} alt="SNS College of Technology" className="admin-college-logo" />
                            <img src={snscasLogo} alt="SNS College of Arts & Science" className="admin-college-logo" />
                        </div>
                        <h2>Admin Panel</h2>
                    </motion.div>
                )}
                {isCollapsed && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="admin-sidebar-logo-collapsed"
                    >
                        <img src={snsctLogo} alt="SNSCT" className="admin-college-logo-small" />
                    </motion.div>
                )}
                <button
                    className="admin-sidebar-toggle"
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                >
                    {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
                </button>
            </div>

            <nav className="admin-sidebar-nav">
                {ADMIN_NAV_ITEMS.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`admin-sidebar-link ${isActive ? 'admin-sidebar-link--active' : ''}`}
                            title={isCollapsed ? item.label : ''}
                        >
                            <div className="admin-sidebar-icon">
                                <Icon size={22} />
                            </div>
                            {!isCollapsed && (
                                <motion.span
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    className="admin-sidebar-label"
                                >
                                    {item.label}
                                </motion.span>
                            )}
                            {isActive && (
                                <motion.div
                                    layoutId="active-indicator"
                                    className="admin-sidebar-active-indicator"
                                    initial={false}
                                    transition={{ duration: 0.3 }}
                                />
                            )}
                        </Link>
                    );
                })}
            </nav>
        </motion.aside>
    );
};

export default AdminSidebar;
