import React, { useState } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { Camera, Plus, Calendar, Clock, Heart, Users } from 'lucide-react';
import GlassCard from '../../components/GlassCard';
import Button from '../../components/Button';
import './SRI.css';

export const SRI = () => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [reflection, setReflection] = useState('');
  const [activityTitle, setActivityTitle] = useState('');
  const [activityDate, setActivityDate] = useState('');

  // Mock data for quota and timeline
  const monthlyQuota = 4;
  const completedActivities = 2;
  const quotaPercentage = (completedActivities / monthlyQuota) * 100;

  const pastActivities = [
    { id: 1, title: 'Beach Cleanup Drive', date: '2025-11-15', hours: 4, type: 'Environment' },
    { id: 2, title: 'Old Age Home Visit', date: '2025-11-28', hours: 3, type: 'Community' },
  ];

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    const imageUrls = files.map(file => URL.createObjectURL(file));
    setSelectedImages([...selectedImages, ...imageUrls]);
  };

  const removeImage = (index) => {
    const newImages = selectedImages.filter((_, i) => i !== index);
    setSelectedImages(newImages);
  };

  const characterLimit = 500;
  const characterCount = reflection.length;
  const isNearLimit = characterCount > characterLimit * 0.8;

  return (
    <div className="sri-container">
      {/* Header */}
      <motion.div
        className="sri-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="sri-title">Social Responsibility Initiatives</h1>
        <p className="sri-subtitle">
          Make a difference in your community through meaningful social service
        </p>
      </motion.div>

      <div className="sri-layout">
        {/* Main Content */}
        <div className="sri-main">
          <GlassCard variant="medium" className="sri-form-card">
            <h2 className="sri-form-title">Log New Activity</h2>

            {/* Activity Title */}
            <div className="sri-input-group">
              <label className="sri-label">Activity Title</label>
              <input
                type="text"
                className="sri-input"
                placeholder="e.g., Community Clean-up Drive"
                value={activityTitle}
                onChange={(e) => setActivityTitle(e.target.value)}
              />
            </div>

            {/* Activity Date */}
            <div className="sri-input-group">
              <label className="sri-label">Activity Date</label>
              <div className="sri-input-with-icon">
                <Calendar className="sri-input-icon" size={20} />
                <input
                  type="date"
                  className="sri-input sri-input--with-icon"
                  value={activityDate}
                  onChange={(e) => setActivityDate(e.target.value)}
                />
              </div>
            </div>

            {/* Image Upload Grid */}
            <div className="sri-upload-section">
              <label className="sri-label">Activity Photos</label>
              <div className="sri-image-grid">
                {selectedImages.map((url, index) => (
                  <motion.div
                    key={index}
                    className="sri-image-card"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    whileHover={{ scale: 1.05, rotate: 2 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <img src={url} alt={`Upload ${index + 1}`} className="sri-image" />
                    <button
                      className="sri-image-remove"
                      onClick={() => removeImage(index)}
                    >
                      ×
                    </button>
                  </motion.div>
                ))}

                {/* Add Photo Tile */}
                <motion.label
                  className="sri-add-photo"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="sri-file-input"
                  />
                  <div className="sri-add-photo-content">
                    <motion.div
                      animate={{
                        scale: [1, 1.2, 1],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                      }}
                    >
                      <Plus size={32} />
                    </motion.div>
                    <span>Add Photos</span>
                  </div>
                </motion.label>
              </div>
            </div>

            {/* Reflection */}
            <div className="sri-reflection-section">
              <div className="sri-reflection-header">
                <label className="sri-label">Personal Reflection</label>
                <motion.span
                  className={`sri-character-count ${isNearLimit ? 'sri-character-count--warning' : ''}`}
                  animate={isNearLimit ? {
                    color: ['#ffcc00', '#ffcc00'],
                  } : {}}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  {characterCount}/{characterLimit}
                </motion.span>
              </div>
              <textarea
                className="sri-textarea"
                rows="6"
                placeholder="Share your experience, what you learned, and how this activity impacted you..."
                value={reflection}
                onChange={(e) => {
                  if (e.target.value.length <= characterLimit) {
                    setReflection(e.target.value);
                  }
                }}
              />
            </div>

            <div className="sri-form-actions">
              <Button
                variant="outline"
                onClick={() => alert('Activity saved as draft!')}
              >
                Save as Draft
              </Button>
              <Button
                variant="primary"
                withGlow
                onClick={() => {
                  if (activityTitle && activityDate && selectedImages.length > 0) {
                    alert('Activity submitted successfully!');
                    setActivityTitle('');
                    setActivityDate('');
                    setSelectedImages([]);
                    setReflection('');
                  } else {
                    alert('Please fill in all required fields');
                  }
                }}
              >
                Submit Activity
              </Button>
            </div>
          </GlassCard>
        </div>

        {/* Sidebar */}
        <div className="sri-sidebar">
          {/* Monthly Quota Card */}
          <GlassCard variant="heavy" className="sri-quota-card">
            <h3 className="sri-quota-title">Monthly Progress</h3>

            <div className="sri-quota-meter">
              <svg viewBox="0 0 200 200" className="sri-circular-meter">
                {/* Background Circle */}
                <circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="12"
                  className="sri-meter-bg"
                />

                {/* Animated Progress Circle */}
                <motion.circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke="url(#gradient)"
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 90}`}
                  initial={{ strokeDashoffset: 2 * Math.PI * 90 }}
                  animate={{
                    strokeDashoffset: 2 * Math.PI * 90 * (1 - quotaPercentage / 100),
                  }}
                  transition={{ duration: 1.5, ease: 'easeOut' }}
                  style={{
                    transform: 'rotate(-90deg)',
                    transformOrigin: '100px 100px',
                  }}
                />

                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#ffcc00" />
                    <stop offset="100%" stopColor="#ffcc00" />
                  </linearGradient>
                </defs>
              </svg>

              <div className="sri-quota-center">
                <motion.div
                  className="sri-quota-number"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: 'spring' }}
                >
                  {completedActivities}/{monthlyQuota}
                </motion.div>
                <div className="sri-quota-label">Activities</div>
              </div>
            </div>

            <div className="sri-quota-stats">
              <div className="sri-stat">
                <Clock size={20} />
                <div>
                  <div className="sri-stat-value">7 hours</div>
                  <div className="sri-stat-label">This Month</div>
                </div>
              </div>
              <div className="sri-stat">
                <Users size={20} />
                <div>
                  <div className="sri-stat-value">150+</div>
                  <div className="sri-stat-label">People Helped</div>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Activity Timeline */}
          <GlassCard variant="medium" className="sri-timeline-card">
            <h3 className="sri-timeline-title">Activity History</h3>

            <div className="sri-timeline">
              {pastActivities.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  className="sri-timeline-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.2 }}
                >
                  <motion.div
                    className="sri-timeline-node"
                    animate={{
                      boxShadow: [
                        '0 0 10px rgba(247, 201, 72, 0.4)',
                        '0 0 20px rgba(247, 201, 72, 0.8)',
                        '0 0 10px rgba(247, 201, 72, 0.4)',
                      ],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      delay: index * 0.3,
                    }}
                  />

                  <div className="sri-timeline-content">
                    <h4 className="sri-timeline-activity">{activity.title}</h4>
                    <div className="sri-timeline-meta">
                      <span className="sri-timeline-date">{activity.date}</span>
                      <span className="sri-timeline-type">{activity.type}</span>
                    </div>
                    <div className="sri-timeline-hours">
                      {activity.hours} hours
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};

export default SRI;
