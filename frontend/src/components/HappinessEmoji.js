import React from 'react';

const HappinessEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#C8E6C9', // Light green like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Happy curved eyebrows/eyes */}
      <div style={{
        position: 'absolute',
        top: '25%',
        left: '25%',
        width: '15%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '0 0 50px 50px',
        border: '3px solid #000',
        borderTop: 'none'
      }} />
      <div style={{
        position: 'absolute',
        top: '25%',
        right: '25%',
        width: '15%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '0 0 50px 50px',
        border: '3px solid #000',
        borderTop: 'none'
      }} />
      
      {/* Big happy smile - open mouth */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '30%',
        right: '30%',
        height: '20%',
        backgroundColor: '#000',
        borderRadius: '50%',
        border: '4px solid #000'
      }} />
    </div>
  );
};

export default HappinessEmoji;
