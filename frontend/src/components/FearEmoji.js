import React from 'react';

const FearEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#B0BEC5', // Gray like your image
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
        left: '28%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '30%',
        right: '28%',
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
      
      {/* Fearful mouth - small O */}
      <div style={{
        position: 'absolute',
        bottom: '30%',
        left: '47%',
        right: '47%',
        height: '12%',
        backgroundColor: 'transparent',
        borderRadius: '50%',
        border: '3px solid #000'
      }} />
    </div>
  );
};

export default FearEmoji;
