import React from 'react';

const AngerEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#FF6B6B', // Red like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Angry eyebrows */}
      <div style={{
        position: 'absolute',
        top: '20%',
        left: '25%',
        width: '15%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '2px',
        transform: 'rotate(25deg)'
      }} />
      <div style={{
        position: 'absolute',
        top: '20%',
        right: '25%',
        width: '15%',
        height: '8%',
        backgroundColor: '#000',
        borderRadius: '2px',
        transform: 'rotate(-25deg)'
      }} />
      
      {/* Eyes */}
      <div style={{
        position: 'absolute',
        top: '35%',
        left: '30%',
        width: '6%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '35%',
        right: '30%',
        width: '6%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Nose */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '4%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Angry frown */}
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

export default AngerEmoji;
