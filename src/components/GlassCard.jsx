import React from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../theme/ThemeContext';
import './GlassCard.css';

export const GlassCard = ({ 
  children, 
  className = '', 
  variant = 'medium',
  hoverable = true,
  animated = true,
  ...props 
}) => {
  const { theme } = useTheme();
  
  const variants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.5, ease: 'easeOut' }
    },
    hover: hoverable ? { 
      y: -4,
      transition: { duration: 0.25, ease: 'easeOut' }
    } : {}
  };

  const Component = animated ? motion.div : 'div';

  return (
    <Component
      className={`glass-card glass-card--${variant} ${className}`}
      variants={animated ? variants : undefined}
      initial={animated ? 'hidden' : undefined}
      animate={animated ? 'visible' : undefined}
      whileHover={animated && hoverable ? 'hover' : undefined}
      {...props}
    >
      {children}
    </Component>
  );
};

export default GlassCard;
