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
  
  // Audio recording states
  const [isAudioRecording, setIsAudioRecording] = useState(false);
  const [recordedAudioBlob, setRecordedAudioBlob] = useState(null);
  const [recordedAudioUrl, setRecordedAudioUrl] = useState(null);
  const [audioRecordingTime, setAudioRecordingTime] = useState(0);
  
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  const audioRecorderRef = useRef(null);
  const audioStreamRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioTimerRef = useRef(null);

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
      console.log('Permission API not supported', err);
      // Don't throw error, just log it
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
      // Create FormData to send the video file for processing
      const formData = new FormData();
      formData.append('video', recordedVideoBlob, 'recording.webm');

      // Use the dedicated video analysis endpoint
      const response = await axios.post("http://localhost:5002/analyze-video", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 45000, // Increased timeout for video processing
      });

      // The video analysis endpoint returns comprehensive analysis results
      const analysisData = response.data;
      
      // Check if the analysis was successful
      if (!analysisData.success) {
        throw new Error(analysisData.error || 'Video analysis failed');
      }
      
      // Extract analysis results
      const analysisResults = analysisData.analysis_results || {};
      const videoInfo = analysisData.video_info || {};
      
      // Create a transcript placeholder since video analysis focuses on facial emotions
      const transcript = analysisData.transcript || "Video analyzed for facial emotions (no speech detected)";
      
      // Prepare comprehensive analysis results
      let combinedResults = {
        transcript: transcript,
        source: "video_recording",
        timestamp: new Date().toISOString(),
        analysis: {
          tone: analysisResults.dominant_emotion || "neutral",
          tone_explanation: analysisData.summary || "Video facial emotion analysis completed",
          message: "Video analysis with facial emotion detection completed",
          video_analysis: {
            dominant_emotion: analysisResults.dominant_emotion,
            confidence: analysisResults.confidence,
            frames_analyzed: analysisResults.frames_analyzed,
            faces_detected: analysisResults.faces_detected_total,
            emotion_distribution: analysisResults.emotion_distribution,
            frame_by_frame: analysisResults.frame_by_frame
          },
          video_info: videoInfo
        },
        accessibility_features: {
          tone_explanation: analysisResults.dominant_emotion ? 
            `Your facial expressions showed primarily ${analysisResults.dominant_emotion} emotion` : 
            "Your facial expressions were analyzed",
          simplified_message: analysisData.summary || transcript,
          communication_tips: [
            analysisResults.faces_detected_total > 0 ? 
              "Great! Your face was clearly visible for emotion analysis" : 
              "Try positioning yourself closer to the camera for better analysis",
            analysisResults.confidence > 0.7 ? 
              "Your facial expressions were clear and confident" : 
              "Keep practicing - facial expression clarity improves with time",
            videoInfo.duration_seconds ? 
              `Good video length: ${videoInfo.duration_seconds.toFixed(1)} seconds` : 
              "Video was successfully recorded"
          ],
          clarity_score: analysisResults.faces_detected_total > 0 ? "Good" : "Needs improvement",
          suggested_improvements: [
            "Great job recording your video!",
            analysisResults.frames_analyzed > 5 ? 
              "Multiple frames were analyzed for accuracy" : 
              "Try a slightly longer recording for more comprehensive analysis",
            "Continue practicing to build confidence with video communication"
          ]
        }
      };

      // If we have slang detection results, include them  
      if (analysisData.slang) {
        combinedResults.analysis.slang = analysisData.slang;
      }

      // Store comprehensive results
      localStorage.setItem("analysisResults", JSON.stringify(combinedResults));

      navigate('/analyze');
    } catch (error) {
      console.error('Video analysis error:', error);
      let errorMessage = 'Failed to analyze video. ';
      
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage += 'The analysis is taking longer than expected. This might be due to a large video file or slow internet connection.';
      } else if (error.response?.status === 413) {
        errorMessage += 'The video file is too large. Please try recording a shorter video.';
      } else if (error.response?.status === 415) {
        errorMessage += 'The video format is not supported. Please try again.';
      } else {
        errorMessage += 'Please check your internet connection and try again.';
      }
      
      setError(errorMessage);
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

  // Audio recording functions
  const startAudioRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioStreamRef.current = stream;
      audioChunksRef.current = [];

      const mediaRecorder = new MediaRecorder(stream);
      audioRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setRecordedAudioBlob(blob);
        setRecordedAudioUrl(URL.createObjectURL(blob));
        
        // Stop the stream
        if (audioStreamRef.current) {
          audioStreamRef.current.getTracks().forEach(track => track.stop());
          audioStreamRef.current = null;
        }
      };

      mediaRecorder.start();
      setIsAudioRecording(true);
      setAudioRecordingTime(0);

      // Start timer
      audioTimerRef.current = setInterval(() => {
        setAudioRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (err) {
      console.error('Audio recording error:', err);
      setError('Failed to access microphone. Please allow microphone access.');
    }
  };

  const stopAudioRecording = () => {
    if (audioRecorderRef.current && audioRecorderRef.current.state !== 'inactive') {
      audioRecorderRef.current.stop();
      setIsAudioRecording(false);
      
      // Clear timer
      if (audioTimerRef.current) {
        clearInterval(audioTimerRef.current);
        audioTimerRef.current = null;
      }
    }
  };

  const discardAudioRecording = () => {
    if (recordedAudioUrl) {
      URL.revokeObjectURL(recordedAudioUrl);
    }
    setRecordedAudioBlob(null);
    setRecordedAudioUrl(null);
    setAudioRecordingTime(0);
  };

  const analyzeAudio = async () => {
    if (!recordedAudioBlob) return;

    setIsAnalyzing(true);
    setError('');

    try {
      // Create FormData to send the audio file
      const formData = new FormData();
      formData.append('audio', recordedAudioBlob, 'recording.webm');

      const response = await axios.post("http://localhost:5002/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000,
      });

      const transcript = response.data.transcript || "Could not understand the audio clearly";
      
      // Prepare results with accessibility features
      let analysisResults = {
        transcript: transcript,
        source: "audio_recording",
        timestamp: new Date().toISOString()
      };

      if (transcript && transcript !== "Could not understand the audio clearly") {
        // Send for comprehensive tone analysis with accessibility focus
        try {
          const analysisResponse = await axios.post("http://localhost:5002/analyze", {
            transcript: transcript,
            context: "audio_only_recording",
            assistance_type: "neurodivergent_and_esl"
          }, {
            timeout: 15000,
          });

          analysisResults.analysis = analysisResponse.data;
          
          // Add accessibility and learning features
          analysisResults.accessibility_features = {
            tone_explanation: analysisResponse.data.tone_explanation || "The tone sounds conversational",
            simplified_message: analysisResponse.data.simplified_version || transcript,
            communication_tips: analysisResponse.data.communication_tips || [
              "Your speech was clear and understandable",
              "Good pacing in your delivery"
            ],
            clarity_score: analysisResponse.data.clarity_score || "Good",
            pronunciation_feedback: analysisResponse.data.pronunciation_notes || [],
            suggested_improvements: analysisResponse.data.improvements || [],
            cultural_context: analysisResponse.data.cultural_notes || ""
          };

        } catch (analysisError) {
          console.warn('Advanced analysis failed, providing basic feedback:', analysisError);
          // Provide encouraging basic analysis
          analysisResults.analysis = {
            tone: "Conversational",
            tone_explanation: "Your speech was recorded successfully",
            message: "Audio analysis completed"
          };
          analysisResults.accessibility_features = {
            tone_explanation: "Your voice came through clearly in the recording",
            simplified_message: transcript,
            communication_tips: [
              "Great job recording your audio!",
              "Your speech was clear enough for transcription",
              "Keep practicing to build confidence"
            ],
            clarity_score: "Successfully processed",
            pronunciation_feedback: ["Audio quality was sufficient for analysis"],
            suggested_improvements: ["Continue practicing speaking at a comfortable pace"],
            cultural_context: "Every accent and speaking style is valuable"
          };
        }
      } else {
        // Encouraging message for unclear audio
        analysisResults.analysis = {
          tone: "Audio unclear",
          message: "We had trouble understanding the audio, but that's okay!"
        };
        analysisResults.accessibility_features = {
          tone_explanation: "The audio wasn't clear enough to analyze, but this is common and nothing to worry about",
          simplified_message: "Audio recording completed - clarity could be improved",
          communication_tips: [
            "Don't worry! Many factors can affect audio clarity",
            "Try speaking a bit slower next time",
            "Get closer to your microphone",
            "Find a quiet space for recording"
          ],
          clarity_score: "Needs improvement - but keep practicing!",
          pronunciation_feedback: [
            "Audio quality can affect transcription accuracy",
            "This doesn't reflect your speaking ability"
          ],
          suggested_improvements: [
            "Practice in a quiet room",
            "Speak at a comfortable volume",
            "Take your time - there's no rush",
            "Every attempt helps you improve"
          ],
          cultural_context: "Everyone's voice and accent is unique and valuable"
        };
      }

      localStorage.setItem("analysisResults", JSON.stringify(analysisResults));
      navigate('/analyze');
    } catch (error) {
      console.error('Audio analysis error:', error);
      let errorMessage = 'Audio analysis encountered an issue. ';
      
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage += "The analysis is taking a bit longer. This is normal for detailed processing.";
      } else if (error.response?.status === 413) {
        errorMessage += "The audio file is quite large. Try a shorter recording.";
      } else {
        errorMessage += "Don't worry - technical issues happen. Please try again.";
      }
      
      setError(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Format recording time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Initialize camera and permissions on component mount
  React.useEffect(() => {
    checkPermissions().catch(err => {
      console.error('Error checking permissions:', err);
    });
    
    // Add global error handler for unhandled promise rejections
    const handleUnhandledRejection = (event) => {
      console.warn('Unhandled promise rejection:', event.reason);
      // Prevent the default behavior (logging to console)
      event.preventDefault();
    };
    
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    
    return () => {
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
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
      background: 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
      minHeight: '100vh',
      color: '#333333'
    }}>
      <h2 style={{ textAlign: 'center', marginBottom: 30, color: '#666666' }}>Communication Practice & Analysis</h2>
      <p style={{ textAlign: 'center', marginBottom: 30, fontSize: 16, lineHeight: 1.5, color: '#666666' }}>
        Practice speaking with confidence! Record yourself and get helpful feedback on your communication style, 
        tone, and clarity. Perfect for English learners, neurodivergent individuals, or anyone wanting to improve their communication.
      </p>

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
              <p><strong>How to allow camera access:</strong></p>
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
              background: 'linear-gradient(135deg, #87CEEB 0%, #B0DCEB 100%)',
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
            Enable Camera Access
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
            border: isRecording ? '3px solid #A8D8A8' : '3px solid #C5E4C5'
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
                background: '#A8D8A8',
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
              onClick={() => {
                startRecording().catch(err => {
                  console.error('Recording start failed:', err);
                  setError('Failed to start recording');
                });
              }}
              style={{
                padding: '15px 30px',
                background: 'linear-gradient(135deg, #A8D8A8 0%, #C5E4C5 100%)',
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
              Start Recording
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
              Recording Not Supported
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
              Stop Recording
            </button>
          )}

          {recordedVideoUrl && (
            <>
              <button
                onClick={() => {
                  analyzeVideo().catch(err => {
                    console.error('Video analysis failed:', err);
                    setError('Analysis failed. Please try again.');
                    setIsAnalyzing(false);
                  });
                }}
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
                  {isAnalyzing ? 'Analyzing Your Communication...' : 'Get Communication Feedback'}
                </button>              <button
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
                Discard
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
                Record Again
              </button>
            </>
          )}
        </div>

        {/* Audio Recording Section */}
        <div style={{
          width: '100%',
          maxWidth: 640,
          background: 'rgba(168, 216, 168, 0.1)',
          borderRadius: 12,
          padding: 20,
          marginTop: 30
        }}>
          <h3 style={{ textAlign: 'center', marginBottom: 20, color: '#666666' }}>
            Voice Practice & Feedback
          </h3>
          <p style={{ textAlign: 'center', marginBottom: 15, fontSize: 14, color: '#666666' }}>
            Practice speaking and get personalized feedback on your tone, clarity, and communication style
          </p>
          
          {/* Audio Recording Controls */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 15 }}>
            
            {/* Recording Time Display */}
            {(isAudioRecording || recordedAudioUrl) && (
              <div style={{
                fontSize: 24,
                fontWeight: 'bold',
                color: isAudioRecording ? '#e74c3c' : '#27ae60',
                fontFamily: 'monospace'
              }}>
                {formatTime(audioRecordingTime)}
              </div>
            )}

            {/* Apple Voice Memo Style Button */}
            {!recordedAudioUrl && (
              <button
                onClick={() => {
                  if (isAudioRecording) {
                    stopAudioRecording();
                  } else {
                    startAudioRecording().catch(err => {
                      console.error('Audio recording start failed:', err);
                      setError('Failed to start audio recording');
                    });
                  }
                }}
                style={{
                  width: 80,
                  height: 80,
                  borderRadius: '50%',
                  border: isAudioRecording ? '4px solid #e74c3c' : '4px solid #ffffff',
                  background: isAudioRecording 
                    ? 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
                    : 'linear-gradient(135deg, #ffffff 0%, #ecf0f1 100%)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: isAudioRecording ? 24 : 28,
                  color: isAudioRecording ? 'white' : '#2c3e50',
                  transition: 'all 0.3s ease',
                  boxShadow: isAudioRecording 
                    ? '0 0 20px rgba(231, 76, 60, 0.5)' 
                    : '0 4px 15px rgba(0,0,0,0.2)',
                  position: 'relative',
                  overflow: 'hidden'
                }}
                onMouseEnter={(e) => {
                  if (!isAudioRecording) {
                    e.target.style.transform = 'scale(1.05)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isAudioRecording) {
                    e.target.style.transform = 'scale(1)';
                  }
                }}
              >
                {isAudioRecording ? (
                  <div style={{
                    width: 20,
                    height: 20,
                    background: 'white',
                    borderRadius: 2
                  }} />
                ) : (
                  'MIC'
                )}
                
                {/* Pulse animation for recording */}
                {isAudioRecording && (
                  <div style={{
                    position: 'absolute',
                    top: -4,
                    left: -4,
                    right: -4,
                    bottom: -4,
                    borderRadius: '50%',
                    border: '2px solid #e74c3c',
                    animation: 'recordPulse 2s infinite'
                  }} />
                )}
              </button>
            )}

            {/* Audio Playback */}
            {recordedAudioUrl && (
              <div style={{
                background: 'rgba(255,255,255,0.2)',
                borderRadius: 8,
                padding: 15,
                width: '100%',
                textAlign: 'center'
              }}>
                <audio 
                  controls 
                  src={recordedAudioUrl}
                  style={{
                    width: '100%',
                    maxWidth: 300
                  }}
                />
              </div>
            )}

            {/* Audio Action Buttons */}
            {recordedAudioUrl && (
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', justifyContent: 'center' }}>
                <button
                  onClick={() => {
                    analyzeAudio().catch(err => {
                      console.error('Audio analysis failed:', err);
                      setError('Audio analysis failed. Please try again.');
                      setIsAnalyzing(false);
                    });
                  }}
                  disabled={isAnalyzing}
                  style={{
                    padding: '10px 20px',
                    background: isAnalyzing ? '#95a5a6' : '#27ae60',
                    color: 'white',
                    border: 'none',
                    borderRadius: 20,
                    fontSize: 14,
                    fontWeight: 'bold',
                    cursor: isAnalyzing ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8
                  }}
                  >
                    {isAnalyzing ? 'Analyzing Your Speech...' : 'Get Speech Feedback'}
                  </button>                <button
                  onClick={discardAudioRecording}
                  disabled={isAnalyzing}
                  style={{
                    padding: '10px 20px',
                    background: '#e67e22',
                    color: 'white',
                    border: 'none',
                    borderRadius: 20,
                    fontSize: 14,
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8
                  }}
                >
                  Discard
                </button>

                <button
                  onClick={() => {
                    discardAudioRecording();
                  }}
                  disabled={isAnalyzing}
                  style={{
                    padding: '10px 20px',
                    background: '#3498db',
                    color: 'white',
                    border: 'none',
                    borderRadius: 20,
                    fontSize: 14,
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8
                  }}
                >
                  Record Again
                </button>
              </div>
            )}

            {/* Recording Status Text */}
            <p style={{
              textAlign: 'center',
              margin: 0,
              fontSize: 14,
              color: 'rgba(255,255,255,0.8)'
            }}>
              {isAudioRecording 
                ? 'Recording your voice... Tap to finish' 
                : recordedAudioUrl 
                  ? 'Great job! Your voice was recorded successfully!'
                  : 'Tap the button to start practicing - take your time!'
              }
            </p>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
        
        @keyframes recordPulse {
          0% { 
            transform: scale(1);
            opacity: 1;
          }
          50% { 
            transform: scale(1.1);
            opacity: 0.5;
          }
          100% { 
            transform: scale(1);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
}
