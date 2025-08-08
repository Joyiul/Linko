import React from 'react';

const SurpriseEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#B3E5FC', // Light blue like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Surprised eyebrows */}
      <div style={{
        position: 'absolute',
        top: '18%',
        left: '25%',
        width: '15%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50px',
        transform: 'rotate(-15deg)'
      }} />
      <div style={{
        position: 'absolute',
        top: '18%',
        right: '25%',
        width: '15%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50px',
        transform: 'rotate(15deg)'
      }} />
      
      {/* Wide surprised eyes */}
      <div style={{
        position: 'absolute',
        top: '32%',
        left: '28%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '32%',
        right: '28%',
        width: '8%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Nose dot */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '2%',
        height: '2%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Surprised mouth - oval O */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '45%',
        right: '45%',
        height: '15%',
        backgroundColor: 'transparent',
        borderRadius: '50%',
        border: '3px solid #000'
      }} />
    </div>
  );
};

export default SurpriseEmoji;
