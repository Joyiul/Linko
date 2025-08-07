import React from 'react';

const EmotionImage = ({ emotion, size = 80 }) => {
  if (!emotion) return null;
  
  const getEmotionImagePath = (emotion) => {
    const emotionLower = emotion.toLowerCase();
    
    // Map emotions to your actual image files
    const emotionFileMap = {
      'happy': '/emotions/happy.png',
      'excited': '/emotions/excited.png', 
      'angry': '/emotions/angry.png',
      'disappointed': '/emotions/disappoint.png',
      'disgust': '/emotions/disgust.png',
      'interest': '/emotions/interest.png',
      'interested': '/emotions/interest.png',
      'curious': '/emotions/interest.png',
      'intrigued': '/emotions/interest.png',
      'neutral': '/emotions/netural.png',
      'calm': '/emotions/netural.png',
      'thinking': '/emotions/netural.png',
      'contemplative': '/emotions/netural.png',
      'sad': '/emotions/sad.png',
      'surprise': '/emotions/shock.png',
      'surprised': '/emotions/shock.png',
      'shocked': '/emotions/shock.png',
      'fear': '/emotions/sad.png', // Use sad for fear if no fear image
      'scared': '/emotions/sad.png',
      'afraid': '/emotions/sad.png'
    };
    
    return emotionFileMap[emotionLower] || '/emotions/netural.png';
  };

  const imagePath = getEmotionImagePath(emotion);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      width: size,
      height: size,
      margin: '10px'
    }}>
      <img 
        src={imagePath}
        alt={`${emotion} emotion`}
        style={{
          width: size,
          height: size,
          objectFit: 'contain',
          borderRadius: '50%'
        }}
        onError={(e) => {
          // Fallback if image doesn't load
          e.target.style.display = 'none';
          e.target.nextSibling.style.display = 'flex';
        }}
      />
      <div style={{
        display: 'none',
        width: size,
        height: size,
        backgroundColor: '#E0E0E0',
        borderRadius: '50%',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: size * 0.5,
        color: '#666'
      }}>
        😐
      </div>
    </div>
  );
};

export default EmotionImage;
