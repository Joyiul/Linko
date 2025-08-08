import React from 'react';

const DisgustEmoji = ({ size = 50, style = {} }) => {
  return (
    <div 
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#D2B48C', // Brown like your image
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        ...style
      }}
    >
      {/* Disgusted eyebrows */}
      <div style={{
        position: 'absolute',
        top: '20%',
        left: '25%',
        width: '15%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '2px'
      }} />
      <div style={{
        position: 'absolute',
        top: '20%',
        right: '25%',
        width: '15%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '2px'
      }} />
      
      {/* Eyes - one squinting */}
      <div style={{
        position: 'absolute',
        top: '35%',
        left: '30%',
        width: '6%',
        height: '3%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      <div style={{
        position: 'absolute',
        top: '35%',
        right: '30%',
        width: '4%',
        height: '6%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Nose with disgust */}
      <div style={{
        position: 'absolute',
        top: '50%',
        right: '45%',
        width: '6%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '50%'
      }} />
      
      {/* Disgusted mouth */}
      <div style={{
        position: 'absolute',
        bottom: '25%',
        left: '35%',
        right: '45%',
        height: '4%',
        backgroundColor: '#000',
        borderRadius: '2px'
      }} />
    </div>
  );
};

export default DisgustEmoji;
