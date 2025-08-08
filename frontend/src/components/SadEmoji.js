import React from 'react';

const SadEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#90A4AE', // Blue-gray like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Eyes */}
      <div style={{
        position: 'absolute',
        top: '30%',
        left: '30%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '30%',
        right: '30%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Nose */}
      <div style={{
        position: 'absolute',
        top: '48%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '4%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Tear */}
      <div style={{
        position: 'absolute',
        top: '42%',
        right: '28%',
        width: '3%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%'
      }} />
      
      {/* Sad mouth */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '35%',
        right: '35%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50px 50px 0 0',
        border: '3px solid #000',
        borderBottom: 'none'
      }} />
    </div>
  );
};

export default SadEmoji;
