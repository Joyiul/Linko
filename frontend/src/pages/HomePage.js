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
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
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
          color: theme.colors.primary
        }}>
          Connect & Communicate with Confidence
        </h2>

        <p style={{ 
          fontSize: theme.typography.body1.fontSize, 
          lineHeight: theme.typography.body1.lineHeight, 
          marginBottom: theme.spacing.xxl,
          color: theme.colors.onSurfaceVariant,
          maxWidth: 600,
          margin: `0 auto ${theme.spacing.xxl}px auto`
        }}>
          Perfect for English learners, neurodivergent individuals, and anyone wanting to improve their communication skills. 
          Get personalized feedback on your tone, clarity, and speaking style.
        </p>

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

        {/* User Type Selection */}
        <div style={{ marginBottom: theme.spacing.xxl }}>
          <h3 style={{ 
            marginBottom: theme.spacing.lg, 
            fontSize: theme.typography.h3.fontSize,
            color: theme.colors.accent
          }}>Choose Your Journey</h3>
          
          <div style={{
            display: 'flex',
            gap: theme.spacing.lg,
            justifyContent: 'center',
            flexWrap: 'wrap'
          }}>
            {/* English Learner Path */}
            <button
              onClick={() => navigate('/listen')}
              style={{
                padding: theme.spacing.lg,
                background: theme.colors.surface,
                border: `2px solid ${theme.colors.primary}`,
                borderRadius: theme.borderRadius.large,
                color: theme.colors.onSurface,
                fontSize: theme.typography.button.fontSize,
                fontWeight: 'bold',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: theme.spacing.sm,
                minWidth: 200,
                boxShadow: theme.shadows.light
              }}
              onMouseEnter={(e) => {
                e.target.style.background = theme.colors.primaryLight;
                e.target.style.transform = 'scale(1.05)';
                e.target.style.boxShadow = theme.shadows.medium;
              }}
              onMouseLeave={(e) => {
                e.target.style.background = theme.colors.surface;
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = theme.shadows.light;
              }}
            >
              <span style={{ fontSize: 24, color: theme.colors.primary }}>🌍</span>
              <span>English Learner</span>
              <span style={{ fontSize: 12, color: theme.colors.onSurfaceVariant }}>
                Perfect pronunciation & tone
              </span>
            </button>

            {/* Neurodivergent Support Path */}
            <button
              onClick={() => navigate('/videos')}
              style={{
                padding: theme.spacing.lg,
                background: theme.colors.surface,
                border: `2px solid ${theme.colors.secondary}`,
                borderRadius: theme.borderRadius.large,
                color: theme.colors.onSurface,
                fontSize: theme.typography.button.fontSize,
                fontWeight: 'bold',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: theme.spacing.sm,
                minWidth: 200,
                boxShadow: theme.shadows.light
              }}
              onMouseEnter={(e) => {
                e.target.style.background = theme.colors.secondaryLight;
                e.target.style.transform = 'scale(1.05)';
                e.target.style.boxShadow = theme.shadows.medium;
              }}
              onMouseLeave={(e) => {
                e.target.style.background = theme.colors.surface;
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = theme.shadows.light;
              }}
            >
              <span style={{ fontSize: 24, color: theme.colors.secondary }}>🧠</span>
              <span>Communication Support</span>
              <span style={{ fontSize: 12, color: theme.colors.onSurfaceVariant }}>
                Social cues & tone guidance
              </span>
            </button>

            {/* General Improvement Path */}
            <button
              onClick={() => navigate('/videos')}
              style={{
                padding: theme.spacing.lg,
                background: theme.colors.surface,
                border: `2px solid ${theme.colors.accent}`,
                borderRadius: theme.borderRadius.large,
                color: theme.colors.onSurface,
                fontSize: theme.typography.button.fontSize,
                fontWeight: 'bold',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: theme.spacing.sm,
                minWidth: 200,
                boxShadow: theme.shadows.light
              }}
              onMouseEnter={(e) => {
                e.target.style.background = theme.colors.accentLight;
                e.target.style.transform = 'scale(1.05)';
                e.target.style.boxShadow = theme.shadows.medium;
              }}
              onMouseLeave={(e) => {
                e.target.style.background = theme.colors.surface;
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = theme.shadows.light;
              }}
            >
              <span style={{ fontSize: 24, color: theme.colors.accent }}>🚀</span>
              <span>Skill Builder</span>
              <span style={{ fontSize: 12, color: theme.colors.onSurfaceVariant }}>
                Enhance speaking confidence
              </span>
            </button>
          </div>
        </div>

        {/* Features List */}
        <div style={{
          background: theme.colors.surface,
          borderRadius: theme.borderRadius.large,
          padding: theme.spacing.xl,
          boxShadow: theme.shadows.medium,
          border: `1px solid ${theme.colors.surfaceVariant}`,
          textAlign: 'left',
          maxWidth: 600,
          margin: `0 auto ${theme.spacing.xxl}px auto`
        }}>
          <h4 style={{ 
            textAlign: 'center', 
            marginBottom: theme.spacing.lg, 
            color: theme.colors.accent,
            fontSize: theme.typography.h3.fontSize
          }}>
            What You'll Get
          </h4>
          <ul style={{ 
            listStyle: 'none', 
            padding: 0, 
            margin: 0,
            lineHeight: 2
          }}>
            <li style={{ marginBottom: theme.spacing.sm, color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Instant transcripts</strong> of your speech
            </li>
            <li style={{ marginBottom: theme.spacing.sm, color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Tone analysis</strong> and emotional context
            </li>
            <li style={{ marginBottom: theme.spacing.sm, color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Personalized tips</strong> for clearer communication
            </li>
            <li style={{ marginBottom: theme.spacing.sm, color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Cultural guidance</strong> for better understanding
            </li>
            <li style={{ marginBottom: theme.spacing.sm, color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Practice exercises</strong> tailored to your needs
            </li>
            <li style={{ color: theme.colors.onSurface }}>
              <span style={{ marginRight: theme.spacing.sm, color: theme.colors.primary }}>•</span>
              <strong>Safe environment</strong> to practice without judgment
            </li>
          </ul>
        </div>

        {/* Call to Action */}
        <div>
          <button
            onClick={() => navigate('/videos')}
            style={{
              padding: `${theme.spacing.lg} ${theme.spacing.xxl}`,
              background: theme.colors.primaryGradient,
              border: 'none',
              borderRadius: theme.borderRadius.large,
              color: theme.colors.onPrimary,
              fontSize: theme.typography.h3.fontSize,
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: theme.shadows.medium
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = 'translateY(-3px)';
              e.target.style.boxShadow = theme.shadows.heavy;
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = theme.shadows.medium;
            }}
          >
            Start Your Journey
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer style={{
        position: 'absolute',
        bottom: theme.spacing.lg,
        textAlign: 'center',
        color: theme.colors.onSurfaceVariant,
        fontSize: theme.typography.body2.fontSize
      }}>
        <p>Built with love for inclusive communication</p>
      </footer>
    </div>
  );
}
