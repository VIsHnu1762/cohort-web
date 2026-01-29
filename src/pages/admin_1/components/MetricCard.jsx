import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../../../components/GlassCard';
import './MetricCard.css';

/**
 * Reusable Metric Card Component for Admin Dashboard
 * Displays key statistics with icon, value, label, and trend
 */
const MetricCard = ({ icon: Icon, label, value, trend, trendValue, color, delay = 0 }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay }}
            className="metric-card-wrapper"
        >
            <GlassCard variant="medium">
                <div className="metric-card">
                    <div className="metric-icon-container" style={{ backgroundColor: `${color}20` }}>
                        <Icon size={28} color={color} />
                    </div>
                    <div className="metric-details">
                        <h3 className="metric-value">{value}</h3>
                        <p className="metric-label">{label}</p>
                        {trend && (
                            <div className={`metric-trend ${trend}`}>
                                <span className="trend-indicator">{trend === 'up' ? '↑' : '↓'}</span>
                                <span className="trend-value">{trendValue}</span>
                            </div>
                        )}
                    </div>
                </div>
            </GlassCard>
        </motion.div>
    );
};

export default MetricCard;
