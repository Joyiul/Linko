import React from 'react';

const NeutralEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#4CAF50', // Green color like your image
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
        top: '25%',
        left: '25%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '25%',
        right: '25%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Nose dots */}
      <div style={{
        position: 'absolute',
        top: '40%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '4%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Mouth - neutral straight line */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '25%',
        right: '25%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '3px'
      }} />
    </div>
  );
};

export default NeutralEmoji;
