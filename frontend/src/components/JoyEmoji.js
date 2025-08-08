import React from 'react';

const JoyEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#FFD700', // Yellow like your image
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
      
      {/* Nose dot */}
      <div style={{
        position: 'absolute',
        top: '45%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '4%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Happy smile */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '25%',
        right: '25%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '0 0 50px 50px',
        border: '3px solid #000',
        borderTop: 'none'
      }} />
    </div>
  );
};

export default JoyEmoji;
