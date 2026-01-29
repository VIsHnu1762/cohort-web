import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';

/**
 * StatCard Component
 * Reusable card for displaying statistics with optional trend indicator
 * 
 * @param {string} title - Card title
 * @param {string|number} value - Main stat value
 * @param {object} icon - Lucide icon component
 * @param {string} iconColor - Icon background color class
 * @param {number} trend - Percentage change (optional)
 * @param {string} trendLabel - Label for trend (optional)
 * @param {function} onClick - Click handler (optional)
 */
const StatCard = ({
    title,
    value,
    icon: Icon,
    iconColor = 'bg-indigo-600',
    trend,
    trendLabel,
    onClick,
    loading = false
}) => {
    const isPositiveTrend = trend >= 0;

    if (loading) {
        return (
            <div className="glass-card p-6 animate-pulse">
                <div className="flex items-center justify-between">
                    <div className="flex-1">
                        <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-24 mb-3"></div>
                        <div className="h-8 bg-gray-300 dark:bg-gray-600 rounded w-20"></div>
                    </div>
                    <div className="w-12 h-12 bg-gray-300 dark:bg-gray-600 rounded-xl"></div>
                </div>
            </div>
        );
    }

    return (
        <motion.div
            whileHover={{ y: -4, scale: 1.02 }}
            transition={{ duration: 0.2 }}
            className={`glass-card p-6 ${onClick ? 'cursor-pointer' : ''}`}
            onClick={onClick}
        >
            <div className="flex items-center justify-between">
                <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                        {title}
                    </p>
                    <div className="flex items-baseline gap-2">
                        <h3 className="text-3xl font-bold text-gray-900 dark:text-white">
                            {value}
                        </h3>
                        {trend !== undefined && (
                            <div className={`flex items-center text-sm font-medium ${isPositiveTrend ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                                }`}>
                                {isPositiveTrend ? (
                                    <TrendingUp size={16} className="mr-1" />
                                ) : (
                                    <TrendingDown size={16} className="mr-1" />
                                )}
                                {Math.abs(trend)}%
                            </div>
                        )}
                    </div>
                    {trendLabel && (
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                            {trendLabel}
                        </p>
                    )}
                </div>

                {Icon && (
                    <div className={`${iconColor} p-3 rounded-xl`}>
                        <Icon size={24} className="text-white" />
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default StatCard;
