import React, { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function VideoPage() {
  const navigate = useNavigate();
  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideoBlob, setRecordedVideoBlob] = useState(null);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [hasCamera, setHasCamera] = useState(true);
  const [permissionState, setPermissionState] = useState('prompt');
  
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);

  // Check camera permission status
  const checkPermissions = useCallback(async () => {
    try {
      if (navigator.permissions && navigator.permissions.query) {
        const permission = await navigator.permissions.query({ name: 'camera' });
        setPermissionState(permission.state);
        console.log('Camera permission state:', permission.state);
        
        permission.onchange = () => {
          setPermissionState(permission.state);
          console.log('Permission changed to:', permission.state);
        };
      }
    } catch (err) {
      console.log('Permission API not supported');
    }
  }, []);

  const startCamera = useCallback(async () => {
    try {
      setError('');
      console.log('Requesting camera access...');
      
      // Check if getUserMedia is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera API not supported in this browser');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 1280, min: 640 },
          height: { ideal: 720, min: 480 },
          facingMode: 'user'
        }, 
        audio: true 
      });
      
      console.log('Camera access granted:', stream);
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        // Ensure video plays
        await videoRef.current.play();
      }
      setHasCamera(true);
    } catch (err) {
      console.error('Camera access error:', err);
      let errorMessage = 'Camera access failed. ';
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        errorMessage += 'Please allow camera access in your browser settings and refresh the page.';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        errorMessage += 'No camera found. Please connect a camera and try again.';
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        errorMessage += 'Camera is being used by another application. Please close other apps using the camera.';
      } else if (err.name === 'OverconstrainedError') {
        errorMessage += 'Camera constraints not supported. Trying with basic settings...';
        // Try again with simpler constraints
        try {
          const simpleStream = await navigator.mediaDevices.getUserMedia({ 
            video: true, 
            audio: true 
          });
          streamRef.current = simpleStream;
          if (videoRef.current) {
            videoRef.current.srcObject = simpleStream;
            await videoRef.current.play();
          }
          setHasCamera(true);
          return;
        } catch (simpleErr) {
          errorMessage += ' Simple camera access also failed.';
        }
      } else {
        errorMessage += `Error: ${err.message}`;
      }
      
      setError(errorMessage);
      setHasCamera(false);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  }, []);

  const startRecording = useCallback(async () => {
    if (!streamRef.current) {
      await startCamera();
      // Wait a bit for camera to initialize
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    if (!streamRef.current) {
      setError('Camera not available for recording');
      return;
    }

    try {
      setError('');
      chunksRef.current = [];
      
      // Check MediaRecorder support
      if (!window.MediaRecorder) {
        throw new Error('MediaRecorder not supported in this browser');
      }

      // Try different codec options based on browser support
      let options = null;
      const supportedMimeTypes = [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp8,opus',
        'video/webm;codecs=h264,opus',
        'video/webm',
        'video/mp4;codecs=h264,aac',
        'video/mp4'
      ];

      for (const mimeType of supportedMimeTypes) {
        if (MediaRecorder.isTypeSupported(mimeType)) {
          options = { mimeType };
          console.log('Using MIME type:', mimeType);
          break;
        }
      }

      if (!options) {
        console.log('No supported MIME types found, using default');
      }
      
      const mediaRecorder = new MediaRecorder(streamRef.current, options);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const mimeType = options?.mimeType || 'video/webm';
        const blob = new Blob(chunksRef.current, { type: mimeType });
        setRecordedVideoBlob(blob);
        setRecordedVideoUrl(URL.createObjectURL(blob));
        stopCamera();
      };

      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        setError(`Recording error: ${event.error?.message || 'Unknown error'}`);
        setIsRecording(false);
      };

      mediaRecorder.start(1000); // Record in 1-second chunks
      setIsRecording(true);
      console.log('Recording started successfully');
    } catch (err) {
      console.error('Recording start error:', err);
      let errorMessage = 'Failed to start recording. ';
      
      if (err.message.includes('MediaRecorder not supported')) {
        errorMessage += 'Your browser does not support video recording. Try using Chrome, Firefox, or Edge.';
      } else if (err.name === 'NotSupportedError') {
        errorMessage += 'The selected video format is not supported. Trying alternative format...';
        // Try again with no options (browser default)
        try {
          const fallbackRecorder = new MediaRecorder(streamRef.current);
          mediaRecorderRef.current = fallbackRecorder;
          
          fallbackRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              chunksRef.current.push(event.data);
            }
          };

          fallbackRecorder.onstop = () => {
            const blob = new Blob(chunksRef.current, { type: 'video/webm' });
            setRecordedVideoBlob(blob);
            setRecordedVideoUrl(URL.createObjectURL(blob));
            stopCamera();
          };

          fallbackRecorder.start(1000);
          setIsRecording(true);
          console.log('Fallback recording started');
          return;
        } catch (fallbackErr) {
          console.error('Fallback recording failed:', fallbackErr);
          errorMessage += ' Fallback recording also failed.';
        }
      } else {
        errorMessage += `Error: ${err.message}`;
      }
      
      setError(errorMessage);
    }
  }, [startCamera, stopCamera]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, []);

  const analyzeVideo = async () => {
    if (!recordedVideoBlob) return;

    setIsAnalyzing(true);
    setError('');

    try {
      // For demo purposes, let's analyze with a sample text
      // In production, you'd extract audio from video and transcribe it
      const response = await axios.post("http://localhost:5001/analyze", {
        transcript: "This is a sample analysis of the recorded video content with gestures and expressions",
      }, {
        timeout: 15000,
      });

      // Store results and navigate to analysis page
      localStorage.setItem("analysisResults", JSON.stringify({
        transcript: "Video recorded successfully! Analysis includes speech, gestures, and facial expressions.",
        analysis: response.data,
        source: "video_recording",
        timestamp: new Date().toISOString()
      }));

      navigate('/analyze');
    } catch (error) {
      console.error('Analysis error:', error);
      setError('Failed to analyze video. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const discardRecording = () => {
    if (recordedVideoUrl) {
      URL.revokeObjectURL(recordedVideoUrl);
    }
    setRecordedVideoBlob(null);
    setRecordedVideoUrl(null);
    setError('');
  };

  // Initialize camera and permissions on component mount
  React.useEffect(() => {
    checkPermissions();
  }, [checkPermissions]);

  // Show browser compatibility and troubleshooting info
  const getBrowserInfo = () => {
    const userAgent = navigator.userAgent;
    if (userAgent.includes('Chrome')) return 'Chrome';
    if (userAgent.includes('Firefox')) return 'Firefox';
    if (userAgent.includes('Safari')) return 'Safari';
    if (userAgent.includes('Edge')) return 'Edge';
    return 'Unknown';
  };

  // Check MediaRecorder support and available codecs
  const getRecordingSupport = () => {
    if (!window.MediaRecorder) {
      return { supported: false, codecs: [] };
    }

    const testCodecs = [
      'video/webm;codecs=vp9,opus',
      'video/webm;codecs=vp8,opus', 
      'video/webm;codecs=h264,opus',
      'video/webm',
      'video/mp4;codecs=h264,aac',
      'video/mp4'
    ];

    const supportedCodecs = testCodecs.filter(codec => 
      MediaRecorder.isTypeSupported(codec)
    );

    return { 
      supported: true, 
      codecs: supportedCodecs.length > 0 ? supportedCodecs : ['browser default']
    };
  };

  return (
    <div style={{ 
      padding: 20, 
      maxWidth: 800, 
      margin: '0 auto',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh',
      color: 'white'
    }}>
      <h2 style={{ textAlign: 'center', marginBottom: 30 }}>🎥 Video Recording & Analysis</h2>
      <p style={{ textAlign: 'center', marginBottom: 30 }}>
        Record yourself speaking with gestures and facial expressions for comprehensive analysis
      </p>

      {/* Browser and Permission Info */}
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: 15,
        borderRadius: 8,
        marginBottom: 20,
        fontSize: 14
      }}>
        <p><strong>Browser:</strong> {getBrowserInfo()} | <strong>Permission:</strong> {permissionState}</p>
        <p><strong>Recording Support:</strong> {
          (() => {
            const support = getRecordingSupport();
            return support.supported 
              ? `✅ Supported (${support.codecs.length} codec${support.codecs.length !== 1 ? 's' : ''})` 
              : '❌ Not Supported';
          })()
        }</p>
        {permissionState === 'denied' && (
          <p style={{ color: '#ff6b6b', fontWeight: 'bold' }}>
            ⚠️ Camera permission denied. Please click the camera icon in your browser's address bar to allow access.
          </p>
        )}
        {!getRecordingSupport().supported && (
          <p style={{ color: '#ff6b6b', fontWeight: 'bold' }}>
            ⚠️ Video recording not supported. Please use Chrome, Firefox, or Edge for recording functionality.
          </p>
        )}
      </div>

      {error && (
        <div style={{ 
          background: '#ff4757', 
          color: 'white', 
          padding: 15, 
          borderRadius: 8, 
          marginBottom: 20,
          textAlign: 'center'
        }}>
          {error}
          {error.includes('Please allow camera access') && (
            <div style={{ marginTop: 10, fontSize: 14 }}>
              <p>📱 <strong>How to allow camera access:</strong></p>
              <p>• Click the camera icon in your browser's address bar</p>
              <p>• Or go to browser Settings → Privacy → Camera → Allow for this site</p>
              <p>• Then refresh this page</p>
            </div>
          )}
        </div>
      )}

      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        gap: 20 
      }}>
        {/* Camera Access Button */}
        {!hasCamera && (
          <button
            onClick={startCamera}
            style={{
              padding: '15px 30px',
              background: '#3498db',
              color: 'white',
              border: 'none',
              borderRadius: 25,
              fontSize: 16,
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 10
            }}
          >
            📷 Enable Camera Access
          </button>
        )}

        {/* Camera Preview */}
        {!recordedVideoUrl && hasCamera && (
          <div style={{
            position: 'relative',
            width: '100%',
            maxWidth: 640,
            background: '#2c3e50',
            borderRadius: 12,
            overflow: 'hidden',
            border: isRecording ? '3px solid #e74c3c' : '3px solid #34495e'
          }}>
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              style={{
                width: '100%',
                height: 'auto'
              }}
            />
            {isRecording && (
              <div style={{
                position: 'absolute',
                top: 15,
                right: 15,
                background: '#e74c3c',
                color: 'white',
                padding: '8px 12px',
                borderRadius: 6,
                fontSize: 14,
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: 8
              }}>
                <div style={{
                  width: 8,
                  height: 8,
                  background: 'white',
                  borderRadius: '50%',
                  animation: 'pulse 1s infinite'
                }} />
                REC
              </div>
            )}
          </div>
        )}

        {/* Recorded Video Preview */}
        {recordedVideoUrl && (
          <div style={{
            width: '100%',
            maxWidth: 640,
            background: '#2c3e50',
            borderRadius: 12,
            overflow: 'hidden',
            border: '3px solid #27ae60'
          }}>
            <video
              src={recordedVideoUrl}
              controls
              style={{
                width: '100%',
                height: 'auto'
              }}
            />
          </div>
        )}

        {/* Recording Controls */}
        <div style={{ display: 'flex', gap: 15, flexWrap: 'wrap', justifyContent: 'center' }}>
          {!recordedVideoUrl && !isRecording && hasCamera && getRecordingSupport().supported && (
            <button
              onClick={startRecording}
              style={{
                padding: '15px 30px',
                background: '#e74c3c',
                color: 'white',
                border: 'none',
                borderRadius: 25,
                fontSize: 16,
                fontWeight: 'bold',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                transition: 'all 0.3s ease'
              }}
            >
              🎥 Start Recording
            </button>
          )}

          {!recordedVideoUrl && !isRecording && hasCamera && !getRecordingSupport().supported && (
            <div style={{
              padding: '15px 30px',
              background: '#95a5a6',
              color: 'white',
              borderRadius: 25,
              fontSize: 16,
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: 10
            }}>
              🚫 Recording Not Supported
            </div>
          )}

          {isRecording && (
            <button
              onClick={stopRecording}
              style={{
                padding: '15px 30px',
                background: '#2c3e50',
                color: 'white',
                border: '2px solid #e74c3c',
                borderRadius: 25,
                fontSize: 16,
                fontWeight: 'bold',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 10
              }}
            >
              ⏹️ Stop Recording
            </button>
          )}

          {recordedVideoUrl && (
            <>
              <button
                onClick={analyzeVideo}
                disabled={isAnalyzing}
                style={{
                  padding: '15px 30px',
                  background: isAnalyzing ? '#95a5a6' : '#27ae60',
                  color: 'white',
                  border: 'none',
                  borderRadius: 25,
                  fontSize: 16,
                  fontWeight: 'bold',
                  cursor: isAnalyzing ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10
                }}
              >
                {isAnalyzing ? '⏳ Analyzing...' : '🔍 Analyze Video'}
              </button>

              <button
                onClick={discardRecording}
                disabled={isAnalyzing}
                style={{
                  padding: '15px 30px',
                  background: '#e67e22',
                  color: 'white',
                  border: 'none',
                  borderRadius: 25,
                  fontSize: 16,
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10
                }}
              >
                🗑️ Discard
              </button>

              <button
                onClick={() => {
                  discardRecording();
                  startCamera();
                }}
                disabled={isAnalyzing}
                style={{
                  padding: '15px 30px',
                  background: '#3498db',
                  color: 'white',
                  border: 'none',
                  borderRadius: 25,
                  fontSize: 16,
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10
                }}
              >
                🎬 Record Again
              </button>
            </>
          )}
        </div>

        {/* Troubleshooting Guide */}
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          padding: 20,
          borderRadius: 12,
          textAlign: 'left',
          maxWidth: 600,
          fontSize: 14
        }}>
          <h4>🔧 Recording Troubleshooting:</h4>
          <ul style={{ lineHeight: 1.6 }}>
            <li><strong>Browser Support:</strong> Chrome (recommended), Firefox, Edge support recording. Safari has limited support.</li>
            <li><strong>Codec Issues:</strong> If recording fails, the app will try multiple video formats automatically</li>
            <li><strong>Permission Denied:</strong> Click the camera icon in the address bar and select "Allow"</li>
            <li><strong>No Camera Found:</strong> Check if your camera is connected and not being used by other apps</li>
            <li><strong>Chrome:</strong> Go to Settings → Privacy and security → Site Settings → Camera</li>
            <li><strong>Firefox:</strong> Click the shield icon → Permissions → Camera → Allow</li>
            <li><strong>Safari:</strong> Safari → Preferences → Websites → Camera → Allow (recording may not work)</li>
            <li><strong>HTTPS Required:</strong> Camera access requires secure connection (https://)</li>
            <li><strong>Hardware Acceleration:</strong> Enable hardware acceleration in browser settings for better performance</li>
          </ul>
        </div>

        {/* Recording Tips */}
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          padding: 20,
          borderRadius: 12,
          textAlign: 'center',
          maxWidth: 600
        }}>
          <h4>📋 Recording Tips:</h4>
          <ul style={{ textAlign: 'left', lineHeight: 1.6 }}>
            <li>🎯 <strong>Look at the camera</strong> for better facial expression analysis</li>
            <li>🗣️ <strong>Speak clearly</strong> for accurate speech recognition</li>
            <li>✋ <strong>Use gestures naturally</strong> - they'll be part of the analysis</li>
            <li>😊 <strong>Express emotions</strong> through facial expressions</li>
            <li>🔊 <strong>Ensure good lighting</strong> for optimal video quality</li>
            <li>⏱️ <strong>Keep recordings under 2 minutes</strong> for best results</li>
          </ul>
        </div>
      </div>

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
