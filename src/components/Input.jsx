import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../theme/ThemeContext';
import './Input.css';

export const Input = ({ 
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  icon,
  className = '',
  floatingLabel = true,
  ...props 
}) => {
  const { theme } = useTheme();
  const [isFocused, setIsFocused] = useState(false);
  const hasValue = value && value.length > 0;

  return (
    <div className={`input-wrapper ${className}`}>
      <div className={`input-container ${isFocused ? 'input-container--focused' : ''} ${error ? 'input-container--error' : ''}`}>
        {icon && <span className="input-icon">{icon}</span>}
        
        <input
          type={type}
          className={`input-field ${floatingLabel ? 'input-field--floating' : ''} ${icon ? 'input-field--with-icon' : ''}`}
          placeholder={floatingLabel ? '' : placeholder}
          value={value}
          onChange={onChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          {...props}
        />
        
        {floatingLabel && label && (
          <motion.label
            className={`input-label ${isFocused || hasValue ? 'input-label--active' : ''} ${icon ? 'input-label--with-icon' : ''}`}
            initial={false}
            animate={{
              top: isFocused || hasValue ? '-0.75rem' : '50%',
              left: (isFocused || hasValue) ? '0.75rem' : (icon ? '3.25rem' : '1rem'),
              fontSize: isFocused || hasValue ? '0.75rem' : '1rem',
              color: error ? '#ffcc00' : isFocused ? '#ffcc00' : 'inherit',
            }}
            transition={{ duration: 0.2 }}
          >
            {label}
          </motion.label>
        )}
        
        {!floatingLabel && label && (
          <label className="input-label-static">{label}</label>
        )}
      </div>
      
      {error && (
        <motion.span
          className="input-error"
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {error}
        </motion.span>
      )}
    </div>
  );
};

export default Input;
