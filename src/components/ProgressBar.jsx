import React from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../theme/ThemeContext';
import './ProgressBar.css';

export const ProgressBar = ({ 
  progress = 0, 
  animated = true,
  showPercentage = true,
  variant = 'gradient',
  size = 'medium',
  className = '',
}) => {
  const { theme } = useTheme();
  const clampedProgress = Math.max(0, Math.min(100, progress));

  return (
    <div className={`progress-bar-container progress-bar--${size} ${className}`}>
      <div className="progress-bar-track">
        <motion.div
          className={`progress-bar-fill progress-bar-fill--${variant}`}
          initial={animated ? { width: 0 } : undefined}
          animate={{ width: `${clampedProgress}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        >
          {animated && (
            <span className="progress-bar-glow" />
          )}
        </motion.div>
      </div>
      
      {showPercentage && (
        <motion.span
          className="progress-bar-percentage"
          initial={animated ? { opacity: 0 } : undefined}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          {Math.round(clampedProgress)}%
        </motion.span>
      )}
    </div>
  );
};

export default ProgressBar;
