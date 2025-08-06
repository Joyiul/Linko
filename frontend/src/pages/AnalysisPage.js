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
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '5px', border: '1px solid #dee2e6' }}>
          <strong>📁 File:</strong> {results.filename}
        </div>
      )}

      {/* Enhanced Emotion Analysis Section */}
      <div style={{ marginBottom: '30px' }}>
        <h3>Emotion & Tone Analysis</h3>
        
        {/* Primary Tone */}
        <div style={{ marginBottom: '20px' }}>
          <h4>Primary Tone</h4>
          <EmojiToneBar tone={analysis.tone || results.tone || "Neutral"} />
        </div>

        {/* Detailed Emotion Analysis */}
        {emotionAnalysis.detected_emotion && (
          <div style={{ 
            backgroundColor: '#FFFFFF', 
            padding: '20px', 
            borderRadius: '10px',
            border: '1px solid #dee2e6',
            marginBottom: '20px'
          }}>
            <h4 style={{ marginBottom: '15px' }}>Detailed Emotion Detection</h4>
            
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <div>
                <div style={{ fontSize: '1.2rem', fontWeight: '500', textTransform: 'capitalize', fontFamily: 'Poppins, Nunito, Circular, sans-serif', color: '#6c757d', letterSpacing: '0.2px' }}>
                  {emotionAnalysis.detected_emotion}
                </div>
                <div style={{ 
                  fontSize: '0.95rem', 
                  color: getConfidenceColor(emotionAnalysis.confidence || 0),
                  fontFamily: 'Poppins, Nunito, Circular, sans-serif',
                  fontStyle: 'italic',
                  fontWeight: '400',
                  letterSpacing: '0.1px'
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
                      <div style={{ fontSize: '0.85rem', textTransform: 'capitalize', fontFamily: 'Poppins, Nunito, Circular, sans-serif', color: '#6c757d', fontWeight: '400', letterSpacing: '0.1px' }}>{emotion}</div>
                      <div style={{ fontWeight: '500', color: score > 0 ? '#28a745' : '#6c757d', fontFamily: 'Poppins, Nunito, Circular, sans-serif', fontSize: '0.9rem' }}>
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
            backgroundColor: analysis.analysis_confidence === 'high' ? '#f8f9fa' : '#ffffff',
            borderRadius: '5px',
            marginBottom: '20px',
            border: '1px solid #dee2e6'
          }}>
            <strong>Analysis Quality:</strong> {analysis.analysis_confidence} 
            {analysis.transcript_length && ` (${analysis.transcript_length} words)`}
          </div>
        )}
      </div>

      {/* Video Analysis Section */}
      {analysis.video_analysis && (
        <div style={{ marginBottom: '30px' }}>
          <h3>Video Analysis Results</h3>
          <div style={{
            backgroundColor: '#FFFFFF',
            padding: '20px',
            borderRadius: '10px',
            border: '1px solid #dee2e6',
            marginBottom: '20px'
          }}>
            <h4 style={{ marginBottom: '15px', color: '#6c757d' }}>Facial Emotion Detection</h4>
            
            {/* Primary Emotion from Video */}
            <div style={{ marginBottom: '15px' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: '600', textTransform: 'capitalize', color: '#495057' }}>
                Primary Emotion: {analysis.video_analysis.dominant_emotion || 'Not detected'}
              </div>
              {analysis.video_analysis.confidence && (
                <div style={{
                  fontSize: '1rem',
                  color: getConfidenceColor(analysis.video_analysis.confidence),
                  fontWeight: '500',
                  marginTop: '5px'
                }}>
                  Confidence: {(analysis.video_analysis.confidence * 100).toFixed(1)}%
                </div>
              )}
            </div>

            {/* Video Statistics */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px', marginBottom: '20px' }}>
              <div style={{
                textAlign: 'center',
                padding: '15px',
                backgroundColor: '#f8f9fa',
                borderRadius: '8px',
                border: '1px solid #dee2e6'
              }}>
                <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#28a745' }}>
                  {analysis.video_analysis.frames_analyzed || 0}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#6c757d' }}>Frames Analyzed</div>
              </div>
              
              <div style={{
                textAlign: 'center',
                padding: '15px',
                backgroundColor: '#f8f9fa',
                borderRadius: '8px',
                border: '1px solid #dee2e6'
              }}>
                <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#17a2b8' }}>
                  {analysis.video_analysis.faces_detected || 0}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#6c757d' }}>Faces Detected</div>
              </div>

              {analysis.video_info && analysis.video_info.duration_seconds && (
                <div style={{
                  textAlign: 'center',
                  padding: '15px',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '8px',
                  border: '1px solid #dee2e6'
                }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#fd7e14' }}>
                    {analysis.video_info.duration_seconds.toFixed(1)}s
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#6c757d' }}>Duration</div>
                </div>
              )}
            </div>

            {/* Emotion Distribution */}
            {analysis.video_analysis.emotion_distribution && Object.keys(analysis.video_analysis.emotion_distribution).length > 1 && (
              <div style={{ marginTop: '20px' }}>
                <h5>Emotion Distribution Across Video</h5>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '10px' }}>
                  {Object.entries(analysis.video_analysis.emotion_distribution).map(([emotion, count]) => (
                    <div key={emotion} style={{
                      textAlign: 'center',
                      padding: '10px',
                      backgroundColor: count > 1 ? '#e7f5e7' : '#f8f9fa',
                      borderRadius: '5px',
                      border: count > 1 ? '2px solid #28a745' : '1px solid #dee2e6'
                    }}>
                      <div style={{ fontSize: '0.85rem', textTransform: 'capitalize', color: '#6c757d' }}>{emotion}</div>
                      <div style={{ fontWeight: '600', color: count > 1 ? '#28a745' : '#6c757d' }}>
                        {count} frame{count !== 1 ? 's' : ''}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Video Quality Feedback */}
            <div style={{
              marginTop: '20px',
              padding: '15px',
              backgroundColor: analysis.video_analysis.faces_detected > 0 ? '#d4edda' : '#fff3cd',
              borderRadius: '8px',
              border: `1px solid ${analysis.video_analysis.faces_detected > 0 ? '#c3e6cb' : '#ffeaa7'}`
            }}>
              <strong>Video Analysis Summary:</strong>
              <p style={{ margin: '8px 0 0 0', lineHeight: '1.5' }}>
                {analysis.video_analysis.faces_detected > 0
                  ? `Great! Your face was clearly visible in ${analysis.video_analysis.frames_analyzed} analyzed frames. The primary emotion detected was "${analysis.video_analysis.dominant_emotion}" with ${(analysis.video_analysis.confidence * 100).toFixed(0)}% confidence.`
                  : 'No faces were clearly detected in the video. Try recording with better lighting and positioning yourself closer to the camera for more accurate emotion analysis.'
                }
              </p>
            </div>
          </div>
        </div>
      )}

      <div style={{ marginBottom: '30px' }}>
        <h3>Transcript</h3>
        {results.transcript ? (
          <div style={{ 
            padding: '15px', 
            backgroundColor: '#FFFFFF', 
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
            backgroundColor: '#f8f9fa',
            borderRadius: '5px',
            padding: '15px',
            border: '1px solid #dee2e6'
          }}>
            {Object.entries(analysis.slang || results.slang || {}).map(([word, meaning]) => (
              <li key={word} style={{ 
                marginBottom: '12px',
                padding: '12px',
                backgroundColor: 'white',
                borderRadius: '6px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
                fontFamily: 'Poppins, Nunito, Circular, sans-serif',
                lineHeight: '1.5',
                fontWeight: '400',
                fontSize: '1rem'
              }}>
                <strong style={{ color: '#6c757d', fontWeight: '600', letterSpacing: '0.1px' }}>"{word}"</strong> 
                <span style={{ color: '#6c757d', fontSize: '1rem', fontWeight: '400' }}> → {meaning}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ 
            color: '#6c757d', 
            fontStyle: 'italic',
            padding: '16px',
            backgroundColor: '#FFFFFF',
            borderRadius: '6px',
            border: '1px solid #dee2e6',
            fontFamily: 'Poppins, Nunito, Circular, sans-serif',
            fontSize: '1rem',
            lineHeight: '1.5',
            fontWeight: '400',
            letterSpacing: '0.1px'
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
            backgroundColor: 'linear-gradient(135deg, #87CEEB 0%, #B0DCEB 100%)',
            background: '#87CEEB',
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
