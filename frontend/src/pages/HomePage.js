import React from 'react';
import { useNavigate } from 'react-router-dom';
import { theme } from '../theme';
import Logo from '../components/Logo';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div style={{
      background: theme.colors.backgroundGradient,
      minHeight: '100vh',
      color: theme.colors.onBackground,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: theme.spacing.lg,
      textAlign: 'center'
    }}>
      {/* Hero Section */}
      <div style={{ 
        maxWidth: 800, 
        margin: '0 auto',
        textAlign: 'center',
        width: '100%'
      }}>
        {/* Enhanced Earth AI Assistant */}
        <div style={{
          marginBottom: theme.spacing.xl,
          display: 'flex',
          justifyContent: 'center'
        }}>
          <Logo size="hero" animated={true} showText={false} />
        </div>

        <h1 style={{ 
          ...theme.typography.h1,
          fontSize: '5rem',
          marginBottom: theme.spacing.lg, 
          fontWeight: '700',
          color: '#666666',
          textShadow: '4px 4px 8px rgba(0,0,0,0.2)',
          letterSpacing: '3px',
          textAlign: 'center',
          margin: `0 0 ${theme.spacing.lg}px 0`
        }}>
          Linko
        </h1>
        
        <h2 style={{ 
          ...theme.typography.h2,
          marginBottom: theme.spacing.lg, 
          fontWeight: '500',
          color: theme.colors.primary,
          textAlign: 'center'
        }}>
          Connect & Communicate with Confidence
        </h2>

        {/* AI Assistant Welcome Message */}
        <div style={{
          background: `linear-gradient(135deg, ${theme.colors.surface} 0%, rgba(255,255,255,0.9) 100%)`,
          borderRadius: theme.borderRadius.bubble,
          padding: theme.spacing.lg,
          marginBottom: theme.spacing.xl,
          boxShadow: theme.shadows.bubble,
          border: `2px solid ${theme.colors.primary}`,
          position: 'relative',
          maxWidth: '600px',
          margin: `0 auto ${theme.spacing.xl}px auto`
        }}>
          {/* Speech bubble pointer */}
          <div style={{
            position: 'absolute',
            top: '-20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '20px solid transparent',
            borderRight: '20px solid transparent',
            borderBottom: `20px solid ${theme.colors.primary}`
          }} />
          <div style={{
            position: 'absolute',
            top: '-17px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '18px solid transparent',
            borderRight: '18px solid transparent',
            borderBottom: '18px solid white'
          }} />
          
          <p style={{
            ...theme.typography.body1,
            fontSize: '1.1rem',
            color: theme.colors.onSurface,
            margin: 0,
            lineHeight: 1.6,
            fontWeight: '500'
          }}>
            👋 Hi there! I'm your friendly AI language assistant. I'm here to help you master English communication, 
            understand cultural nuances, and express yourself with confidence. Ready to start your language journey?
          </p>
        </div>

        {/* Feature Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: theme.spacing.xl,
          marginBottom: theme.spacing.xxl
        }}>
          {/* Listen & Learn Card */}
          <div style={{
            background: theme.colors.surface,
            borderRadius: theme.borderRadius.bubble,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.bubble,
            border: `2px solid ${theme.colors.primary}`,
            transition: 'all 0.3s ease',
            cursor: 'pointer',
            backdropFilter: 'blur(10px)'
          }}
          onClick={() => navigate('/listen')}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)';
            e.currentTarget.style.boxShadow = theme.shadows.heavy;
            e.currentTarget.style.borderColor = theme.colors.primaryDark;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = theme.shadows.bubble;
            e.currentTarget.style.borderColor = theme.colors.primary;
          }}>
            <div style={{ 
              fontSize: 48, 
              marginBottom: theme.spacing.md,
              color: theme.colors.primary
            }}>🎧</div>
            <h3 style={{ 
              ...theme.typography.h3,
              marginBottom: theme.spacing.md, 
              color: theme.colors.accent
            }}>Listen & Learn</h3>
            <p style={{ 
              ...theme.typography.body1,
              color: theme.colors.onSurfaceVariant
            }}>
              Upload audio files or record yourself speaking. Get instant transcripts and understand different tones and styles.
            </p>
          </div>

          {/* Practice Speaking Card */}
          <div style={{
            background: theme.colors.surface,
            borderRadius: theme.borderRadius.bubble,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.bubble,
            border: `2px solid ${theme.colors.secondary}`,
            transition: 'all 0.3s ease',
            cursor: 'pointer',
            backdropFilter: 'blur(10px)'
          }}
          onClick={() => navigate('/videos')}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)';
            e.currentTarget.style.boxShadow = theme.shadows.heavy;
            e.currentTarget.style.borderColor = theme.colors.secondaryDark;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = theme.shadows.bubble;
            e.currentTarget.style.borderColor = theme.colors.secondary;
          }}>
            <div style={{ 
              fontSize: 48, 
              marginBottom: theme.spacing.md,
              color: theme.colors.secondary
            }}>🎥</div>
            <h3 style={{ 
              ...theme.typography.h3,
              marginBottom: theme.spacing.md, 
              color: theme.colors.accent
            }}>Practice Speaking</h3>
            <p style={{ 
              ...theme.typography.body1,
              color: theme.colors.onSurfaceVariant
            }}>
              Record video or audio of yourself speaking. Get personalized feedback on tone, clarity, and communication style.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
