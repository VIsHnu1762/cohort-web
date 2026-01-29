import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrendingUp, TrendingDown, AlertTriangle, Award, Target, X } from 'lucide-react';
import gamificationAPI from '../services/gamification';
import './ProgressAlert.css';

const ProgressAlert = () => {
  const [alertData, setAlertData] = useState(null);
  const [showAlert, setShowAlert] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    // Check for progress notifications at random intervals
    const checkProgress = async () => {
      try {
        const response = await gamificationAPI.getMyComparison();
        const data = response.data;

        // Only show alert if student should be notified
        if (data.should_show_alert && !dismissed) {
          setAlertData(data);
          
          // Random delay between 5-15 seconds before showing
          const randomDelay = Math.random() * 10000 + 5000;
          setTimeout(() => {
            setShowAlert(true);
          }, randomDelay);
        }
      } catch (err) {
        console.error('Error fetching progress comparison:', err);
      }
    };

    // Check immediately
    checkProgress();

    // Then check at random intervals (30-90 seconds)
    const intervalId = setInterval(() => {
      if (!dismissed) {
        checkProgress();
      }
    }, Math.random() * 60000 + 30000);

    return () => clearInterval(intervalId);
  }, [dismissed]);

  const handleDismiss = () => {
    setShowAlert(false);
    setDismissed(true);
  };

  const getAlertConfig = (urgencyLevel) => {
    const configs = {
      success: {
        icon: Award,
        gradient: 'linear-gradient(135deg, #10b981, #059669)',
        borderColor: '#10b981',
        glowColor: 'rgba(16, 185, 129, 0.5)',
      },
      info: {
        icon: Target,
        gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)',
        borderColor: '#3b82f6',
        glowColor: 'rgba(59, 130, 246, 0.5)',
      },
      warning: {
        icon: TrendingUp,
        gradient: 'linear-gradient(135deg, #f59e0b, #d97706)',
        borderColor: '#f59e0b',
        glowColor: 'rgba(245, 158, 11, 0.5)',
      },
      danger: {
        icon: TrendingDown,
        gradient: 'linear-gradient(135deg, #ef4444, #dc2626)',
        borderColor: '#ef4444',
        glowColor: 'rgba(239, 68, 68, 0.5)',
      },
      critical: {
        icon: AlertTriangle,
        gradient: 'linear-gradient(135deg, #dc2626, #991b1b)',
        borderColor: '#dc2626',
        glowColor: 'rgba(220, 38, 38, 0.7)',
      },
    };
    return configs[urgencyLevel] || configs.info;
  };

  if (!alertData) return null;

  const config = getAlertConfig(alertData.urgency_level);
  const Icon = config.icon;

  return (
    <AnimatePresence>
      {showAlert && (
        <>
          {/* Overlay */}
          <motion.div
            className="progress-alert-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleDismiss}
          />

          {/* Alert Card */}
          <motion.div
            className="progress-alert-container"
            initial={{ scale: 0.5, opacity: 0, y: 100, rotate: -10 }}
            animate={{ 
              scale: 1, 
              opacity: 1, 
              y: 0, 
              rotate: 0,
              transition: {
                type: "spring",
                stiffness: 300,
                damping: 20
              }
            }}
            exit={{ 
              scale: 0.8, 
              opacity: 0, 
              y: -50,
              transition: { duration: 0.3 }
            }}
          >
            <div 
              className="progress-alert-card"
              style={{
                background: config.gradient,
                borderColor: config.borderColor,
                boxShadow: `0 20px 60px ${config.glowColor}, 0 0 40px ${config.glowColor}`
              }}
            >
              {/* Close Button */}
              <button className="progress-alert-close" onClick={handleDismiss}>
                <X size={20} />
              </button>

              {/* Icon with Animation */}
              <motion.div 
                className="progress-alert-icon"
                animate={{
                  scale: [1, 1.2, 1],
                  rotate: [0, 10, -10, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                <Icon size={64} />
              </motion.div>

              {/* Message */}
              <h2 className="progress-alert-message">{alertData.message}</h2>

              {/* Stats Grid */}
              <div className="progress-alert-stats">
                <div className="stat-item">
                  <span className="stat-label">Your Progress</span>
                  <span className="stat-value">{alertData.student_progress}%</span>
                </div>
                <div className="stat-divider"></div>
                <div className="stat-item">
                  <span className="stat-label">Batch Average</span>
                  <span className="stat-value">{alertData.batch_average}%</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="progress-alert-bar">
                <motion.div 
                  className="progress-alert-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${(alertData.student_progress / alertData.batch_average) * 100}%` }}
                  transition={{ duration: 1.5, delay: 0.5 }}
                />
              </div>

              {/* Rank Info */}
              <div className="progress-alert-rank">
                <span>You're in the top {100 - alertData.percentile_rank}% of {alertData.total_students} students</span>
              </div>

              {/* Action Button */}
              <motion.button
                className="progress-alert-action"
                onClick={handleDismiss}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Got It!
              </motion.button>

              {/* Particles Effect */}
              <div className="progress-alert-particles">
                {[...Array(15)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="particle"
                    initial={{ 
                      x: 0, 
                      y: 0, 
                      opacity: 1,
                      scale: Math.random() * 0.5 + 0.5
                    }}
                    animate={{
                      x: (Math.random() - 0.5) * 300,
                      y: (Math.random() - 0.5) * 300,
                      opacity: 0,
                    }}
                    transition={{
                      duration: Math.random() * 2 + 1,
                      delay: Math.random() * 0.5,
                      repeat: Infinity,
                      repeatDelay: Math.random() * 3
                    }}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default ProgressAlert;
