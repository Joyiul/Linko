import React from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from '../components/Logo';
import { theme } from '../theme';

export default function OnboardingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ 
      padding: theme.spacing.xxl, 
      textAlign: 'center',
      background: theme.colors.backgroundGradient,
      minHeight: '100vh',
      fontFamily: theme.typography.fontFamily
    }}>
      {/* Lingo Logo Section */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginBottom: theme.spacing.xxl
      }}>
        <Logo size="xlarge" animated={true} />
        <h1 style={{
          ...theme.typography.h1,
          fontSize: '4.5rem',
          fontWeight: '600',
          color: theme.colors.accent,
          margin: `4px 0 ${theme.spacing.md} 0`,
          textShadow: '3px 3px 0px rgba(0,0,0,0.2), 6px 6px 10px rgba(0,0,0,0.15)',
          letterSpacing: '0.05em',
          filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))',
          transform: 'perspective(500px) rotateX(15deg)',
          transition: 'all 0.3s ease'
        }}>
          Linko
        </h1>
        <p style={{
          ...theme.typography.body1,
          fontSize: '1.2rem',
          color: theme.colors.onSurfaceVariant,
          maxWidth: '500px',
          lineHeight: 1.6,
          margin: 0
        }}>
          Master emotions and communication with AI-powered speech analysis
        </p>
      </div>
      
      {/* Action Buttons */}
      <div style={{
        display: 'flex',
        gap: theme.spacing.lg,
        justifyContent: 'center',
        flexWrap: 'wrap'
      }}>
        <button 
          onClick={() => navigate('/listen')}
          style={{
            ...theme.typography.button,
            padding: `${theme.spacing.md} ${theme.spacing.xl}`,
            fontSize: theme.typography.h3.fontSize,
            fontWeight: '600',
            background: `linear-gradient(135deg, ${theme.colors.primary} 0%, ${theme.colors.primaryLight} 100%)`,
            color: theme.colors.onPrimary,
            border: 'none',
            borderRadius: theme.borderRadius.bubble,
            cursor: 'pointer',
            boxShadow: theme.shadows.bubble,
            transition: 'all 0.3s ease',
            minWidth: '160px'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'translateY(-3px)';
            e.target.style.boxShadow = theme.shadows.heavy;
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'translateY(0)';
            e.target.style.boxShadow = theme.shadows.bubble;
          }}
        >
          🎧 Listener
        </button>
        
        <button 
          onClick={() => navigate('/learners-base')}
          style={{
            padding: `${theme.spacing.md} ${theme.spacing.xl}`,
            fontSize: theme.typography.h3.fontSize,
            fontWeight: theme.typography.button.fontWeight,
            background: theme.colors.secondaryGradient,
            color: theme.colors.onSecondary,
            border: 'none',
            borderRadius: theme.borderRadius.large,
            cursor: 'pointer',
            boxShadow: theme.shadows.medium,
            transition: 'all 0.3s ease',
            minWidth: '160px'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'translateY(-2px)';
            e.target.style.boxShadow = theme.shadows.heavy;
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'translateY(0)';
            e.target.style.boxShadow = theme.shadows.medium;
          }}
        >
          🎓 Learner
        </button>
      </div>
    </div>
  );
}
