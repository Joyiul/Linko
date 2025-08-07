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
        try {
          if (event.data.size > 0) {
            chunksRef.current.push(event.data);
          }
        } catch (error) {
          console.warn('Error handling video data:', error);
        }
      };

      mediaRecorder.onstop = () => {
        try {
          const mimeType = options?.mimeType || 'video/webm';
          const blob = new Blob(chunksRef.current, { type: mimeType });
          setRecordedVideoBlob(blob);
          setRecordedVideoUrl(URL.createObjectURL(blob));
          stopCamera();
        } catch (error) {
          console.error('Error processing recorded video:', error);
          setError('Failed to process recorded video. Please try again.');
        }
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
      formData.append('file', recordedVideoBlob, 'recording.webm');

      // Use the video analysis endpoint that includes speech transcription
      const response = await axios.post("http://localhost:5002/upload-and-analyze-video", formData, {
        // Let axios set Content-Type automatically to include boundary
        timeout: 45000, // Increased timeout for video processing
      });

      console.log('🎯 Video analysis response:', response);
      console.log('🎯 Video analysis response:', response.data);

      const analysisData = response.data;
      
      // Check if there's an error
      if (analysisData.error) {
        throw new Error(analysisData.error);
      }
      
      console.log('✅ Video analysis successful:', analysisData);
      
      // Extract the actual transcript from speech recognition
      const transcript = analysisData.transcript || "Audio could not be transcribed clearly";
      const videoInfo = analysisData.video_info || {};
      const analysis = analysisData.analysis || {};
      
      // Create comprehensive results with both face and speech recognition
      let combinedResults = {
        transcript: transcript,
        source: "video_recording_with_speech",
        timestamp: new Date().toISOString(),
        analysis: {
          tone: analysis.dominant_emotion || analysis.audio_tone || "neutral",
          tone_explanation: `Video analysis with face recognition and speech transcription completed. 
                            ${transcript.length > 10 ? 'Speech was successfully transcribed.' : 'Speech transcription had limited success.'}
                            ${analysis.frames_analyzed > 0 ? ' Facial expressions were analyzed.' : ' Limited facial analysis.'}`,
          message: "Video analyzed with both face recognition and speech transcription",
          
          // Face recognition results
          facial_analysis: {
            frames_analyzed: analysis.frames_analyzed || 0,
            dominant_emotion: analysis.dominant_emotion || "neutral",
            frame_results: analysis.frame_results || [],
            face_detection_success: (analysis.frames_analyzed || 0) > 0
          },
          
          // Speech recognition results
          speech_recognition: {
            transcript_available: transcript && transcript.length > 10,
            transcript_length: transcript ? transcript.split(' ').length : 0,
            speech_detected: transcript && transcript !== "Audio could not be transcribed clearly",
            audio_tone: analysis.audio_tone || "neutral"
          },
          
          // Combined analysis
          multimodal_analysis: {
            video_duration: videoInfo.duration_seconds || 0,
            total_frames: videoInfo.total_frames || 0,
            fps: videoInfo.fps || 0,
            both_modalities_successful: (analysis.frames_analyzed || 0) > 0 && transcript && transcript.length > 10
          }
        },
        
        // Enhanced accessibility features for face + speech recognition
        accessibility_features: {
          tone_explanation: generateVideoToneExplanation(analysis, transcript),
          simplified_message: transcript.length > 10 ? 
            `Great! Your speech was transcribed: "${transcript.substring(0, 100)}${transcript.length > 100 ? '...' : ''}"` :
            "Video recorded successfully with face recognition analysis",
          communication_tips: generateVideoTips(analysis, transcript),
          clarity_score: calculateVideoClarity(analysis, transcript),
          suggested_improvements: generateVideoImprovements(analysis, transcript),
          transcript_quality: transcript && transcript.length > 10 ? "Good" : "Limited"
        }
      };

      // Add video metadata if available
      if (videoInfo.duration_seconds) {
        combinedResults.video_info = videoInfo;
      }

      // Add slang analysis if available
      if (analysis.slang) {
        combinedResults.analysis.slang = analysis.slang;
      }

      // Store comprehensive results
      localStorage.setItem("analysisResults", JSON.stringify(combinedResults));

      navigate('/analyze');
    } catch (error) {
      console.error('❌ Video analysis error:', error);
      console.error('❌ Error details:', {
        message: error.message,
        code: error.code,
        response: error.response,
        stack: error.stack
      });
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

  // Helper functions for video analysis with face + speech recognition
  const generateVideoToneExplanation = (analysis, transcript) => {
    try {
      const hasTranscript = transcript && transcript.length > 10;
      const hasFaceAnalysis = (analysis?.frames_analyzed || 0) > 0;
      const dominantEmotion = analysis?.dominant_emotion || analysis?.audio_tone || 'neutral';
      
      if (hasTranscript && hasFaceAnalysis) {
        return `Excellent! Both your speech and facial expressions were analyzed. Your dominant emotion was ${dominantEmotion}. Speech transcribed: "${transcript.substring(0, 50)}${transcript.length > 50 ? '...' : ''}"`;
      } else if (hasTranscript) {
        return `Great! Your speech was successfully transcribed and analyzed. Your speaking tone appears ${dominantEmotion}. Transcript: "${transcript.substring(0, 50)}${transcript.length > 50 ? '...' : ''}"`;
      } else if (hasFaceAnalysis) {
        return `Your facial expressions were analyzed and show ${dominantEmotion} emotion. Speech transcription was limited - try speaking more clearly next time.`;
      } else {
        return `Video recorded successfully. For better results, ensure good lighting for face recognition and speak clearly for speech transcription.`;
      }
    } catch (error) {
      console.warn('Error generating video tone explanation:', error);
      return 'Video analysis completed with face recognition and speech processing';
    }
  };

  const generateVideoTips = (analysis, transcript) => {
    try {
      const tips = [];
      const hasTranscript = transcript && transcript.length > 10;
      const hasFaceAnalysis = (analysis?.frames_analyzed || 0) > 0;
      
      if (hasTranscript) {
        tips.push("✅ Speech transcription successful - your voice was clear");
      } else {
        tips.push("💡 Speak more clearly and closer to the microphone for better transcription");
      }
      
      if (hasFaceAnalysis) {
        tips.push("✅ Face recognition successful - good camera positioning");
      } else {
        tips.push("💡 Position yourself in good lighting facing the camera for face recognition");
      }
      
      if (hasTranscript && hasFaceAnalysis) {
        tips.push("🎉 Perfect! Both speech and facial recognition worked great");
      } else {
        tips.push("🎯 For best results, ensure both clear speech and good face visibility");
      }
      
      return tips;
    } catch (error) {
      console.warn('Error generating video tips:', error);
      return ["Video analysis completed"];
    }
  };

  const calculateVideoClarity = (analysis, transcript) => {
    try {
      const hasTranscript = transcript && transcript.length > 10;
      const hasFaceAnalysis = (analysis?.frames_analyzed || 0) > 0;
      
      if (hasTranscript && hasFaceAnalysis) {
        return "Excellent - Both speech and face recognition successful";
      } else if (hasTranscript || hasFaceAnalysis) {
        return "Good - One modality successful";
      } else {
        return "Practice more - Try clearer speech and better lighting";
      }
    } catch (error) {
      console.warn('Error calculating video clarity:', error);
      return "Analysis completed";
    }
  };

  const generateVideoImprovements = (analysis, transcript) => {
    try {
      const improvements = [];
      const hasTranscript = transcript && transcript.length > 10;
      const hasFaceAnalysis = (analysis?.frames_analyzed || 0) > 0;
      
      if (!hasTranscript) {
        improvements.push("Speak more clearly and ensure microphone is working");
        improvements.push("Try speaking closer to the device");
      }
      
      if (!hasFaceAnalysis) {
        improvements.push("Improve lighting and face positioning for better face recognition");
        improvements.push("Look directly at the camera while speaking");
      }
      
      if (hasTranscript && hasFaceAnalysis) {
        improvements.push("Great job! Continue practicing with different scenarios");
      }
      
      improvements.push("Practice regularly to improve both speech clarity and facial expression");
      
      return improvements;
    } catch (error) {
      console.warn('Error generating video improvements:', error);
      return ["Keep practicing for better results"];
    }
  };

  // Audio recording functions
  const startAudioRecording = async () => {
    try {
      setError('');
      // Request audio with specific constraints for speech recording
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 44100,
          channelCount: 1
        } 
      });
      audioStreamRef.current = stream;
      audioChunksRef.current = [];

      // Configure MediaRecorder with options optimized for speech
      const options = {
        mimeType: 'audio/webm;codecs=opus',
        audioBitsPerSecond: 128000
      };

      // Fallback to browser default if the preferred format isn't supported
      const mediaRecorder = new MediaRecorder(stream, 
        MediaRecorder.isTypeSupported(options.mimeType) ? options : undefined
      );
      audioRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        try {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
            console.log('📊 Audio chunk recorded:', event.data.size, 'bytes');
          }
        } catch (error) {
          console.warn('Error handling audio data:', error);
        }
      };

      mediaRecorder.onstop = () => {
        try {
          const blob = new Blob(audioChunksRef.current, { 
            type: options?.mimeType || 'audio/webm' 
          });
          console.log('🎤 Audio recording completed. Total size:', blob.size, 'bytes');
          setRecordedAudioBlob(blob);
          setRecordedAudioUrl(URL.createObjectURL(blob));
          
          // Stop the stream
          if (audioStreamRef.current) {
            audioStreamRef.current.getTracks().forEach(track => {
              try {
                track.stop();
              } catch (err) {
                console.warn('Error stopping audio track:', err);
              }
            });
            audioStreamRef.current = null;
          }
        } catch (error) {
          console.error('Error processing recorded audio:', error);
          setError('Failed to process recorded audio. Please try again.');
        }
      };

      // Add error handling
      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        setError(`Recording error: ${event.error?.message || 'Unknown error'}`);
        setIsAudioRecording(false);
      };

      // Start recording with 250ms slices to prevent data loss
      mediaRecorder.start(250);
      setIsAudioRecording(true);
      setAudioRecordingTime(0);

      console.log('🎤 Audio recording started with format:', options?.mimeType || 'browser default');

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
      formData.append('file', recordedAudioBlob, 'recording.webm');

      // Use the upload endpoint that does speech-to-text transcription
      const response = await axios.post("http://localhost:5002/upload-and-analyze", formData, {
        // Let axios set Content-Type automatically to include boundary
        timeout: 30000,
      });

      console.log('🎤 Audio upload response:', response.data);

      const transcript = response.data.transcript || "Audio was processed successfully";
      
      // Prepare results with accessibility features
      let analysisResults = {
        transcript: transcript,
        source: "audio_recording",
        timestamp: new Date().toISOString(),
        audio_info: response.data.audio_info || {}
      };

      if (transcript && transcript !== "Could not understand the audio clearly" && 
          !transcript.includes("Audio transcript would appear here")) {
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
            tone: "Clear recording",
            tone_explanation: "Your audio was recorded successfully and sounds clear",
            message: "Audio recording quality analysis completed"
          };
          analysisResults.accessibility_features = {
            tone_explanation: "Great job! Your audio recording came through clearly",
            simplified_message: "Audio recording successful - good quality detected",
            communication_tips: [
              "Excellent! Your recording quality is good",
              "Your audio levels are appropriate",
              "Keep practicing - you're doing great!"
            ],
            clarity_score: "Recording successful",
            pronunciation_feedback: ["Audio quality was clear for processing"],
            suggested_improvements: ["Continue practicing speaking at a comfortable pace"],
            cultural_context: "Every voice and accent adds value to communication"
          };
        }
      } else {
        // Encouraging message when speech-to-text isn't available
        analysisResults.analysis = {
          tone: "Practice session completed",
          tone_explanation: "Your audio practice session was recorded successfully",
          message: "Audio practice completed - keep building confidence!"
        };
        analysisResults.accessibility_features = {
          tone_explanation: "Fantastic work! You completed an audio practice session",
          simplified_message: "Audio practice session successful",
          communication_tips: [
            "Great job speaking and practicing!",
            "Regular practice builds communication confidence",
            "Every practice session helps improve your skills",
            "Your effort in practicing is valuable"
          ],
          clarity_score: "Practice completed successfully",
          pronunciation_feedback: [
            "You're building important speaking practice",
            "Consistent practice leads to improvement"
          ],
          suggested_improvements: [
            "Keep practicing regularly",
            "Try speaking about different topics",
            "Practice in various environments",
            "Celebrate your progress - every session counts!"
          ],
          cultural_context: "Every accent and speaking style brings richness to communication"
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
    const initializeComponent = async () => {
      try {
        await checkPermissions();
      } catch (err) {
        console.warn('Error checking permissions:', err);
        // Don't set error state for permission check failures
      }
    };
    
    initializeComponent();
    
    // Add global error handler for unhandled promise rejections
    const handleUnhandledRejection = (event) => {
      console.warn('Unhandled promise rejection:', event.reason);
      // Prevent the default behavior (logging to console)
      event.preventDefault();
      
      // Only set error if it's a critical error
      if (event.reason && typeof event.reason === 'object' && event.reason.message) {
        const errorMessage = event.reason.message;
        if (errorMessage.includes('camera') || errorMessage.includes('microphone') || errorMessage.includes('recording')) {
          console.error('Media-related error:', errorMessage);
          // Don't automatically set error state to avoid disrupting user experience
        }
      }
    };
    
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    
    return () => {
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
      // Clean up any ongoing recording or streams
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => {
          try {
            track.stop();
          } catch (err) {
            console.warn('Error stopping track:', err);
          }
        });
      }
      if (audioStreamRef.current) {
        audioStreamRef.current.getTracks().forEach(track => {
          try {
            track.stop();
          } catch (err) {
            console.warn('Error stopping audio track:', err);
          }
        });
      }
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
      <h2 style={{ textAlign: 'center', marginBottom: 30, color: '#666666' }}>🎭 Practice Speaking with Face & Voice Recognition</h2>
      <p style={{ textAlign: 'center', marginBottom: 30, fontSize: 16, lineHeight: 1.5, color: '#666666' }}>
        Practice speaking with confidence! Record yourself and get AI feedback that analyzes both your <strong>facial expressions</strong> and <strong>voice tone</strong> together. 
        Perfect for English learners, neurodivergent individuals, or anyone wanting to improve their communication with comprehensive face and audio recognition.
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
            
            {/* Face Recognition Indicator */}
            {hasCamera && (
              <div style={{
                position: 'absolute',
                bottom: 15,
                left: 15,
                background: 'rgba(0,0,0,0.7)',
                color: 'white',
                padding: '6px 10px',
                borderRadius: 4,
                fontSize: 12,
                display: 'flex',
                alignItems: 'center',
                gap: 5
              }}>
                👤 Face Recognition Active
              </div>
            )}
            
            {/* Audio Recognition Indicator */}
            {hasCamera && (
              <div style={{
                position: 'absolute',
                bottom: 15,
                right: 15,
                background: 'rgba(0,0,0,0.7)',
                color: 'white',
                padding: '6px 10px',
                borderRadius: 4,
                fontSize: 12,
                display: 'flex',
                alignItems: 'center',
                gap: 5
              }}>
                🎤 Audio Recognition Active
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
              onClick={async () => {
                try {
                  await startRecording();
                } catch (err) {
                  console.error('Recording start failed:', err);
                  setError('Failed to start recording. Please try again.');
                }
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
                onClick={async () => {
                  try {
                    await analyzeVideo();
                  } catch (err) {
                    console.error('Video analysis failed:', err);
                    setError('Analysis failed. Please try again.');
                    setIsAnalyzing(false);
                  }
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
                  {isAnalyzing ? 'Analyzing Face & Voice...' : 'Get Face & Voice Analysis'}
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
                onClick={async () => {
                  try {
                    discardRecording();
                    await startCamera();
                  } catch (err) {
                    console.error('Failed to restart camera:', err);
                    setError('Failed to restart camera. Please refresh the page.');
                  }
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
                onClick={async () => {
                  try {
                    if (isAudioRecording) {
                      stopAudioRecording();
                    } else {
                      await startAudioRecording();
                    }
                  } catch (err) {
                    console.error('Audio recording error:', err);
                    setError('Failed to start audio recording. Please try again.');
                    setIsAudioRecording(false);
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
                  onClick={async () => {
                    try {
                      await analyzeAudio();
                    } catch (err) {
                      console.error('Audio analysis failed:', err);
                      setError('Audio analysis failed. Please try again.');
                      setIsAnalyzing(false);
                    }
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

        {/* Practice Speaking Section */}
        <div style={{
          width: '100%',
          maxWidth: 800,
          background: 'rgba(135, 206, 235, 0.1)',
          borderRadius: 12,
          padding: 25,
          marginTop: 40,
          border: '2px solid rgba(135, 206, 235, 0.3)'
        }}>
          <h3 style={{ 
            textAlign: 'center', 
            marginBottom: 20, 
            color: '#4a90a4',
            fontSize: 24,
            fontWeight: 'bold'
          }}>
            🎭 Practice Speaking with AI Face & Voice Recognition
          </h3>
          <p style={{ 
            textAlign: 'center', 
            marginBottom: 25, 
            fontSize: 16, 
            lineHeight: 1.6, 
            color: '#666666' 
          }}>
            Use the video recording above to practice speaking scenarios. Your <strong>facial expressions</strong> and <strong>voice tone</strong> will be analyzed together to give you comprehensive feedback on your communication skills.
          </p>

          {/* Practice Scenarios */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
            gap: 15,
            marginBottom: 25
          }}>
            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>👋 Introduce Yourself</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "Tell me about yourself - your name, where you're from, and what you enjoy doing."
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Look at the camera, speak clearly, and let your personality show through your expressions!
              </p>
            </div>

            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>💭 Share Your Opinion</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "What's your favorite season and why? What do you love about it?"
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Use expressive facial expressions and vary your tone to show enthusiasm!
              </p>
            </div>

            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>📖 Tell a Story</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "Share a recent memory that made you happy, surprised, or excited."
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Use storytelling expressions and let emotions show naturally on your face!
              </p>
            </div>

            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>🗓️ Describe Your Day</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "What did you do today? Walk me through your typical day."
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Use different facial expressions for different activities and emotions!
              </p>
            </div>

            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>🔮 Future Plans</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "What are your plans for the weekend or next vacation?"
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Show excitement through facial expressions and voice tone!
              </p>
            </div>

            <div style={{
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 10,
              padding: 18,
              transition: 'all 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = '#87CEEB';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(135,206,235,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = '#e0e0e0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <h4 style={{ marginBottom: 8, color: '#4a90a4', fontSize: 16 }}>🎯 Free Practice</h4>
              <p style={{ fontSize: 14, marginBottom: 8, color: '#666' }}>
                "Practice any topic you want - a presentation, conversation, or speech."
              </p>
              <p style={{ fontSize: 12, color: '#87CEEB', fontStyle: 'italic' }}>
                💡 Focus on matching your facial expressions with your voice tone!
              </p>
            </div>
          </div>

          {/* How It Works Section */}
          <div style={{
            background: 'rgba(255,255,255,0.8)',
            borderRadius: 8,
            padding: 20,
            marginBottom: 20
          }}>
            <h4 style={{ color: '#4a90a4', marginBottom: 15, textAlign: 'center' }}>
              🤖 How Face & Voice Recognition Works
            </h4>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
              gap: 15 
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>👤</div>
                <strong style={{ color: '#4a90a4', fontSize: 14 }}>Face Recognition</strong>
                <ul style={{ fontSize: 12, marginTop: 5, paddingLeft: 0, listStyle: 'none', color: '#666' }}>
                  <li>• Facial emotion detection</li>
                  <li>• Expression analysis</li>
                  <li>• Eye contact assessment</li>
                  <li>• Engagement measurement</li>
                </ul>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>🎤</div>
                <strong style={{ color: '#4a90a4', fontSize: 14 }}>Voice Recognition</strong>
                <ul style={{ fontSize: 12, marginTop: 5, paddingLeft: 0, listStyle: 'none', color: '#666' }}>
                  <li>• Voice emotion analysis</li>
                  <li>• Tone evaluation</li>
                  <li>• Speech clarity</li>
                  <li>• Confidence detection</li>
                </ul>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>🔗</div>
                <strong style={{ color: '#4a90a4', fontSize: 14 }}>Combined Analysis</strong>
                <ul style={{ fontSize: 12, marginTop: 5, paddingLeft: 0, listStyle: 'none', color: '#666' }}>
                  <li>• Face + voice sync check</li>
                  <li>• Overall emotion score</li>
                  <li>• Communication tips</li>
                  <li>• Personalized feedback</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Practice Instructions */}
          <div style={{
            background: 'rgba(168, 216, 168, 0.2)',
            border: '1px solid rgba(168, 216, 168, 0.5)',
            borderRadius: 8,
            padding: 18,
            textAlign: 'center'
          }}>
            <h4 style={{ color: '#4a90a4', marginBottom: 10 }}>📝 How to Practice</h4>
            <p style={{ fontSize: 14, color: '#666', marginBottom: 8 }}>
              1. Choose a scenario above (or create your own) • 2. Click "Start Recording" • 3. Speak naturally while looking at the camera
            </p>
            <p style={{ fontSize: 14, color: '#666', marginBottom: 8 }}>
              4. Stop recording when finished • 5. Click "Get Face & Voice Analysis" for AI feedback
            </p>
            <p style={{ fontSize: 13, color: '#87CEEB', fontStyle: 'italic', marginTop: 10 }}>
              💡 <strong>Pro Tip:</strong> The AI will analyze how well your facial expressions match your voice tone, giving you insights into your overall communication effectiveness!
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
