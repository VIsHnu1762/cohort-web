import React from 'react';

/**
 * ChartWrapper Component
 * Wrapper for Recharts to handle responsiveness and theme
 * 
 * @param {string} title - Chart title
 * @param {node} children - Recharts components
 * @param {string} height - Chart height (default: 300px)
 */
const ChartWrapper = ({ title, children, height = '300px', action }) => {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>
        {action && (
          <div className="text-sm">
            {action}
          </div>
        )}
      </div>
      <div style={{ height }} className="w-full">
        {children}
      </div>
    </div>
  );
};

export default ChartWrapper;
