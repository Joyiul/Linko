import React, { useState } from 'react';

const Logo = ({ size = 'medium', showText = false, className = '', animated = false }) => {
  const [hovered, setHovered] = useState(false);
  
  const sizes = {
    small: { width: 50, height: 50 },
    medium: { width: 80, height: 80 },
    large: { width: 100, height: 100 },
    xlarge: { width: 150, height: 150 },
    hero: { width: 250, height: 250 } // Increased from 200 to 250
  };

  const currentSize = sizes[size] || sizes.medium;

  return (
    <div 
      className={`logo-container ${className}`}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative'
      }}
    >
      {/* AI Assistant as semi-circle with tech/AI aesthetic */}
      {/* Your Uploaded Earth Image - Clean & Simple */}
      <div style={{
        width: `${currentSize.width}px`,
        height: `${currentSize.height}px`,
        position: 'relative',
        cursor: hovered ? 'pointer' : 'default',
        transform: hovered ? 'scale(1.05) translateY(-3px)' : 'scale(1)',
        transition: 'all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}>
        
        <img 
          src="/earth-logo.png" 
          alt="Linko Earth AI Assistant"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            display: 'block'
          }}
        />
      </div>

      {/* Text label if requested */}
      {showText && (
        <div style={{
          marginTop: '10px',
          fontSize: `${currentSize.width / 8}px`,
          fontWeight: 'bold',
          color: '#4A5568',
          textAlign: 'center'
        }}>
          Linko AI
        </div>
      )}

      {/* No animations needed - clean and simple */}
    </div>
  );
};

export default Logo;
