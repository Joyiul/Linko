import React, { useState, useRef } from 'react';
import { theme } from '../theme';

export default function VoiceRecorder({ onRecordingComplete }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const chunks = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        setRecordedBlob(blob);
        if (onRecordingComplete) {
          onRecordingComplete(blob);
        }
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setError('');
    } catch (err) {
      console.error('Error starting recording:', err);
      setError('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', margin: '20px 0' }}>
      {error && (
        <div style={{ 
          color: 'red', 
          marginBottom: '10px', 
          padding: '10px', 
          backgroundColor: '#ffe6e6', 
          borderRadius: '5px' 
        }}>
          {error}
        </div>
      )}
      
            <div style={{ marginBottom: theme.spacing.md }}>
        {!isRecording ? (
          <button
            onClick={startRecording}
            style={{
              ...theme.typography.button,
              backgroundColor: theme.colors.primary,
              color: theme.colors.onPrimary,
              border: 'none',
              borderRadius: theme.borderRadius.bubble,
              padding: theme.spacing.md + ' ' + theme.spacing.lg,
              fontSize: '18px',
              fontWeight: '600',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto',
              gap: theme.spacing.sm,
              boxShadow: theme.shadows.bubble,
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = theme.shadows.heavy;
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = theme.shadows.bubble;
            }}
          >
            🎤 Start Recording
          </button>
        ) : (
          <button
            onClick={stopRecording}
            style={{
              ...theme.typography.button,
              backgroundColor: theme.colors.error,
              color: theme.colors.onPrimary,
              border: 'none',
              borderRadius: theme.borderRadius.bubble,
              padding: theme.spacing.md + ' ' + theme.spacing.lg,
              fontSize: '18px',
              fontWeight: '600',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto',
              gap: theme.spacing.sm,
              boxShadow: theme.shadows.bubble,
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = theme.shadows.heavy;
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = theme.shadows.bubble;
            }}
          >
            🛑 Stop Recording
          </button>
        )}
      </div>

      {isRecording && (
        <div style={{ 
          color: theme.colors.error, 
          fontWeight: '600',
          fontFamily: theme.typography.fontFamily,
          animation: 'pulse 1s infinite',
          textAlign: 'center',
          marginTop: theme.spacing.sm
        }}>
          🔴 Recording in progress...
        </div>
      )}

      {recordedBlob && !isRecording && (
        <div style={{ 
          marginTop: theme.spacing.md, 
          padding: theme.spacing.sm, 
          backgroundColor: theme.colors.primaryLight, 
          borderRadius: theme.borderRadius.medium,
          color: theme.colors.primary,
          textAlign: 'center',
          fontFamily: theme.typography.fontFamily,
          fontWeight: '500'
        }}>
          ✅ Recording completed! Ready to decipher.
        </div>
      )}

      <style jsx>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
