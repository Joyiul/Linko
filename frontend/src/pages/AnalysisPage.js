import React, { useEffect, useState } from 'react';
import EmojiToneBar from '../components/EmojiToneBar';
import HighlightedText from '../components/HighlightedText';
import './AnalysisPage.css';

export default function AnalysisPage() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem("analysisResults");
    if (stored) setResults(JSON.parse(stored));
  }, []);

  if (!results) return (
    <div style={{ padding: 20, textAlign: 'center' }}>
      <h2>No Analysis Results</h2>
      <p>Please upload an audio file or enter text on the <a href="/listen">Listening Page</a> first.</p>
    </div>
  );

  return (
    <div style={{ padding: 20 }}>
      <h2>🎯 Analysis Results</h2>
      
      {results.filename && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#e8f4fd', borderRadius: '5px' }}>
          <strong>📁 File:</strong> {results.filename}
        </div>
      )}
      
      <div style={{ marginBottom: '30px' }}>
        <h3>🎭 Emotional Tone</h3>
        <EmojiToneBar tone={results.tone || "😐 Neutral"} />
      </div>

      <div style={{ marginBottom: '30px' }}>
        <h3>📝 Transcript</h3>
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
        <h3>🗣️ Slang Detection</h3>
        {Object.keys(results.slang || {}).length > 0 ? (
          <ul style={{ 
            listStyle: 'none', 
            padding: 0,
            backgroundColor: '#fff3cd',
            borderRadius: '5px',
            padding: '15px'
          }}>
            {Object.entries(results.slang).map(([word, meaning]) => (
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
          🎤 Analyze Another File
        </button>
      </div>
    </div>
  );
}
