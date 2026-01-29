import React, { createContext, useContext, useState, useEffect } from 'react';
import { lightTheme, darkTheme } from './theme';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme-mode');
    return saved ? saved === 'dark' : false;
  });

  const theme = isDark ? darkTheme : lightTheme;

  useEffect(() => {
    localStorage.setItem('theme-mode', isDark ? 'dark' : 'light');
    
    // Update CSS custom properties
    const root = document.documentElement;
    root.style.setProperty('--bg-primary', theme.colors.background.primary);
    root.style.setProperty('--bg-secondary', theme.colors.background.secondary);
    root.style.setProperty('--bg-tertiary', theme.colors.background.tertiary);
    root.style.setProperty('--bg-elevated', theme.colors.background.elevated);
    
    root.style.setProperty('--text-primary', theme.colors.text.primary);
    root.style.setProperty('--text-secondary', theme.colors.text.secondary);
    root.style.setProperty('--text-tertiary', theme.colors.text.tertiary);
    root.style.setProperty('--text-inverse', theme.colors.text.inverse);
    
    root.style.setProperty('--border-primary', theme.colors.border.primary);
    root.style.setProperty('--border-secondary', theme.colors.border.secondary);
    
    root.style.setProperty('--surface-base', theme.colors.surface.base);
    root.style.setProperty('--surface-hover', theme.colors.surface.hover);
    root.style.setProperty('--surface-active', theme.colors.surface.active);
    
    root.style.setProperty('--glass-bg', theme.glass.background);
    
    // Set data attribute for theme
    root.setAttribute('data-theme', isDark ? 'dark' : 'light');
  }, [isDark, theme]);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <ThemeContext.Provider value={{ theme, isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
