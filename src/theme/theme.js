// Global Theme System with Dark/Light Mode Support
// High-Fidelity Educational UI Theme

export const colors = {
  // Primary Colors
  yellow: '#ffcc00',
  black: '#000000',
  red: '#ffcc00',
  white: '#FFFFFF',
  
  // Greys
  grey: {
    50: '#F4F4F4',
    100: '#E0E0E0',
    200: '#BDBDBD',
    300: '#9E9E9E',
    400: '#757575',
    500: '#616161',
    600: '#424242',
    700: '#303030',
    800: '#212121',
    900: '#121212',
  },
  
  // Neon Accents
  neon: {
    yellow: '#FFE566',
    yellowGlow: 'rgba(247, 201, 72, 0.6)',
    red: '#ffcc00',
    redGlow: 'rgba(229, 57, 53, 0.5)',
    blue: '#42A5F5',
    blueGlow: 'rgba(66, 165, 245, 0.5)',
    green: '#66BB6A',
    greenGlow: 'rgba(102, 187, 106, 0.5)',
    purple: '#AB47BC',
    purpleGlow: 'rgba(171, 71, 188, 0.5)',
  },
  
  // Gradients
  gradients: {
    yellowRed: 'linear-gradient(135deg, #ffcc00 0%, #ffcc00 100%)',
    yellowRedHorizontal: 'linear-gradient(90deg, #ffcc00 0%, #ffcc00 100%)',
    yellowRedVertical: 'linear-gradient(180deg, #ffcc00 0%, #ffcc00 100%)',
    neonYellow: 'linear-gradient(135deg, #FFE566 0%, #ffcc00 100%)',
    darkOverlay: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%)',
    glassLight: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
    glassDark: 'linear-gradient(135deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.1) 100%)',
  },
};

export const typography = {
  fonts: {
    primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    secondary: "'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    display: "'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    mono: "'Fira Code', 'Courier New', monospace",
  },
  
  sizes: {
    xs: '0.75rem',      // 12px
    sm: '0.875rem',     // 14px
    base: '1rem',       // 16px
    lg: '1.125rem',     // 18px
    xl: '1.25rem',      // 20px
    '2xl': '1.5rem',    // 24px
    '3xl': '1.875rem',  // 30px
    '4xl': '2.25rem',   // 36px
    '5xl': '3rem',      // 48px
    '6xl': '3.75rem',   // 60px
  },
  
  weights: {
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  
  lineHeights: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
    loose: 2,
  },
};

export const spacing = {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
  16: '4rem',     // 64px
  20: '5rem',     // 80px
  24: '6rem',     // 96px
};

export const radii = {
  none: '0',
  sm: '0.375rem',   // 6px
  base: '0.5rem',   // 8px
  md: '0.75rem',    // 12px
  lg: '1rem',       // 16px
  xl: '1.25rem',    // 20px
  '2xl': '1.5rem',  // 24px
  full: '9999px',
};

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  
  // Neon Glows
  neonYellow: '0 0 20px rgba(247, 201, 72, 0.6), 0 0 40px rgba(247, 201, 72, 0.3)',
  neonRed: '0 0 20px rgba(229, 57, 53, 0.5), 0 0 40px rgba(229, 57, 53, 0.2)',
  neonBlue: '0 0 20px rgba(66, 165, 245, 0.5), 0 0 40px rgba(66, 165, 245, 0.2)',
  neonGreen: '0 0 20px rgba(102, 187, 106, 0.5), 0 0 40px rgba(102, 187, 106, 0.2)',
  
  // Glassmorphism
  glass: '0 8px 32px 0 rgba(0, 0, 0, 0.1)',
  glassHover: '0 8px 32px 0 rgba(0, 0, 0, 0.2)',
};

export const animations = {
  // Durations
  durations: {
    fast: '150ms',
    base: '250ms',
    slow: '350ms',
    slower: '500ms',
  },
  
  // Timing Functions
  easings: {
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    smooth: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
  },
  
  // Motion Presets
  hover: {
    lift: 'transform 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
    scale: 'transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    glow: 'box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  
  // Keyframes (CSS strings)
  keyframes: {
    pulse: `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
      }
    `,
    glow: `
      @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(247, 201, 72, 0.4); }
        50% { box-shadow: 0 0 40px rgba(247, 201, 72, 0.8); }
      }
    `,
    slideIn: `
      @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
    `,
    fadeIn: `
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    `,
    ripple: `
      @keyframes ripple {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(4); opacity: 0; }
      }
    `,
    float: `
      @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }
    `,
    rotate: `
      @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    `,
  },
};

// Glassmorphism Presets
export const glassmorphism = {
  light: {
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(10px) saturate(180%)',
    WebkitBackdropFilter: 'blur(10px) saturate(180%)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    boxShadow: shadows.glass,
  },
  
  medium: {
    background: 'rgba(255, 255, 255, 0.15)',
    backdropFilter: 'blur(16px) saturate(180%)',
    WebkitBackdropFilter: 'blur(16px) saturate(180%)',
    border: '1px solid rgba(255, 255, 255, 0.25)',
    boxShadow: shadows.glass,
  },
  
  heavy: {
    background: 'rgba(255, 255, 255, 0.2)',
    backdropFilter: 'blur(20px) saturate(200%)',
    WebkitBackdropFilter: 'blur(20px) saturate(200%)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    boxShadow: shadows.glassHover,
  },
  
  dark: {
    background: 'rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(16px) saturate(180%)',
    WebkitBackdropFilter: 'blur(16px) saturate(180%)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    boxShadow: shadows.glass,
  },
};

// Theme Modes
export const lightTheme = {
  mode: 'light',
  colors: {
    ...colors,
    background: {
      primary: '#FFFFFF',
      secondary: '#F4F4F4',
      tertiary: '#E0E0E0',
      elevated: '#FFFFFF',
    },
    text: {
      primary: '#000000',
      secondary: '#616161',
      tertiary: '#9E9E9E',
      inverse: '#FFFFFF',
    },
    border: {
      primary: '#E0E0E0',
      secondary: '#BDBDBD',
      focus: colors.yellow,
    },
    surface: {
      base: '#FFFFFF',
      hover: '#F4F4F4',
      active: '#E0E0E0',
      disabled: '#BDBDBD',
    },
  },
  glass: {
    ...glassmorphism.light,
    background: 'rgba(255, 255, 255, 0.7)',
  },
};

export const darkTheme = {
  mode: 'dark',
  colors: {
    ...colors,
    background: {
      primary: '#000000',
      secondary: '#121212',
      tertiary: '#212121',
      elevated: '#1E1E1E',
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#BDBDBD',
      tertiary: '#757575',
      inverse: '#000000',
    },
    border: {
      primary: '#303030',
      secondary: '#424242',
      focus: colors.yellow,
    },
    surface: {
      base: '#121212',
      hover: '#1E1E1E',
      active: '#303030',
      disabled: '#424242',
    },
  },
  glass: {
    ...glassmorphism.dark,
    background: 'rgba(18, 18, 18, 0.7)',
  },
};

// Export complete theme object
export const theme = {
  colors,
  typography,
  spacing,
  radii,
  shadows,
  animations,
  glassmorphism,
  lightTheme,
  darkTheme,
};

export default theme;
