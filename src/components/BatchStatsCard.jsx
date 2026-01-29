import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, Award } from 'lucide-react';
import { motion } from 'framer-motion';
import gamificationAPI from '../services/gamification';
import './BatchStatsCard.css';

const BatchStatsCard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBatchStats();
  }, []);

  const fetchBatchStats = async () => {
    try {
      const response = await gamificationAPI.getBatchStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching batch stats:', err);
      // Set default stats if API fails
      setStats({
        average_progress: 0,
        total_students: 0,
        top_performers: 0
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) return null;

  return (
    <motion.div
      className="batch-stats-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.6 }}
    >
      <div className="batch-stats-header">
        <Users size={24} />
        <h3>Batch Progress</h3>
      </div>

      <div className="batch-stats-content">
        <div className="batch-main-stat">
          <span className="batch-stat-label">Average Progress</span>
          <div className="batch-stat-value-wrapper">
            <motion.span 
              className="batch-stat-value"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 200, delay: 0.4 }}
            >
              {stats.average_progress}%
            </motion.span>
          </div>
          <span className="batch-stat-sublabel">{stats.total_students} students in your batch</span>
        </div>

        {/* Visual Progress Bar */}
        <div className="batch-progress-bar">
          <motion.div 
            className="batch-progress-fill"
            initial={{ width: 0 }}
            animate={{ width: `${stats.average_progress}%` }}
            transition={{ duration: 1.5, delay: 0.6 }}
          />
        </div>
      </div>
    </motion.div>
  );
};

export default BatchStatsCard;
