import React from 'react';

const SadnessEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#B19CD9', // Purple like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Sad eyebrows */}
      <div style={{
        position: 'absolute',
        top: '20%',
        left: '25%',
        width: '15%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '2px',
        transform: 'rotate(-20deg)'
      }} />
      <div style={{
        position: 'absolute',
        top: '20%',
        right: '25%',
        width: '15%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '2px',
        transform: 'rotate(20deg)'
      }} />
      
      {/* Eyes with tears */}
      <div style={{
        position: 'absolute',
        top: '35%',
        left: '32%',
        width: '6%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '35%',
        right: '32%',
        width: '6%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Sad mouth */}
      <div style={{
        position: 'absolute',
        bottom: '30%',
        left: '40%',
        right: '40%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50px 50px 0 0',
        border: '2px solid #000',
        borderBottom: 'none'
      }} />
    </div>
  );
};

export default SadnessEmoji;
