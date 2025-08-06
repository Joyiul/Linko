import React from 'react';

const Logo = ({ size = 'medium', showText = false, className = '' }) => {
  const sizes = {
    small: { width: 32, height: 32 },
    medium: { width: 40, height: 40 },
    large: { width: 48, height: 48 },
    xlarge: { width: 56, height: 56 }
  };

  const currentSize = sizes[size] || sizes.medium;

  return (
    <div 
      className={`logo-container ${className}`}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      {/* Just the cute earth icon - matching your logo style */}
      <div
        style={{
          width: currentSize.width,
          height: currentSize.height,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #A8D8A8 0%, #87CEEB 100%)',
          border: '3px solid #666666',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          boxShadow: '2px 2px 6px rgba(0,0,0,0.15)'
        }}
      >
        {/* Simple cute face */}
        <div style={{
          position: 'relative',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {/* Eyes */}
          <div style={{
            position: 'absolute',
            top: '30%',
            left: '35%',
            width: '3px',
            height: '3px',
            borderRadius: '50%',
            backgroundColor: '#333333'
          }} />
          <div style={{
            position: 'absolute',
            top: '30%',
            right: '35%',
            width: '3px',
            height: '3px',
            borderRadius: '50%',
            backgroundColor: '#333333'
          }} />
          {/* Smile */}
          <div style={{
            position: 'absolute',
            bottom: '35%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '8px',
            height: '4px',
            borderBottom: '2px solid #333333',
            borderRadius: '0 0 8px 8px'
          }} />
        </div>
      </div>
    </div>
  );
};

export default Logo;
