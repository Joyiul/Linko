import React, { useEffect, useState } from 'react';
import EmojiToneBar from '../components/EmojiToneBar';
import HighlightedText from '../components/HighlightedText';
import './AnalysisPage.css';

export default function AnalysisPage() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("analysisResults");
      if (stored) {
        const parsedResults = JSON.parse(stored);
        console.log("Loaded analysis results from localStorage:", parsedResults);
        setResults(parsedResults);
      } else {
        console.log("No analysis results found in localStorage");
      }
    } catch (error) {
      console.error("Error loading analysis results from localStorage:", error);
      // Clear corrupted data
      localStorage.removeItem("analysisResults");
    }
  }, []);

  const getEmotionEmoji = (emotion) => {
    const emojiMap = {
      'angry': 'ANGRY',
      'happy': 'HAPPY', 
      'sad': 'SAD',
      'fear': 'FEAR',
      'disgust': 'DISGUST',
      'surprise': 'SURPRISE',
      'neutral': 'NEUTRAL',
      'ps': 'THINKING'
    };
    return emojiMap[emotion] || 'NEUTRAL';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#28a745'; // Green
    if (confidence >= 0.6) return '#ffc107'; // Yellow  
    if (confidence >= 0.4) return '#fd7e14'; // Orange
    return '#dc3545'; // Red
  };

  if (!results) return (
    <div style={{ padding: 20, textAlign: 'center' }}>
      <h2>No Analysis Results</h2>
      <p>Please upload an audio file or enter text on the <a href="/listen">Listening Page</a> first.</p>
    </div>
  );

  const analysis = results.analysis || {};
  const emotionAnalysis = analysis.emotion_analysis || {};

  return (
    <div style={{ padding: 20 }}>
      <h2>Analysis Results</h2>
      
      {results.filename && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#e8f4fd', borderRadius: '5px' }}>
          <strong>📁 File:</strong> {results.filename}
        </div>
      )}

      {/* Enhanced Emotion Analysis Section */}
      <div style={{ marginBottom: '30px' }}>
        <h3>🎭 Emotion & Tone Analysis</h3>
        
        {/* Primary Tone */}
        <div style={{ marginBottom: '20px' }}>
          <h4>Primary Tone</h4>
          <EmojiToneBar tone={analysis.tone || results.tone || "😐 Neutral"} />
        </div>

        {/* Detailed Emotion Analysis */}
        {emotionAnalysis.detected_emotion && (
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '10px',
            border: '1px solid #dee2e6',
            marginBottom: '20px'
          }}>
            <h4 style={{ marginBottom: '15px' }}>🔍 Detailed Emotion Detection</h4>
            
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <span style={{ fontSize: '2em', marginRight: '15px' }}>
                {getEmotionEmoji(emotionAnalysis.detected_emotion)}
              </span>
              <div>
                <div style={{ fontSize: '1.2em', fontWeight: 'bold', textTransform: 'capitalize' }}>
                  {emotionAnalysis.detected_emotion}
                </div>
                <div style={{ 
                  fontSize: '0.9em', 
                  color: getConfidenceColor(emotionAnalysis.confidence || 0)
                }}>
                  Confidence: {((emotionAnalysis.confidence || 0) * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Emotion Scores Breakdown */}
            {emotionAnalysis.emotion_scores && (
              <div>
                <h5>Emotion Indicators Found:</h5>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '10px' }}>
                  {Object.entries(emotionAnalysis.emotion_scores).map(([emotion, score]) => (
                    <div key={emotion} style={{ 
                      textAlign: 'center',
                      padding: '8px',
                      backgroundColor: score > 0 ? '#e7f5e7' : '#f8f9fa',
                      borderRadius: '5px',
                      border: score > 0 ? '2px solid #28a745' : '1px solid #dee2e6'
                    }}>
                      <div style={{ fontSize: '1.5em' }}>{getEmotionEmoji(emotion)}</div>
                      <div style={{ fontSize: '0.8em', textTransform: 'capitalize' }}>{emotion}</div>
                      <div style={{ fontWeight: 'bold', color: score > 0 ? '#28a745' : '#6c757d' }}>
                        {score}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Analysis Confidence */}
        {analysis.analysis_confidence && (
          <div style={{ 
            padding: '10px', 
            backgroundColor: analysis.analysis_confidence === 'high' ? '#d4edda' : '#fff3cd',
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            <strong>Analysis Quality:</strong> {analysis.analysis_confidence} 
            {analysis.transcript_length && ` (${analysis.transcript_length} words)`}
          </div>
        )}
      </div>

      <div style={{ marginBottom: '30px' }}>
        <h3>Transcript</h3>
        {results.transcript ? (
          <div style={{ 
            padding: '15px', 
            backgroundColor: '#f8f9fa', 
            borderRadius: '5px',
            border: '1px solid #dee2e6',
            fontStyle: 'italic'
          }}>
            <HighlightedText text={results.transcript} />
          </div>
        ) : (
          <p style={{ color: '#666' }}>No transcript available</p>
        )}
      </div>

      <div>
        <h3>Slang Detection</h3>
        {Object.keys(analysis.slang || results.slang || {}).length > 0 ? (
          <ul style={{ 
            listStyle: 'none', 
            padding: 0,
            backgroundColor: '#fff3cd',
            borderRadius: '5px',
            padding: '15px'
          }}>
            {Object.entries(analysis.slang || results.slang || {}).map(([word, meaning]) => (
              <li key={word} style={{ 
                marginBottom: '10px',
                padding: '8px',
                backgroundColor: 'white',
                borderRadius: '3px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
              }}>
                <strong style={{ color: '#d63384' }}>"{word}"</strong> → {meaning}
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ 
            color: '#666', 
            fontStyle: 'italic',
            padding: '15px',
            backgroundColor: '#f8f9fa',
            borderRadius: '5px'
          }}>
            No slang terms detected in this text
          </p>
        )}
      </div>

      <div style={{ marginTop: '40px', textAlign: 'center' }}>
        <button 
          onClick={() => window.location.href = '/listen'} 
          style={{
            padding: '12px 24px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Analyze Another File
        </button>
      </div>
    </div>
  );
}
