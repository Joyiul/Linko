import React, { useEffect, useState } from 'react';
import EmojiToneBar from '../components/EmojiToneBar';
import HighlightedText from '../components/HighlightedText';
import TextSimplificationBox from '../components/TextSimplificationBox';
import EmotionImage from '../components/EmotionImage';
import FormalityAnalysis from '../components/FormalityAnalysis';
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

            {/* Primary Detected Emotion */}
            {emotionAnalysis.detected_emotion && (
              <div>
                <h5>Detected Emotion:</h5>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center',
                  padding: '20px',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '12px',
                  border: '2px solid #28a745',
                  marginBottom: '20px'
                }}>
                  <div style={{ 
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '12px'
                  }}>
                    <EmotionImage emotion={emotionAnalysis.detected_emotion} size={80} />
                    <div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        textTransform: 'capitalize', 
                        fontFamily: 'Poppins, Nunito, Circular, sans-serif', 
                        color: '#495057', 
                        fontWeight: '600', 
                        letterSpacing: '0.5px',
                        marginBottom: '8px'
                      }}>
                        {emotionAnalysis.detected_emotion}
                      </div>
                      <div style={{ 
                        fontSize: '1.1rem',
                        color: getConfidenceColor(emotionAnalysis.confidence || 0),
                        fontFamily: 'Poppins, Nunito, Circular, sans-serif',
                        fontWeight: '500'
                      }}>
                        Confidence: {((emotionAnalysis.confidence || 0) * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
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
              <h5 style={{ marginBottom: '15px', color: '#6c757d' }}>Detected Facial Emotion:</h5>
              {analysis.video_analysis.dominant_emotion ? (
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center',
                  padding: '20px',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '12px',
                  border: '2px solid #17a2b8',
                  marginBottom: '20px'
                }}>
                  <div style={{ 
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '12px'
                  }}>
                    <EmotionImage emotion={analysis.video_analysis.dominant_emotion} size={70} />
                    <div>
                      <div style={{ 
                        fontSize: '1.3rem', 
                        fontWeight: '600', 
                        textTransform: 'capitalize', 
                        color: '#495057',
                        marginBottom: '8px'
                      }}>
                        {analysis.video_analysis.dominant_emotion}
                      </div>
                      {analysis.video_analysis.confidence && (
                        <div style={{
                          fontSize: '1rem',
                          color: getConfidenceColor(analysis.video_analysis.confidence),
                          fontWeight: '500'
                        }}>
                          Confidence: {(analysis.video_analysis.confidence * 100).toFixed(1)}%
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ 
                  textAlign: 'center',
                  padding: '20px',
                  backgroundColor: '#fff3cd',
                  borderRadius: '8px',
                  border: '1px solid #ffeaa7',
                  color: '#856404'
                }}>
                  No facial emotion detected
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
          <div>
            <div style={{ 
              padding: '15px', 
              backgroundColor: '#FFFFFF', 
              borderRadius: '5px',
              border: '1px solid #dee2e6',
              fontStyle: 'italic',
              fontSize: '1.1rem',
              lineHeight: '1.6'
            }}>
              {/* Display highlighted text if sarcasm analysis is available, otherwise show plain transcript */}
              {analysis.comprehensive_sarcasm_analysis && analysis.comprehensive_sarcasm_analysis.highlighted_text ? (
                <div dangerouslySetInnerHTML={{ 
                  __html: analysis.comprehensive_sarcasm_analysis.highlighted_text 
                }} />
              ) : (
                <HighlightedText text={results.transcript} />
              )}
            </div>
            
            {/* Sarcasm Key - only show if sarcasm is detected */}
            {analysis.comprehensive_sarcasm_analysis && analysis.comprehensive_sarcasm_analysis.sarcasm_detected && (
              <div style={{ 
                marginTop: '10px', 
                fontSize: '0.9rem', 
                color: '#6c757d',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '8px 12px',
                backgroundColor: '#f8f9fa',
                borderRadius: '5px',
                border: '1px solid #dee2e6'
              }}>
                <span style={{ 
                  color: 'red', 
                  fontWeight: 'bold',
                  fontSize: '1.1rem'
                }}>■</span>
                <span>Red text indicates sarcasm</span>
                <span style={{ 
                  marginLeft: 'auto',
                  fontSize: '0.8rem',
                  color: '#999'
                }}>
                  Confidence: {(analysis.comprehensive_sarcasm_analysis.confidence * 100).toFixed(1)}%
                </span>
              </div>
            )}
          </div>
        ) : (
          <p style={{ color: '#666' }}>No transcript available</p>
        )}
      </div>

      {/* Text Simplification Section */}
      {results.transcript && (
        <div style={{ marginBottom: '30px' }}>
          <TextSimplificationBox 
            originalText={results.transcript} 
            initialSimplification={analysis.text_simplification}
          />
        </div>
      )}

      {/* Formality Analysis Section */}
      {results.transcript && (
        <div style={{ marginBottom: '30px' }}>
          <FormalityAnalysis 
            text={results.transcript}
            initialData={analysis.formality_analysis ? { 
              formality_analysis: analysis.formality_analysis,
              explicit_formality_breakdown: analysis.explicit_formality_breakdown,
              success: true 
            } : null}
            showTitle={true}
          />
        </div>
      )}

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
            {Object.entries(analysis.slang || results.slang || {}).map(([word, slangData]) => {
              // Handle both old format (string) and new format (object)
              const meaning = typeof slangData === 'string' ? slangData : slangData?.meaning || slangData;
              const popularity = typeof slangData === 'object' ? slangData?.popularity : null;
              const type = typeof slangData === 'object' ? slangData?.type : null;
              
              return (
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
                  {popularity && (
                    <span style={{ 
                      marginLeft: '8px', 
                      fontSize: '0.8rem', 
                      color: popularity === 'high' ? '#28a745' : popularity === 'medium' ? '#ffc107' : '#6c757d',
                      fontWeight: '500'
                    }}>
                      [{popularity}]
                    </span>
                  )}
                  {type && (
                    <span style={{ 
                      marginLeft: '4px', 
                      fontSize: '0.7rem', 
                      color: '#6c757d',
                      fontStyle: 'italic'
                    }}>
                      ({type})
                    </span>
                  )}
                </li>
              );
            })}
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

      {/* AI Disclaimer */}
      <div style={{
        marginTop: '30px',
        padding: '15px',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #dee2e6',
        textAlign: 'center'
      }}>
        <p style={{
          margin: 0,
          fontSize: '14px',
          color: '#6c757d',
          fontStyle: 'italic'
        }}>
          ⚠️ This response was generated using AI. Please use responsibly.
        </p>
      </div>
    </div>
  );
}
