import React from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from '../components/Logo';

const LearnersBasePage = () => {
  const navigate = useNavigate();

  const buttonStyle = {
    padding: '20px 40px',
    fontSize: '18px',
    fontWeight: '600',
    color: '#FFFFFF',
    backgroundColor: '#4CAF50',
    border: 'none',
    borderRadius: '25px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    minWidth: '250px',
    fontFamily: 'Poppins, Nunito, Circular, -apple-system, BlinkMacSystemFont, sans-serif',
    boxShadow: '0 8px 20px rgba(76, 175, 80, 0.3)',
    backdropFilter: 'blur(10px)',
    margin: '15px'
  };

  const hoverStyle = {
    transform: 'translateY(-3px)',
    boxShadow: '0 12px 30px rgba(76, 175, 80, 0.4)',
    backgroundColor: '#45a049'
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #E8F5E8 0%, #B8E6B8 50%, #87CEEB 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      fontFamily: 'Poppins, Nunito, Circular, -apple-system, BlinkMacSystemFont, sans-serif'
    }}>
      {/* Header with Logo */}
      <div style={{
        textAlign: 'center',
        marginBottom: '60px'
      }}>
        <Logo size="hero" animated={true} />
        <h1 style={{
          fontSize: '48px',
          fontWeight: '700',
          color: '#2E7D32',
          marginTop: '20px',
          marginBottom: '10px',
          textShadow: '2px 2px 4px rgba(0,0,0,0.1)'
        }}>
          Learners Base
        </h1>
        <p style={{
          fontSize: '20px',
          color: '#4A5568',
          fontWeight: '400',
          maxWidth: '600px',
          lineHeight: '1.6'
        }}>
          Your learning hub for mastering communication skills and slang
        </p>
      </div>

      {/* Navigation Buttons */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '20px',
        maxWidth: '400px',
        width: '100%'
      }}>
        <button
          style={buttonStyle}
          onMouseEnter={(e) => {
            Object.assign(e.target.style, hoverStyle);
          }}
          onMouseLeave={(e) => {
            Object.assign(e.target.style, buttonStyle);
          }}
          onClick={() => navigate('/videos')}
        >
          🎯 Practice Speaking
        </button>

        <button
          style={{...buttonStyle, backgroundColor: '#2196F3', boxShadow: '0 8px 20px rgba(33, 150, 243, 0.3)'}}
          onMouseEnter={(e) => {
            Object.assign(e.target.style, {
              ...hoverStyle,
              backgroundColor: '#1976D2',
              boxShadow: '0 12px 30px rgba(33, 150, 243, 0.4)'
            });
          }}
          onMouseLeave={(e) => {
            Object.assign(e.target.style, {...buttonStyle, backgroundColor: '#2196F3', boxShadow: '0 8px 20px rgba(33, 150, 243, 0.3)'});
          }}
          onClick={() => navigate('/learning-library')}
        >
          📚 Learning Library
        </button>

        <button
          style={{...buttonStyle, backgroundColor: '#FF9800', boxShadow: '0 8px 20px rgba(255, 152, 0, 0.3)'}}
          onMouseEnter={(e) => {
            Object.assign(e.target.style, {
              ...hoverStyle,
              backgroundColor: '#F57C00',
              boxShadow: '0 12px 30px rgba(255, 152, 0, 0.4)'
            });
          }}
          onMouseLeave={(e) => {
            Object.assign(e.target.style, {...buttonStyle, backgroundColor: '#FF9800', boxShadow: '0 8px 20px rgba(255, 152, 0, 0.3)'});
          }}
          onClick={() => navigate('/chat')}
        >
          💬 AI Chat
        </button>
      </div>

      {/* Back Button */}
      <div style={{
        marginTop: '40px'
      }}>
        <button
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: '500',
            color: '#4A5568',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            border: '2px solid rgba(76, 175, 80, 0.3)',
            borderRadius: '20px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            fontFamily: 'Poppins, Nunito, Circular, -apple-system, BlinkMacSystemFont, sans-serif',
            backdropFilter: 'blur(10px)'
          }}
          onMouseEnter={(e) => {
            e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
            e.target.style.borderColor = '#4CAF50';
            e.target.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
            e.target.style.borderColor = 'rgba(76, 175, 80, 0.3)';
            e.target.style.transform = 'translateY(0px)';
          }}
          onClick={() => navigate('/')}
        >
          ← Back to Home
        </button>
      </div>
    </div>
  );
};

export default LearnersBasePage;
