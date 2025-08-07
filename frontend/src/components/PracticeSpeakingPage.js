import React, { useState, useRef, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function PracticeSpeakingPage() {
  const navigate = useNavigate();
  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideoBlob, setRecordedVideoBlob] = useState(null);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [hasCamera, setHasCamera] = useState(false);
  const [permissionState, setPermissionState] = useState('prompt');
  const [practicePrompt, setPracticePrompt] = useState('');
  const [practiceSession, setPracticeSession] = useState(null);
  
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);

  // Practice scenarios for speaking practice
  const practiceScenarios = [
    {
      id: 'introduction',
      title: 'Introduce Yourself',
      prompt: 'Tell me about yourself - your name, where you\'re from, what you do, and one interesting hobby you have.',
      tips: 'Speak clearly, maintain good eye contact with the camera, and try to sound confident and friendly.'
    },
    {
      id: 'daily_routine',
      title: 'Describe Your Day',
      prompt: 'Describe what you did today or what a typical day looks like for you.',
      tips: 'Use past tense verbs, speak at a natural pace, and try to include emotions about different activities.'
    },
    {
      id: 'opinion',
      title: 'Share Your Opinion',
      prompt: 'What\'s your favorite season and why? Explain what you like about it.',
      tips: 'Use opinion expressions like "I think", "I believe", and support your opinion with reasons.'
    },
    {
      id: 'storytelling',
      title: 'Tell a Short Story',
      prompt: 'Tell me about a memorable experience you had recently - something that made you happy, surprised, or excited.',
      tips: 'Use descriptive language, vary your tone to match the emotions, and maintain good facial expressions.'
    },
    {
      id: 'future_plans',
      title: 'Talk About Future Plans',
      prompt: 'What are your plans for this weekend or next vacation? What are you looking forward to?',
      tips: 'Use future tense, express enthusiasm, and let your facial expressions show your excitement.'
    }
  ];

  // Initialize camera and permissions
  const checkPermissions = useCallback(async () => {
    try {
      if (navigator.permissions && navigator.permissions.query) {
        const permission = await navigator.permissions.query({ name: 'camera' });
        setPermissionState(permission.state);
        
        permission.onchange = () => {
          setPermissionState(permission.state);
        };
      }
    } catch (err) {
      console.log('Permission API not supported', err);
    }
  }, []);

  const startCamera = useCallback(async () => {
    try {
      setError('');
      
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera API not supported in this browser');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 1280, min: 640 },
          height: { ideal: 720, min: 480 },
          facingMode: 'user'
        }, 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });
      
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setHasCamera(true);
    } catch (err) {
      console.error('Camera access error:', err);
      let errorMessage = 'Camera access failed. ';
      
      if (err.name === 'NotAllowedError') {
        errorMessage += 'Please allow camera and microphone access for practice speaking.';
      } else if (err.name === 'NotFoundError') {
        errorMessage += 'No camera or microphone found. Please connect devices and try again.';
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

  const startPracticeSession = (scenario) => {
    setPracticeSession(scenario);
    setPracticePrompt(scenario.prompt);
    setError('');
  };

  const startRecording = useCallback(async () => {
    if (!streamRef.current) {
      await startCamera();
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    if (!streamRef.current) {
      setError('Camera and microphone not available for practice recording');
      return;
    }

    try {
      setError('');
      chunksRef.current = [];
      
      if (!window.MediaRecorder) {
        throw new Error('MediaRecorder not supported in this browser');
      }

      // Use video format optimized for face recognition
      const supportedMimeTypes = [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp8,opus',
        'video/webm',
        'video/mp4'
      ];

      let options = null;
      for (const mimeType of supportedMimeTypes) {
        if (MediaRecorder.isTypeSupported(mimeType)) {
          options = { mimeType };
          break;
        }
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

      mediaRecorder.start(1000);
      setIsRecording(true);
    } catch (err) {
      console.error('Recording start error:', err);
      setError('Failed to start practice recording. Please try again.');
    }
  }, [startCamera, stopCamera]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, []);

  const analyzePracticeSpeaking = async () => {
    if (!recordedVideoBlob || !practiceSession) return;

    setIsAnalyzing(true);
    setError('');

    try {
      // Create FormData for multimodal analysis
      const formData = new FormData();
      formData.append('video', recordedVideoBlob, 'practice_recording.webm');
      formData.append('practice_scenario', practiceSession.id);
      formData.append('practice_prompt', practiceSession.prompt);
      
      // Use the enhanced video analysis endpoint with multimodal capabilities
      const response = await axios.post("http://localhost:5002/analyze-video", formData, {
        timeout: 60000, // Extended timeout for comprehensive analysis
      });

      console.log('🎭 Practice speaking analysis response:', response.data);

      const analysisData = response.data;
      
      if (!analysisData.success) {
        throw new Error(analysisData.error || 'Practice analysis failed');
      }
      
      // Extract comprehensive analysis results
      const analysisResults = analysisData.analysis_results || {};
      const videoInfo = analysisData.video_info || {};
      const processingInfo = analysisData.processing_info || {};
      
      // Generate practice-specific feedback
      const practiceResults = {
        transcript: `Practice Session: ${practiceSession.title}`,
        source: "practice_speaking_multimodal",
        timestamp: new Date().toISOString(),
        practice_session: {
          scenario: practiceSession,
          prompt_given: practiceSession.prompt,
          tips_provided: practiceSession.tips
        },
        
        analysis: {
          // Overall communication assessment
          tone: analysisResults.final_emotion || "neutral",
          tone_explanation: generatePracticeExplanation(analysisResults, practiceSession),
          message: "Practice speaking session completed with multimodal analysis",
          
          // Multimodal analysis results
          multimodal_analysis: {
            final_emotion: analysisResults.final_emotion,
            confidence: analysisResults.confidence,
            fusion_method: analysisResults.fusion_method,
            modalities_agreement: analysisResults.modalities_agreement,
            modalities_used: processingInfo.modalities_used || []
          },
          
          // Face recognition results
          facial_recognition: {
            faces_detected: analysisResults.facial_analysis?.faces_detected_total || 0,
            frames_analyzed: analysisResults.facial_analysis?.frames_analyzed || 0,
            dominant_emotion: analysisResults.facial_analysis?.dominant_emotion,
            facial_confidence: analysisResults.facial_analysis?.facial_confidence,
            emotion_distribution: analysisResults.facial_analysis?.emotion_distribution || {},
            engagement_level: calculateEngagementLevel(analysisResults.facial_analysis)
          },
          
          // Audio recognition results
          audio_recognition: {
            speech_detected: analysisResults.audio_analysis?.analyzed || false,
            emotion_detected: analysisResults.audio_analysis?.emotion,
            audio_confidence: analysisResults.audio_analysis?.confidence,
            clarity_assessment: assessAudioClarity(analysisResults.audio_analysis)
          },
          
          // Practice-specific metrics
          practice_assessment: {
            eye_contact_quality: assessEyeContact(analysisResults.facial_analysis),
            speaking_confidence: calculateSpeakingConfidence(analysisResults),
            emotional_expression: assessEmotionalExpression(analysisResults),
            overall_performance: calculateOverallPerformance(analysisResults)
          }
        },
        
        // Enhanced feedback for practice improvement
        practice_feedback: {
          strengths: generateStrengthsFeedback(analysisResults, practiceSession),
          improvements: generateImprovementSuggestions(analysisResults, practiceSession),
          next_steps: generateNextSteps(analysisResults, practiceSession),
          confidence_building: generateConfidenceBuilding(analysisResults),
          technical_tips: generateTechnicalTips(analysisResults, processingInfo)
        }
      };

      // Add video metadata
      if (videoInfo.duration_seconds) {
        practiceResults.video_info = videoInfo;
      }

      // Store comprehensive practice results
      localStorage.setItem("practiceResults", JSON.stringify(practiceResults));
      localStorage.setItem("analysisResults", JSON.stringify(practiceResults));

      navigate('/analyze');
    } catch (error) {
      console.error('❌ Practice analysis error:', error);
      let errorMessage = 'Practice analysis encountered an issue. ';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage += 'Analysis is taking longer than expected - this is normal for comprehensive speech analysis.';
      } else if (error.response?.status === 413) {
        errorMessage += 'Practice recording is too large. Try a shorter session.';
      } else {
        errorMessage += 'Please try again or contact support if the issue persists.';
      }
      
      setError(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Helper functions for practice assessment
  const generatePracticeExplanation = (results, session) => {
    const emotion = results?.final_emotion || 'neutral';
    const confidence = results?.confidence || 0;
    return `Great job practicing "${session.title}"! Your speaking showed ${emotion} emotion with ${(confidence * 100).toFixed(0)}% confidence. Keep practicing to build your communication skills!`;
  };

  const calculateEngagementLevel = (facialAnalysis) => {
    const facesDetected = facialAnalysis?.faces_detected_total || 0;
    const framesAnalyzed = facialAnalysis?.frames_analyzed || 1;
    const faceRatio = facesDetected / framesAnalyzed;
    
    if (faceRatio > 0.8) return "Excellent";
    if (faceRatio > 0.6) return "Good";
    if (faceRatio > 0.4) return "Fair";
    return "Needs improvement";
  };

  const assessAudioClarity = (audioAnalysis) => {
    if (!audioAnalysis?.analyzed) return "Audio not detected";
    const confidence = audioAnalysis.confidence || 0;
    
    if (confidence > 0.7) return "Clear speech";
    if (confidence > 0.5) return "Mostly clear";
    if (confidence > 0.3) return "Somewhat unclear";
    return "Unclear speech";
  };

  const assessEyeContact = (facialAnalysis) => {
    const facesDetected = facialAnalysis?.faces_detected_total || 0;
    const framesAnalyzed = facialAnalysis?.frames_analyzed || 1;
    
    if (facesDetected / framesAnalyzed > 0.7) return "Good eye contact";
    return "Practice looking at the camera more";
  };

  const calculateSpeakingConfidence = (results) => {
    const overallConfidence = (results?.confidence || 0) * 100;
    
    if (overallConfidence > 70) return "Confident speaker";
    if (overallConfidence > 50) return "Developing confidence";
    return "Building confidence";
  };

  const assessEmotionalExpression = (results) => {
    const emotion = results?.final_emotion;
    if (!emotion || emotion === 'neutral') return "Practice varying your emotional expression";
    return "Good emotional expression detected";
  };

  const calculateOverallPerformance = (results) => {
    const confidence = results?.confidence || 0;
    const facialDetected = results?.facial_analysis?.faces_detected_total || 0;
    const audioAnalyzed = results?.audio_analysis?.analyzed || false;
    
    let score = 0;
    if (confidence > 0.5) score += 25;
    if (facialDetected > 0) score += 25;
    if (audioAnalyzed) score += 25;
    if (confidence > 0.7) score += 25;
    
    if (score >= 75) return "Excellent practice session";
    if (score >= 50) return "Good practice session";
    if (score >= 25) return "Fair practice session";
    return "Keep practicing - you're improving!";
  };

  const generateStrengthsFeedback = (results, session) => {
    const strengths = [];
    
    if ((results?.confidence || 0) > 0.6) {
      strengths.push("Strong overall confidence in your delivery");
    }
    
    if ((results?.facial_analysis?.faces_detected_total || 0) > 0) {
      strengths.push("Good camera presence and facial visibility");
    }
    
    if (results?.audio_analysis?.analyzed) {
      strengths.push("Clear audio recording - your voice came through well");
    }
    
    if (results?.modalities_agreement) {
      strengths.push("Your facial expressions and voice showed consistent emotions");
    }
    
    if (strengths.length === 0) {
      strengths.push("You completed the practice session - that's a great first step!");
    }
    
    return strengths;
  };

  const generateImprovementSuggestions = (results, session) => {
    const suggestions = [];
    
    if ((results?.facial_analysis?.faces_detected_total || 0) === 0) {
      suggestions.push("Position yourself directly in front of the camera with good lighting");
    }
    
    if (!results?.audio_analysis?.analyzed) {
      suggestions.push("Speak more clearly and ensure your microphone is working");
    }
    
    if ((results?.confidence || 0) < 0.5) {
      suggestions.push("Practice the prompt a few times before recording to build confidence");
    }
    
    if (!results?.modalities_agreement) {
      suggestions.push("Try to match your facial expressions with your tone of voice");
    }
    
    suggestions.push(`For "${session.title}" scenarios, remember: ${session.tips}`);
    
    return suggestions;
  };

  const generateNextSteps = (results, session) => {
    const nextSteps = [
      "Try the same practice scenario again to see your improvement",
      "Practice with a different scenario to work on various communication skills",
      "Record yourself in different lighting conditions to improve visibility",
      "Practice speaking for longer periods to build stamina and confidence"
    ];
    
    return nextSteps.slice(0, 3); // Return top 3 suggestions
  };

  const generateConfidenceBuilding = (results) => {
    return [
      "Remember: Every practice session helps you improve",
      "Focus on progress, not perfection",
      "Your unique communication style is valuable",
      "Building confidence takes time - be patient with yourself"
    ];
  };

  const generateTechnicalTips = (results, processingInfo) => {
    const tips = [];
    
    if (!processingInfo?.audio_extracted) {
      tips.push("Ensure microphone permissions are enabled for better audio analysis");
    }
    
    if ((results?.facial_analysis?.frames_analyzed || 0) < 10) {
      tips.push("Try recording for at least 10-15 seconds for better analysis");
    }
    
    tips.push("Use good lighting and position your face in the center of the frame");
    tips.push("Speak clearly and at a natural pace for best analysis results");
    
    return tips;
  };

  const discardRecording = () => {
    if (recordedVideoUrl) {
      URL.revokeObjectURL(recordedVideoUrl);
    }
    setRecordedVideoBlob(null);
    setRecordedVideoUrl(null);
    setError('');
  };

  const resetPracticeSession = () => {
    setPracticeSession(null);
    setPracticePrompt('');
    discardRecording();
  };

  useEffect(() => {
    checkPermissions();
    
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [checkPermissions]);

  return (
    <div style={{ 
      padding: 20, 
      maxWidth: 900, 
      margin: '0 auto',
      background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
      minHeight: '100vh',
      color: '#333333'
    }}>
      <h2 style={{ textAlign: 'center', marginBottom: 20, color: '#495057' }}>
        🎭 Practice Speaking with AI Feedback
      </h2>
      <p style={{ textAlign: 'center', marginBottom: 30, fontSize: 16, lineHeight: 1.6, color: '#6c757d' }}>
        Practice speaking with comprehensive AI analysis using <strong>face recognition</strong> and <strong>audio recognition</strong>. 
        Get detailed feedback on your facial expressions, voice emotions, confidence level, and communication effectiveness.
      </p>

      {error && (
        <div style={{ 
          background: '#dc3545', 
          color: 'white', 
          padding: 15, 
          borderRadius: 8, 
          marginBottom: 20,
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      {/* Practice Scenario Selection */}
      {!practiceSession && (
        <div style={{ marginBottom: 30 }}>
          <h3 style={{ textAlign: 'center', marginBottom: 20, color: '#495057' }}>
            Choose a Practice Scenario
          </h3>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
            gap: 15 
          }}>
            {practiceScenarios.map((scenario) => (
              <div
                key={scenario.id}
                onClick={() => startPracticeSession(scenario)}
                style={{
                  background: '#ffffff',
                  border: '2px solid #dee2e6',
                  borderRadius: 12,
                  padding: 20,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}
                onMouseEnter={(e) => {
                  e.target.style.borderColor = '#007bff';
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 4px 12px rgba(0,123,255,0.15)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.borderColor = '#dee2e6';
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                }}
              >
                <h4 style={{ marginBottom: 10, color: '#007bff' }}>{scenario.title}</h4>
                <p style={{ fontSize: 14, marginBottom: 10, color: '#6c757d' }}>
                  {scenario.prompt}
                </p>
                <p style={{ fontSize: 12, color: '#28a745', fontStyle: 'italic' }}>
                  💡 {scenario.tips}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Active Practice Session */}
      {practiceSession && (
        <div style={{ marginBottom: 30 }}>
          <div style={{
            background: '#e7f3ff',
            border: '2px solid #007bff',
            borderRadius: 12,
            padding: 20,
            marginBottom: 20
          }}>
            <h3 style={{ color: '#007bff', marginBottom: 10 }}>
              📝 Practice: {practiceSession.title}
            </h3>
            <p style={{ fontSize: 16, marginBottom: 15, color: '#333' }}>
              <strong>Your task:</strong> {practiceSession.prompt}
            </p>
            <p style={{ fontSize: 14, color: '#28a745', fontStyle: 'italic' }}>
              💡 <strong>Tips:</strong> {practiceSession.tips}
            </p>
            <button
              onClick={resetPracticeSession}
              style={{
                marginTop: 10,
                padding: '8px 16px',
                background: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: 20,
                fontSize: 14,
                cursor: 'pointer'
              }}
            >
              Choose Different Scenario
            </button>
          </div>

          {/* Camera Setup */}
          {!hasCamera && (
            <div style={{ textAlign: 'center', marginBottom: 20 }}>
              <button
                onClick={startCamera}
                style={{
                  padding: '15px 30px',
                  background: 'linear-gradient(135deg, #28a745 0%, #34ce57 100%)',
                  color: 'white',
                  border: 'none',
                  borderRadius: 25,
                  fontSize: 16,
                  fontWeight: 'bold',
                  cursor: 'pointer'
                }}
              >
                🎥 Enable Camera & Microphone for Practice
              </button>
              <p style={{ marginTop: 10, fontSize: 14, color: '#6c757d' }}>
                Both camera and microphone are needed for face recognition and audio analysis
              </p>
            </div>
          )}

          {/* Camera Preview */}
          {!recordedVideoUrl && hasCamera && (
            <div style={{
              position: 'relative',
              width: '100%',
              maxWidth: 640,
              margin: '0 auto',
              background: '#2c3e50',
              borderRadius: 12,
              overflow: 'hidden',
              border: isRecording ? '3px solid #dc3545' : '3px solid #28a745'
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
                  background: '#dc3545',
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
                  RECORDING
                </div>
              )}
              
              {/* Face detection indicator */}
              <div style={{
                position: 'absolute',
                bottom: 15,
                left: 15,
                background: 'rgba(0,0,0,0.7)',
                color: 'white',
                padding: '6px 10px',
                borderRadius: 4,
                fontSize: 12
              }}>
                👤 Face Recognition Active
              </div>
              
              {/* Audio indicator */}
              <div style={{
                position: 'absolute',
                bottom: 15,
                right: 15,
                background: 'rgba(0,0,0,0.7)',
                color: 'white',
                padding: '6px 10px',
                borderRadius: 4,
                fontSize: 12
              }}>
                🎤 Audio Recognition Active
              </div>
            </div>
          )}

          {/* Recorded Video Preview */}
          {recordedVideoUrl && (
            <div style={{
              width: '100%',
              maxWidth: 640,
              margin: '0 auto',
              background: '#2c3e50',
              borderRadius: 12,
              overflow: 'hidden',
              border: '3px solid #28a745'
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
          <div style={{ 
            display: 'flex', 
            gap: 15, 
            flexWrap: 'wrap', 
            justifyContent: 'center',
            marginTop: 20
          }}>
            {!recordedVideoUrl && !isRecording && hasCamera && (
              <button
                onClick={startRecording}
                style={{
                  padding: '15px 30px',
                  background: 'linear-gradient(135deg, #dc3545 0%, #e74c3c 100%)',
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
                🎬 Start Practice Recording
              </button>
            )}

            {isRecording && (
              <button
                onClick={stopRecording}
                style={{
                  padding: '15px 30px',
                  background: '#2c3e50',
                  color: 'white',
                  border: '2px solid #dc3545',
                  borderRadius: 25,
                  fontSize: 16,
                  fontWeight: 'bold',
                  cursor: 'pointer'
                }}
              >
                ⏹️ Stop Recording
              </button>
            )}

            {recordedVideoUrl && (
              <>
                <button
                  onClick={analyzePracticeSpeaking}
                  disabled={isAnalyzing}
                  style={{
                    padding: '15px 30px',
                    background: isAnalyzing ? '#6c757d' : 'linear-gradient(135deg, #007bff 0%, #0056b3 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: 25,
                    fontSize: 16,
                    fontWeight: 'bold',
                    cursor: isAnalyzing ? 'not-allowed' : 'pointer'
                  }}
                >
                  {isAnalyzing ? '🔍 Analyzing Face & Voice...' : '🎯 Get AI Feedback'}
                </button>

                <button
                  onClick={discardRecording}
                  disabled={isAnalyzing}
                  style={{
                    padding: '15px 30px',
                    background: '#fd7e14',
                    color: 'white',
                    border: 'none',
                    borderRadius: 25,
                    fontSize: 16,
                    fontWeight: 'bold',
                    cursor: 'pointer'
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
                    background: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: 25,
                    fontSize: 16,
                    fontWeight: 'bold',
                    cursor: 'pointer'
                  }}
                >
                  🔄 Record Again
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {/* AI Analysis Information */}
      <div style={{
        background: '#f8f9fa',
        border: '1px solid #dee2e6',
        borderRadius: 8,
        padding: 20,
        marginTop: 30
      }}>
        <h4 style={{ color: '#495057', marginBottom: 15 }}>🤖 AI Analysis Features</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 15 }}>
          <div>
            <strong style={{ color: '#007bff' }}>👤 Face Recognition</strong>
            <ul style={{ fontSize: 14, marginTop: 5, paddingLeft: 20 }}>
              <li>Facial emotion detection</li>
              <li>Eye contact assessment</li>
              <li>Expression analysis</li>
              <li>Engagement measurement</li>
            </ul>
          </div>
          <div>
            <strong style={{ color: '#28a745' }}>🎤 Audio Recognition</strong>
            <ul style={{ fontSize: 14, marginTop: 5, paddingLeft: 20 }}>
              <li>Voice emotion analysis</li>
              <li>Speech clarity assessment</li>
              <li>Confidence detection</li>
              <li>Tone evaluation</li>
            </ul>
          </div>
          <div>
            <strong style={{ color: '#dc3545' }}>🔗 Multimodal Analysis</strong>
            <ul style={{ fontSize: 14, marginTop: 5, paddingLeft: 20 }}>
              <li>Combined face + voice analysis</li>
              <li>Consistency checking</li>
              <li>Overall performance score</li>
              <li>Personalized improvement tips</li>
            </ul>
          </div>
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
