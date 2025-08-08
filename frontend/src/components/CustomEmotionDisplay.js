import React from 'react';
import JoyEmoji from './JoyEmoji';
import AngerEmoji from './AngerEmoji';
import SadnessEmoji from './SadnessEmoji';
import DisgustEmoji from './DisgustEmoji';
import HappinessEmoji from './HappinessEmoji';
import FearEmoji from './FearEmoji';
import SurpriseEmoji from './SurpriseEmoji';
import SadEmoji from './SadEmoji';
import NeutralEmoji from './NeutralEmoji';

const CustomEmotionDisplay = ({ emotion, size = 50, style = {} }) => {
  const emotionLower = emotion?.toLowerCase() || 'neutral';
  
  switch (emotionLower) {
    case 'joy':
    case 'happy':
    case 'happiness':
      return <JoyEmoji size={size} style={style} />;
    case 'anger':
    case 'angry':
      return <AngerEmoji size={size} style={style} />;
    case 'sadness':
      return <SadnessEmoji size={size} style={style} />;
    case 'disgust':
    case 'disgusted':
      return <DisgustEmoji size={size} style={style} />;
    case 'fear':
    case 'scared':
    case 'afraid':
      return <FearEmoji size={size} style={style} />;
    case 'surprise':
    case 'surprised':
      return <SurpriseEmoji size={size} style={style} />;
    case 'sad':
      return <SadEmoji size={size} style={style} />;
    case 'neutral':
    default:
      return <NeutralEmoji size={size} style={style} />;
  }
};

export default CustomEmotionDisplay;
