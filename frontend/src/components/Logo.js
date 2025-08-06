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
      {/* Earth icon as semi-circle with flat bottom */}
      <div
        style={{
          width: currentSize.width,
          height: currentSize.height / 2,
          borderRadius: `${currentSize.width}px ${currentSize.width}px 0 0`,
          background: '#87CEEB', // Sky blue base
          border: '3px solid #666666',
          borderBottom: '3px solid #666666',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          boxShadow: '2px 2px 6px rgba(0,0,0,0.15)',
          overflow: 'hidden'
        }}
      >
        {/* Green landmasses - adjusted for semi-circle */}
        {/* Left landmass */}
        <div style={{
          position: 'absolute',
          left: '15%',
          top: '10%',
          width: '35%',
          height: '60%',
          background: '#A8D8A8',
          borderRadius: '50% 40% 60% 30%',
          transform: 'rotate(-15deg)'
        }} />
        
        {/* Right landmass */}
        <div style={{
          position: 'absolute',
          right: '10%',
          top: '20%',
          width: '25%',
          height: '45%',
          background: '#A8D8A8',
          borderRadius: '40% 50% 30% 60%',
          transform: 'rotate(20deg)'
        }} />
        
        {/* Bottom landmass */}
        <div style={{
          position: 'absolute',
          bottom: '5%',
          left: '30%',
          width: '40%',
          height: '35%',
          background: '#A8D8A8',
          borderRadius: '60% 30% 50% 40%',
          transform: 'rotate(-10deg)'
        }} />
        
        {/* Cute face overlay - adjusted for semi-circle */}
        <div style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 10
        }}>
          {/* Eyes */}
          <div style={{
            position: 'absolute',
            top: '25%',
            left: '32%',
            width: '4px',
            height: '4px',
            borderRadius: '50%',
            backgroundColor: '#333333'
          }} />
          <div style={{
            position: 'absolute',
            top: '25%',
            right: '32%',
            width: '4px',
            height: '4px',
            borderRadius: '50%',
            backgroundColor: '#333333'
          }} />
          
          {/* Small heart-shaped smile */}
          <div style={{
            position: 'absolute',
            bottom: '25%',
            left: '50%',
            transform: 'translateX(-50%)',
            fontSize: '8px',
            color: '#333333'
          }}>
            ♡
          </div>
        </div>
      </div>
    </div>
  );
};

export default Logo;
