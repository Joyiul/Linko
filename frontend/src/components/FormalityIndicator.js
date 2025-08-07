import React from 'react';

const FormalityIndicator = ({ formalityAnalysis, size = 'medium' }) => {
  if (!formalityAnalysis) return null;

  const { formality_level, confidence, details, indicators, summary } = formalityAnalysis;

  // Size configurations
  const sizeConfig = {
    small: { container: '200px', font: '12px', bar: '8px' },
    medium: { container: '300px', font: '14px', bar: '12px' },
    large: { container: '400px', font: '16px', bar: '16px' }
  };

  const config = sizeConfig[size] || sizeConfig.medium;

  // Formality level colors and labels
  const formalityStyles = {
    formal: {
      color: '#2E3192',
      bgColor: '#E8EAF6',
      icon: '🎓',
      label: 'FORMAL',
      description: 'Academic & Professional'
    },
    professional: {
      color: '#1976D2',
      bgColor: '#E3F2FD',
      icon: '💼',
      label: 'PROFESSIONAL',
      description: 'Business & Corporate'
    },
    informal: {
      color: '#388E3C',
      bgColor: '#E8F5E8',
      icon: '💬',
      label: 'INFORMAL',
      description: 'Conversational & Friendly'
    },
    casual: {
      color: '#F57C00',
      bgColor: '#FFF3E0',
      icon: '😎',
      label: 'CASUAL',
      description: 'Relaxed & Slang'
    },
    neutral: {
      color: '#616161',
      bgColor: '#F5F5F5',
      icon: '📝',
      label: 'NEUTRAL',
      description: 'Balanced Tone'
    }
  };

  const currentStyle = formalityStyles[formality_level] || formalityStyles.neutral;

  return (
    <div style={{
      width: config.container,
      padding: '16px',
      backgroundColor: currentStyle.bgColor,
      borderRadius: '12px',
      border: `2px solid ${currentStyle.color}`,
      fontFamily: 'Poppins, sans-serif',
      margin: '10px 0'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '12px'
      }}>
        <span style={{ fontSize: '24px', marginRight: '8px' }}>
          {currentStyle.icon}
        </span>
        <div>
          <div style={{
            fontSize: config.font,
            fontWeight: 'bold',
            color: currentStyle.color
          }}>
            {currentStyle.label}
          </div>
          <div style={{
            fontSize: '12px',
            color: '#666',
            fontStyle: 'italic'
          }}>
            {currentStyle.description}
          </div>
        </div>
        <div style={{
          marginLeft: 'auto',
          fontSize: config.font,
          fontWeight: 'bold',
          color: currentStyle.color
        }}>
          {Math.round(confidence * 100)}%
        </div>
      </div>

      {/* Distribution bars */}
      {details && details.formality_distribution && (
        <div style={{ marginBottom: '12px' }}>
          <div style={{
            fontSize: '12px',
            color: '#666',
            marginBottom: '6px',
            fontWeight: '500'
          }}>
            Formality Breakdown:
          </div>
          {Object.entries(details.formality_distribution).map(([type, percentage]) => {
            if (percentage <= 0) return null;
            const typeStyle = formalityStyles[type] || formalityStyles.neutral;
            return (
              <div key={type} style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: '4px'
              }}>
                <div style={{
                  width: '60px',
                  fontSize: '11px',
                  color: '#666',
                  textTransform: 'capitalize'
                }}>
                  {type}:
                </div>
                <div style={{
                  flex: 1,
                  height: config.bar,
                  backgroundColor: '#E0E0E0',
                  borderRadius: '6px',
                  overflow: 'hidden',
                  marginRight: '8px'
                }}>
                  <div style={{
                    width: `${percentage}%`,
                    height: '100%',
                    backgroundColor: typeStyle.color,
                    transition: 'width 0.5s ease'
                  }} />
                </div>
                <div style={{
                  fontSize: '11px',
                  color: '#666',
                  minWidth: '35px'
                }}>
                  {percentage}%
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Summary */}
      <div style={{
        fontSize: '12px',
        color: '#666',
        lineHeight: '1.4',
        marginBottom: '10px',
        padding: '8px',
        backgroundColor: 'rgba(255,255,255,0.7)',
        borderRadius: '6px'
      }}>
        {summary}
      </div>

      {/* Indicators (collapsible) */}
      {indicators && Object.keys(indicators).some(key => indicators[key].length > 0) && (
        <details style={{ marginTop: '8px' }}>
          <summary style={{
            fontSize: '12px',
            color: currentStyle.color,
            cursor: 'pointer',
            fontWeight: '500'
          }}>
            📋 View Detailed Indicators ({Object.values(indicators).flat().length} found)
          </summary>
          <div style={{ marginTop: '8px' }}>
            {Object.entries(indicators).map(([category, items]) => {
              if (!items || items.length === 0) return null;
              const categoryStyle = formalityStyles[category] || formalityStyles.neutral;
              return (
                <div key={category} style={{ marginBottom: '8px' }}>
                  <div style={{
                    fontSize: '11px',
                    fontWeight: 'bold',
                    color: categoryStyle.color,
                    textTransform: 'capitalize',
                    marginBottom: '4px'
                  }}>
                    {categoryStyle.icon} {category} ({items.length}):
                  </div>
                  <div style={{
                    paddingLeft: '16px',
                    fontSize: '10px',
                    color: '#666'
                  }}>
                    {items.slice(0, 3).map((item, index) => (
                      <div key={index} style={{ marginBottom: '2px' }}>
                        • {item}
                      </div>
                    ))}
                    {items.length > 3 && (
                      <div style={{ fontStyle: 'italic', color: '#999' }}>
                        ... and {items.length - 3} more
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </details>
      )}
    </div>
  );
};

export default FormalityIndicator;
