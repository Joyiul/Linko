// Linko App Theme Configuration - Exact colors from your logo
export const theme = {
  colors: {
    // Primary brand colors - exact from your Linko logo
    primary: '#A8D8A8',      // Soft sage green from logo
    primaryLight: '#C5E4C5',  // Lighter version
    primaryDark: '#8BC68B',   // Slightly darker green
    
    // Secondary colors - from the cute world character
    secondary: '#87CEEB',     // Sky blue from globe (exact)
    secondaryLight: '#B0DCEB', // Light blue
    secondaryDark: '#6BB6CD',  // Darker sky blue
    
    // Accent color - gray from "Linko" text
    accent: '#666666',        // Exact gray from logo text
    accentLight: '#999999',   // Light gray
    accentDark: '#444444',    // Dark gray
    
    // Neutral colors with logo influence
    background: '#FDFEFE',    // Almost white with tiny green hint
    surface: '#FFFFFF',       // Pure white
    surfaceVariant: '#F8FBF8', // Very light green tint
    
    // Text colors
    onPrimary: '#FFFFFF',     // White text on primary
    onSecondary: '#FFFFFF',   // White text on secondary
    onBackground: '#333333',  // Dark text on background
    onSurface: '#333333',     // Dark text on surface
    onSurfaceVariant: '#666666', // Logo gray for text
    
    // Semantic colors using logo palette
    success: '#A8D8A8',       // Use primary green
    warning: '#F4D03F',       // Soft yellow
    error: '#F1948A',         // Soft red
    info: '#87CEEB',          // Use secondary blue
    
    // Gradients using exact logo colors
    primaryGradient: 'linear-gradient(135deg, #A8D8A8 0%, #C5E4C5 100%)',
    secondaryGradient: 'linear-gradient(135deg, #87CEEB 0%, #B0DCEB 100%)',
    backgroundGradient: 'linear-gradient(135deg, #FDFEFE 0%, #F8FBF8 100%)',
    heroGradient: 'linear-gradient(135deg, #F8FBF8 0%, #FDFEFE 100%)',
  },
  
  typography: {
    // Match Learning Library font stack exactly
    fontFamily: '"Poppins", "Nunito", "Circular", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: '600',
      letterSpacing: '0.5px',
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    h2: {
      fontSize: '2rem',
      fontWeight: '600',
      letterSpacing: '0.5px',
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: '600',
      letterSpacing: '0.5px',
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: '600',
      letterSpacing: '0.5px',
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    body1: {
      fontSize: '1rem',
      fontWeight: '400',
      lineHeight: 1.6,
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: '400',
      lineHeight: 1.5,
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    },
    button: {
      fontSize: '0.9rem',
      fontWeight: '500',
      textTransform: 'none',
      letterSpacing: '0.02em',
      fontFamily: '"Poppins", "Nunito", "Circular", sans-serif'
    }
  },
  
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px'
  },
  
  borderRadius: {
    small: '8px',
    medium: '16px',
    large: '24px',
    xlarge: '32px',
    round: '50%',
    bubble: '20px'
  },
  
  shadows: {
    light: '0 2px 8px rgba(0,0,0,0.08), 0 2px 4px rgba(168,216,168,0.12)',
    medium: '0 4px 12px rgba(0,0,0,0.12), 0 4px 8px rgba(168,216,168,0.16)',
    heavy: '0 8px 24px rgba(0,0,0,0.16), 0 8px 16px rgba(168,216,168,0.20)',
    bubble: '0 6px 20px rgba(0,0,0,0.1), 0 4px 12px rgba(168,216,168,0.15)'
  }
};

export default theme;
