import React, { useState } from 'react';
import axios from 'axios';

const FormalityAnalysis = ({ text, initialData = null, showTitle = true }) => {
  const [formalityData, setFormalityData] = useState(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [error, setError] = useState('');

  const analyzeFormalityLevel = async () => {
    if (!text || text.trim().length === 0) {
      setError('No text available for formality analysis');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post("http://localhost:5002/analyze-formality", {
        text: text.trim()
      }, {
        timeout: 10000,
      });

      if (response.data.success) {
        setFormalityData(response.data);
        setIsExpanded(true);
      } else {
        setError('Formality analysis failed');
      }
    } catch (error) {
      console.error('Formality analysis error:', error);
      setError('Failed to analyze formality. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getFormalityColor = (level) => {
    const colors = {
      'formal': '#6f42c1',      // Purple - Academic/Formal
      'professional': '#0056b3', // Blue - Business/Professional  
      'neutral': '#6c757d',     // Gray - Neutral
      'informal': '#fd7e14',    // Orange - Conversational
      'casual': '#e83e8c',      // Pink - Very casual/Slang
    };
    return colors[level] || '#6c757d';
  };

  const getFormalityIcon = (level) => {
    const icons = {
      'formal': '🎓',        // Academic cap
      'professional': '💼',  // Briefcase
      'neutral': '📝',       // Document
      'informal': '💬',      // Speech bubble
      'casual': '😎',        // Cool emoji
    };
    return icons[level] || '📝';
  };

  const getFormalityDescription = (level) => {
    const descriptions = {
      'formal': 'Academic/Formal language with complex structures',
      'professional': 'Business-appropriate professional communication',
      'neutral': 'Balanced tone without strong formality indicators',
      'informal': 'Conversational style with casual expressions',
      'casual': 'Very relaxed with slang and informal expressions'
    };
    return descriptions[level] || 'Formality level analysis';
  };

  const renderIndicators = (indicators) => {
    if (!indicators || Object.keys(indicators).length === 0) return null;

    return (
      <div style={{ marginTop: 15 }}>
        <h4 style={{ fontSize: 14, marginBottom: 10, color: '#495057' }}>
          Language Indicators Found:
        </h4>
        {Object.entries(indicators).map(([category, items]) => {
          if (!items || items.length === 0) return null;
          
          return (
            <div key={category} style={{ marginBottom: 8 }}>
              <strong style={{ 
                fontSize: 12, 
                color: '#6c757d',
                textTransform: 'capitalize'
              }}>
                {category.replace('_', ' ')}: 
              </strong>
              <span style={{ fontSize: 12, marginLeft: 5 }}>
                {items.slice(0, 3).join(', ')}
                {items.length > 3 && ` (and ${items.length - 3} more)`}
              </span>
            </div>
          );
        })}
      </div>
    );
  };

  const renderFormalityDistribution = (distribution) => {
    if (!distribution) return null;

    return (
      <div style={{ marginTop: 15 }}>
        <h4 style={{ fontSize: 14, marginBottom: 10, color: '#495057' }}>
          Formality Breakdown:
        </h4>
        {Object.entries(distribution).map(([level, percentage]) => (
          <div key={level} style={{ 
            display: 'flex', 
            alignItems: 'center', 
            marginBottom: 5,
            fontSize: 12
          }}>
            <span style={{ 
              minWidth: 80,
              textTransform: 'capitalize',
              color: '#6c757d'
            }}>
              {level}:
            </span>
            <div style={{
              flex: 1,
              height: 6,
              backgroundColor: '#e9ecef',
              borderRadius: 3,
              marginLeft: 8,
              marginRight: 8,
              overflow: 'hidden'
            }}>
              <div style={{
                height: '100%',
                width: `${percentage}%`,
                backgroundColor: getFormalityColor(level),
                borderRadius: 3,
                transition: 'width 0.3s ease'
              }} />
            </div>
            <span style={{ minWidth: 35, color: '#6c757d' }}>
              {percentage}%
            </span>
          </div>
        ))}
      </div>
    );
  };

  // If we have initial data, show it directly
  if (formalityData && !isLoading) {
    const { formality_analysis, explicit_formality_breakdown } = formalityData;
    const level = formality_analysis?.formality_level || explicit_formality_breakdown?.level?.toLowerCase();
    const confidence = formality_analysis?.confidence || explicit_formality_breakdown?.confidence_percentage / 100;

    return (
      <div style={{
        background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
        border: `2px solid ${getFormalityColor(level)}`,
        borderRadius: 12,
        padding: 16,
        marginTop: 15,
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        {showTitle && (
          <h3 style={{ 
            fontSize: 16, 
            marginBottom: 12, 
            color: '#495057',
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            📊 Formality Analysis
          </h3>
        )}

        <div style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: 12,
          gap: 12
        }}>
          <div style={{
            fontSize: 24,
            padding: '8px 12px',
            background: 'rgba(255,255,255,0.8)',
            borderRadius: 8,
            border: `1px solid ${getFormalityColor(level)}`
          }}>
            {getFormalityIcon(level)}
          </div>
          
          <div style={{ flex: 1 }}>
            <div style={{
              fontSize: 16,
              fontWeight: 'bold',
              color: getFormalityColor(level),
              textTransform: 'capitalize',
              marginBottom: 4
            }}>
              {level} Style
            </div>
            <div style={{
              fontSize: 12,
              color: '#6c757d',
              marginBottom: 4
            }}>
              {getFormalityDescription(level)}
            </div>
            <div style={{
              fontSize: 11,
              color: '#6c757d'
            }}>
              Confidence: {Math.round(confidence * 100)}%
            </div>
          </div>
        </div>

        {formality_analysis?.summary && (
          <div style={{
            background: 'rgba(255,255,255,0.6)',
            padding: 12,
            borderRadius: 8,
            fontSize: 13,
            color: '#495057',
            lineHeight: 1.4,
            marginBottom: 12
          }}>
            {formality_analysis.summary}
          </div>
        )}

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            background: 'none',
            border: 'none',
            color: getFormalityColor(level),
            fontSize: 12,
            cursor: 'pointer',
            padding: '4px 0',
            fontWeight: 'bold'
          }}
        >
          {isExpanded ? '▼ Hide Details' : '▶ Show Details'}
        </button>

        {isExpanded && (
          <div style={{ marginTop: 12 }}>
            {formality_analysis?.details?.formality_distribution && 
              renderFormalityDistribution(formality_analysis.details.formality_distribution)}
            
            {formality_analysis?.indicators && 
              renderIndicators(formality_analysis.indicators)}
          </div>
        )}
      </div>
    );
  }

  // Show the analyze button if no data
  return (
    <div style={{
      background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
      border: '2px solid #dee2e6',
      borderRadius: 12,
      padding: 16,
      marginTop: 15,
      textAlign: 'center'
    }}>
      {showTitle && (
        <h3 style={{ 
          fontSize: 16, 
          marginBottom: 12, 
          color: '#495057',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8
        }}>
          📊 Formality Analysis
        </h3>
      )}

      {error && (
        <div style={{
          color: '#dc3545',
          fontSize: 12,
          marginBottom: 12,
          padding: 8,
          background: 'rgba(220, 53, 69, 0.1)',
          borderRadius: 6
        }}>
          {error}
        </div>
      )}

      <p style={{ 
        fontSize: 13, 
        color: '#6c757d', 
        marginBottom: 15,
        lineHeight: 1.4
      }}>
        Analyze the formality level of this text to understand whether it uses formal, professional, informal, or casual language patterns.
      </p>

      <button
        onClick={analyzeFormalityLevel}
        disabled={isLoading || !text}
        style={{
          background: isLoading ? '#6c757d' : 'linear-gradient(135deg, #007bff 0%, #0056b3 100%)',
          color: 'white',
          border: 'none',
          borderRadius: 8,
          padding: '10px 20px',
          fontSize: 14,
          fontWeight: 'bold',
          cursor: isLoading || !text ? 'not-allowed' : 'pointer',
          opacity: isLoading || !text ? 0.6 : 1,
          transition: 'all 0.3s ease'
        }}
      >
        {isLoading ? 'Analyzing Formality...' : 'Analyze Formality Level'}
      </button>
    </div>
  );
};

export default FormalityAnalysis;
