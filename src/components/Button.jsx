import React from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../theme/ThemeContext';
import './Button.css';

export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium',
  withRipple = true,
  withGlow = false,
  disabled = false,
  className = '',
  onClick,
  ...props 
}) => {
  const { theme } = useTheme();
  const [ripples, setRipples] = React.useState([]);

  const handleClick = (e) => {
    if (disabled || !withRipple) {
      onClick?.(e);
      return;
    }

    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const ripple = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      id: Date.now(),
    };

    setRipples([...ripples, ripple]);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== ripple.id));
    }, 600);

    onClick?.(e);
  };

  return (
    <motion.button
      className={`btn btn--${variant} btn--${size} ${withGlow ? 'btn--glow' : ''} ${className}`}
      onClick={handleClick}
      disabled={disabled}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      <span className="btn__content">{children}</span>
      
      {withRipple && (
        <span className="btn__ripple-container">
          {ripples.map((ripple) => (
            <span
              key={ripple.id}
              className="btn__ripple"
              style={{
                left: ripple.x,
                top: ripple.y,
              }}
            />
          ))}
        </span>
      )}
    </motion.button>
  );
};

export default Button;
