import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Settings as SettingsIcon, Save, Bell, Shield, Database,
    Palette, Users, Mail, Lock, Globe, CheckCircle
} from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import './Settings.css';

const Settings = () => {
    const [settings, setSettings] = useState({
        // General
        appName: 'Cohort Management System',
        appDescription: 'Student and mentor management platform',
        maxFileSize: 10,
        sessionTimeout: 30,
        maintenanceMode: false,

        // Notifications
        emailNotifications: true,
        pushNotifications: true,
        smsNotifications: false,
        notificationSound: true,

        // Security
        twoFactorAuth: true,
        passwordExpiry: 90,
        minPasswordLength: 8,
        requireSpecialChars: true,

        // XP System
        baseXPReward: 100,
        bonusXPMultiplier: 1.5,
        dailyXPLimit: 1000,
        enableLeaderboard: true,

        // Pillars
        pillarSubmissionDeadline: 7,
        autoApprovalThreshold: 80,
        mentorReviewTime: 48
    });

    const [saveStatus, setSaveStatus] = useState(null);
    const [activeSection, setActiveSection] = useState('general');

    const handleSave = () => {
        console.log('Saving settings:', settings);
        setSaveStatus('saving');

        // Simulate API call
        setTimeout(() => {
            setSaveStatus('success');
            setTimeout(() => setSaveStatus(null), 3000);
        }, 1000);
    };

    const handleReset = () => {
        if (confirm('Reset all settings to default values?')) {
            setSettings({
                appName: 'Cohort Management System',
                appDescription: 'Student and mentor management platform',
                maxFileSize: 10,
                sessionTimeout: 30,
                maintenanceMode: false,
                emailNotifications: true,
                pushNotifications: true,
                smsNotifications: false,
                notificationSound: true,
                twoFactorAuth: true,
                passwordExpiry: 90,
                minPasswordLength: 8,
                requireSpecialChars: true,
                baseXPReward: 100,
                bonusXPMultiplier: 1.5,
                dailyXPLimit: 1000,
                enableLeaderboard: true,
                pillarSubmissionDeadline: 7,
                autoApprovalThreshold: 80,
                mentorReviewTime: 48
            });
        }
    };

    const sections = [
        { id: 'general', label: 'General', icon: Database },
        { id: 'notifications', label: 'Notifications', icon: Bell },
        { id: 'security', label: 'Security', icon: Shield },
        { id: 'xp', label: 'XP System', icon: Palette },
        { id: 'pillars', label: 'Pillars', icon: Users }
    ];

    return (
        <div className="settings-page">
            {/* Header */}
            <div className="page-header">
                <h1 className="page-title">
                    <SettingsIcon size={32} />
                    System Settings
                </h1>
                <p className="page-subtitle">
                    Configure application preferences and system options
                </p>
            </div>

            {/* Stats Overview */}
            <div className="settings-stats-grid">
                <motion.div
                    className="settings-stat-card"
                    whileHover={{ scale: 1.02 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                        <CheckCircle size={28} />
                    </div>
                    <div className="stat-content">
                        <h3 className="stat-value">{Object.values(settings).filter(v => v === true).length}</h3>
                        <p className="stat-label">Active Settings</p>
                    </div>
                </motion.div>

                <motion.div
                    className="settings-stat-card"
                    whileHover={{ scale: 1.02 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ffcc00 0%, #ffcc00 100%)' }}>
                        <Database size={28} />
                    </div>
                    <div className="stat-content">
                        <h3 className="stat-value">{settings.maxFileSize} MB</h3>
                        <p className="stat-label">Max File Size</p>
                    </div>
                </motion.div>

                <motion.div
                    className="settings-stat-card"
                    whileHover={{ scale: 1.02 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)' }}>
                        <Lock size={28} />
                    </div>
                    <div className="stat-content">
                        <h3 className="stat-value">{settings.sessionTimeout} min</h3>
                        <p className="stat-label">Session Timeout</p>
                    </div>
                </motion.div>

                <motion.div
                    className="settings-stat-card"
                    whileHover={{ scale: 1.02 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                        <Palette size={28} />
                    </div>
                    <div className="stat-content">
                        <h3 className="stat-value">{settings.bonusXPMultiplier}x</h3>
                        <p className="stat-label">XP Multiplier</p>
                    </div>
                </motion.div>
            </div>

            {/* Save Actions Bar */}
            <div className="settings-actions">
                <button
                    onClick={handleReset}
                    className="action-btn reset-btn"
                >
                    Reset to Defaults
                </button>
                <button
                    onClick={handleSave}
                    disabled={saveStatus === 'saving'}
                    className="action-btn save-btn"
                >
                    {saveStatus === 'saving' ? (
                        <>
                            <div className="spinner" />
                            Saving...
                        </>
                    ) : saveStatus === 'success' ? (
                        <>
                            <CheckCircle size={18} />
                            Saved!
                        </>
                    ) : (
                        <>
                            <Save size={18} />
                            Save Changes
                        </>
                    )}
                </button>
            </div>

            <div className="settings-layout">
                {/* Sidebar Navigation */}
                <GlassCard className="settings-sidebar">
                    <h3 className="sidebar-title">Categories</h3>
                    <nav className="settings-nav">
                        {sections.map(section => {
                            const Icon = section.icon;
                            return (
                                <motion.button
                                    key={section.id}
                                    onClick={() => setActiveSection(section.id)}
                                    className={`nav-item ${activeSection === section.id ? 'active' : ''}`}
                                    whileHover={{ x: 4 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <Icon size={20} />
                                    <span>{section.label}</span>
                                </motion.button>
                            );
                        })}
                    </nav>
                </GlassCard>

                {/* Settings Content */}
                <div className="settings-content-area">
                    {/* General Settings */}
                    {activeSection === 'general' && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <GlassCard className="settings-card">
                                <div className="card-header">
                                    <Database size={24} />
                                    <h2>General Settings</h2>
                                </div>

                                <div className="form-grid">
                                    <div className="form-field full-width">
                                        <label>Application Name</label>
                                        <input
                                            type="text"
                                            value={settings.appName}
                                            onChange={(e) => setSettings({ ...settings, appName: e.target.value })}
                                            className="input-field"
                                        />
                                    </div>

                                    <div className="form-field full-width">
                                        <label>Description</label>
                                        <textarea
                                            value={settings.appDescription}
                                            onChange={(e) => setSettings({ ...settings, appDescription: e.target.value })}
                                            rows={3}
                                            className="input-field"
                                        />
                                    </div>

                                    <div className="form-field">
                                        <label>Max File Upload Size (MB)</label>
                                        <input
                                            type="number"
                                            value={settings.maxFileSize}
                                            onChange={(e) => setSettings({ ...settings, maxFileSize: parseInt(e.target.value) || 0 })}
                                            className="input-field"
                                        />
                                    </div>

                                    <div className="form-field">
                                        <label>Session Timeout (minutes)</label>
                                        <input
                                            type="number"
                                            value={settings.sessionTimeout}
                                            onChange={(e) => setSettings({ ...settings, sessionTimeout: parseInt(e.target.value) || 0 })}
                                            className="input-field"
                                        />
                                    </div>

                                    <div className="form-field full-width toggle-field">
                                        <div className="toggle-label">
                                            <div>
                                                <h4>Maintenance Mode</h4>
                                                <p>Temporarily disable access for all users</p>
                                            </div>
                                            <label className="toggle-switch">
                                                <input
                                                    type="checkbox"
                                                    checked={settings.maintenanceMode}
                                                    onChange={(e) => setSettings({ ...settings, maintenanceMode: e.target.checked })}
                                                />
                                                <span className="toggle-slider"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </GlassCard>
                        </motion.div>
                    )}

                    {/* Notification Settings */}
                    {activeSection === 'notifications' && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <GlassCard className="settings-card">
                                <div className="card-header">
                                    <Bell size={24} />
                                    <h2>Notification Settings</h2>
                                </div>

                                <div className="toggle-list">
                                    {[
                                        { key: 'emailNotifications', label: 'Email Notifications', desc: 'Receive updates via email' },
                                        { key: 'pushNotifications', label: 'Push Notifications', desc: 'Browser push notifications' },
                                        { key: 'smsNotifications', label: 'SMS Notifications', desc: 'Critical alerts via SMS' },
                                        { key: 'notificationSound', label: 'Notification Sounds', desc: 'Play sound for new notifications' }
                                    ].map(({ key, label, desc }) => (
                                        <div key={key} className="toggle-item">
                                            <div className="toggle-info">
                                                <h4>{label}</h4>
                                                <p>{desc}</p>
                                            </div>
                                            <label className="toggle-switch">
                                                <input
                                                    type="checkbox"
                                                    checked={settings[key]}
                                                    onChange={(e) => setSettings({ ...settings, [key]: e.target.checked })}
                                                />
                                                <span className="toggle-slider"></span>
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </GlassCard>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Settings;
