import React, { useState } from 'react';
import axios from 'axios';

const TextSimplificationBox = ({ originalText, initialSimplification = null }) => {
  const [simplification, setSimplification] = useState(initialSimplification);
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const simplifyText = async () => {
    if (!originalText || !originalText.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5002/simplify-text', {
        text: originalText
      });
      
      if (response.data.status === 'success') {
        setSimplification(response.data.simplification);
      }
    } catch (error) {
      console.error('Error simplifying text:', error);
      setSimplification({
        success: false,
        error: 'Failed to simplify text. Please try again.',
        original_text: originalText,
        simplified_text: originalText,
        method: 'error'
      });
    }
    setIsLoading(false);
  };

  const getDifficultyColor = (level) => {
    const colors = {
      'easy': '#28a745',
      'medium': '#ffc107', 
      'hard': '#dc3545'
    };
    return colors[level] || '#6c757d';
  };

  if (!originalText || originalText.trim().length < 10) {
    return null; // Don't show for very short texts
  }

  return (
    <div style={{
      backgroundColor: '#f8f9fa',
      border: '1px solid #dee2e6',
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '20px'
    }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '15px'
      }}>
        <h4 style={{ 
          margin: 0, 
          color: '#495057',
          fontSize: '1.1rem',
          fontWeight: '600'
        }}>
          � Plain English Version (Idioms & Slang Explained)
        </h4>
        
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            background: 'none',
            border: 'none',
            color: '#007bff',
            cursor: 'pointer',
            fontSize: '14px',
            textDecoration: 'underline'
          }}
        >
          {isExpanded ? 'Hide Details' : 'Show Details'}
        </button>
      </div>

      {/* Single Simplify Button */}
      {!simplification && (
        <div style={{ marginBottom: '15px', textAlign: 'center' }}>
          <button
            onClick={simplifyText}
            disabled={isLoading}
            style={{
              padding: '8px 16px',
              border: '1px solid #007bff',
              backgroundColor: '#007bff',
              color: 'white',
              borderRadius: '6px',
              fontSize: '14px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            {isLoading ? 'Simplifying...' : 'Simplify Text'}
          </button>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div style={{ 
          textAlign: 'center', 
          padding: '20px',
          color: '#6c757d'
        }}>
          <div>🔍 Converting idioms and slang to plain English...</div>
          <div style={{ fontSize: '12px', marginTop: '5px' }}>
            This may take a few seconds
          </div>
        </div>
      )}

      {/* Simplified Text Display */}
      {!isLoading && simplification && (
        <div>
          {/* Main Simplified Text */}
          <div style={{
            backgroundColor: 'white',
            padding: '15px',
            borderRadius: '6px',
            border: '1px solid #dee2e6',
            marginBottom: '15px',
            lineHeight: '1.6'
          }}>
            <div style={{ 
              fontSize: '14px', 
              color: '#6c757d', 
              marginBottom: '8px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <span>Simplified Text:</span>
            </div>
            <div style={{ 
              fontSize: '16px',
              color: '#333',
              fontFamily: 'system-ui, -apple-system, sans-serif'
            }}>
              {simplification.simplified_text}
            </div>
          </div>

          {/* Detailed Analysis (Expandable) */}
          {isExpanded && (
            <div style={{ 
              backgroundColor: '#ffffff',
              padding: '15px',
              borderRadius: '6px',
              border: '1px solid #e9ecef'
            }}>
              {/* Key Explanations */}
              {simplification.key_explanations && simplification.key_explanations.length > 0 && (
                <div style={{ marginBottom: '15px' }}>
                  <h6 style={{ color: '#495057', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
                    💡 Key Explanations:
                  </h6>
                  <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', color: '#6c757d' }}>
                    {simplification.key_explanations.map((explanation, index) => (
                      <li key={index} style={{ marginBottom: '4px' }}>
                        {explanation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Cultural Notes */}
              {simplification.cultural_notes && simplification.cultural_notes.length > 0 && (
                <div style={{ marginBottom: '15px' }}>
                  <h6 style={{ color: '#495057', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
                    🌍 Cultural Context:
                  </h6>
                  <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', color: '#6c757d' }}>
                    {simplification.cultural_notes.map((note, index) => (
                      <li key={index} style={{ marginBottom: '4px' }}>
                        {note}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Word Substitutions */}
              {simplification.word_substitutions && Object.keys(simplification.word_substitutions).length > 0 && (
                <div style={{ marginBottom: '15px' }}>
                  <h6 style={{ color: '#495057', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
                    📝 Simpler Words Used:
                  </h6>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {Object.entries(simplification.word_substitutions).map(([difficult, simple], index) => (
                      <div
                        key={index}
                        style={{
                          fontSize: '12px',
                          padding: '4px 8px',
                          backgroundColor: '#e7f3ff',
                          border: '1px solid #b8daff',
                          borderRadius: '4px',
                          color: '#004085'
                        }}
                      >
                        <span style={{ textDecoration: 'line-through', opacity: 0.7 }}>
                          {difficult}
                        </span>
                        <span style={{ margin: '0 4px' }}>→</span>
                        <span style={{ fontWeight: 'bold' }}>
                          {simple}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Method Info */}
              <div style={{ 
                fontSize: '12px', 
                color: '#6c757d',
                textAlign: 'right',
                fontStyle: 'italic'
              }}>
                {simplification.method === 'llm_powered' ? '🤖 AI-powered simplification' : '📋 Rule-based simplification'}
              </div>
            </div>
          )}

          {/* Auto-simplify on first load */}
          {!simplification && !isLoading && (
            <div style={{ textAlign: 'center', padding: '15px' }}>
              <button
                onClick={() => simplifyText('intermediate')}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#007bff',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                📚 Make This Text Easier to Understand
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TextSimplificationBox;
