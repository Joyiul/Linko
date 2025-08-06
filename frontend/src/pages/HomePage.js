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
        <h1 style={{ 
          fontSize: '5rem',
          marginBottom: theme.spacing.lg, 
          fontWeight: 'bold',
          color: '#666666',
          fontFamily: '"Fredoka One", "Comic Sans MS", "Chalkboard SE", "Bradley Hand", cursive',
          textShadow: '4px 4px 8px rgba(0,0,0,0.2)',
          letterSpacing: '3px',
          textAlign: 'center',
          margin: `0 0 ${theme.spacing.lg}px 0`
        }}>
          Linko
        </h1>
        
        <h2 style={{ 
          fontSize: theme.typography.h2.fontSize, 
          marginBottom: theme.spacing.xl, 
          fontWeight: 300,
          color: theme.colors.primary,
          textAlign: 'center'
        }}>
          Connect & Communicate with Confidence
        </h2>

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
            borderRadius: theme.borderRadius.large,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.medium,
            border: `2px solid ${theme.colors.primary}`,
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}
          onClick={() => navigate('/listen')}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-5px)';
            e.currentTarget.style.boxShadow = theme.shadows.heavy;
            e.currentTarget.style.borderColor = theme.colors.primaryDark;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = theme.shadows.medium;
            e.currentTarget.style.borderColor = theme.colors.primary;
          }}>
            <div style={{ 
              fontSize: 48, 
              marginBottom: theme.spacing.md,
              color: theme.colors.primary
            }}>🎧</div>
            <h3 style={{ 
              marginBottom: theme.spacing.md, 
              color: theme.colors.accent,
              fontSize: theme.typography.h3.fontSize
            }}>Listen & Learn</h3>
            <p style={{ 
              color: theme.colors.onSurfaceVariant, 
              lineHeight: theme.typography.body1.lineHeight 
            }}>
              Upload audio files or record yourself speaking. Get instant transcripts and understand different tones and styles.
            </p>
          </div>

          {/* Practice Speaking Card */}
          <div style={{
            background: theme.colors.surface,
            borderRadius: theme.borderRadius.large,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.medium,
            border: `2px solid ${theme.colors.secondary}`,
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}
          onClick={() => navigate('/videos')}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-5px)';
            e.currentTarget.style.boxShadow = theme.shadows.heavy;
            e.currentTarget.style.borderColor = theme.colors.secondaryDark;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = theme.shadows.medium;
            e.currentTarget.style.borderColor = theme.colors.secondary;
          }}>
            <div style={{ 
              fontSize: 48, 
              marginBottom: theme.spacing.md,
              color: theme.colors.secondary
            }}>🎥</div>
            <h3 style={{ 
              marginBottom: theme.spacing.md, 
              color: theme.colors.accent,
              fontSize: theme.typography.h3.fontSize
            }}>Practice Speaking</h3>
            <p style={{ 
              color: theme.colors.onSurfaceVariant, 
              lineHeight: theme.typography.body1.lineHeight 
            }}>
              Record video or audio of yourself speaking. Get personalized feedback on tone, clarity, and communication style.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
