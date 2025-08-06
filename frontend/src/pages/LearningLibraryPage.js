import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { theme } from '../theme';

export default function LearningLibraryPage() {
  const [videos, setVideos] = useState([]);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadData, setUploadData] = useState({
    title: '',
    description: '',
    emotion: '',
    difficulty: 'beginner',
    language: 'english',
    speaker_info: ''
  });
  const [isUploading, setIsUploading] = useState(false);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const emotions = [
    'happy', 'sad', 'angry', 'neutral', 'excited', 
    'calm', 'frustrated', 'confident', 'nervous', 'surprised'
  ];

  const difficulties = [
    { value: 'beginner', label: 'Beginner - Clear and slow' },
    { value: 'intermediate', label: 'Intermediate - Normal pace' },
    { value: 'advanced', label: 'Advanced - Fast or complex' }
  ];

  // Mock data for now - in real app this would come from backend
  useEffect(() => {
    setVideos([
      {
        id: 1,
        title: 'Happy Conversation Example',
        description: 'A cheerful conversation between friends',
        emotion: 'happy',
        difficulty: 'beginner',
        language: 'english',
        speaker_info: 'Native English speaker from California',
        thumbnail: null,
        duration: '2:34'
      },
      {
        id: 2,
        title: 'Professional Meeting Tone',
        description: 'How to speak in business meetings',
        emotion: 'confident',
        difficulty: 'intermediate',
        language: 'english',
        speaker_info: 'Business professional, 10+ years experience',
        thumbnail: null,
        duration: '4:12'
      }
    ]);
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadFile(file);
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('title', uploadData.title);
    formData.append('description', uploadData.description);
    formData.append('emotion', uploadData.emotion);
    formData.append('difficulty', uploadData.difficulty);
    formData.append('language', uploadData.language);
    formData.append('speaker_info', uploadData.speaker_info);

    try {
      const response = await axios.post('http://localhost:5001/learning-library/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Add to local state for now
      const newVideo = {
        id: Date.now(),
        ...uploadData,
        thumbnail: null,
        duration: 'Processing...'
      };
      setVideos(prev => [newVideo, ...prev]);
      
      // Reset form
      setUploadFile(null);
      setUploadData({
        title: '',
        description: '',
        emotion: '',
        difficulty: 'beginner',
        language: 'english',
        speaker_info: ''
      });
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 3000);

    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const analyzeVideo = async (video) => {
    setSelectedVideo(video);
    setIsAnalyzing(true);
    
    try {
      // Mock analysis for now - in real app would send video to backend
      setTimeout(() => {
        setAnalysis({
          emotion_detected: video.emotion,
          confidence: 0.85,
          tone_characteristics: {
            pitch_variation: 'moderate',
            speaking_pace: 'normal',
            volume_consistency: 'good',
            clarity: 'excellent'
          },
          learning_points: [
            `This speaker demonstrates ${video.emotion} emotion effectively`,
            'Notice the natural pace and clear pronunciation',
            'Pay attention to the facial expressions and body language',
            'Try to match this tone when practicing similar conversations'
          ]
        });
        setIsAnalyzing(false);
      }, 2000);
    } catch (error) {
      console.error('Analysis failed:', error);
      setIsAnalyzing(false);
    }
  };

  return (
    <div style={{
      background: theme.colors.backgroundGradient,
      minHeight: '100vh',
      padding: theme.spacing.lg,
      color: theme.colors.onBackground
    }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: theme.spacing.xxl }}>
          <h1 style={{ 
            fontSize: theme.typography.h1.fontSize,
            marginBottom: theme.spacing.md,
            color: theme.colors.primary
          }}>
            Learning Library
          </h1>
          <p style={{ 
            fontSize: theme.typography.body1.fontSize,
            color: theme.colors.onSurfaceVariant,
            maxWidth: 600,
            margin: '0 auto'
          }}>
            Watch examples of different speaking tones and emotions to improve your communication skills. 
            Contributors can also upload videos to help others learn.
          </p>
        </div>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
          gap: theme.spacing.xl 
        }}>
          {/* Upload Section */}
          <div style={{
            background: theme.colors.surface,
            borderRadius: theme.borderRadius.large,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.medium,
            border: `2px solid ${theme.colors.accent}`
          }}>
            <h2 style={{ 
              color: theme.colors.accent, 
              marginBottom: theme.spacing.lg,
              fontSize: theme.typography.h2.fontSize
            }}>
              Contribute a Video
            </h2>

            {uploadSuccess && (
              <div style={{
                background: '#d4edda',
                color: '#155724',
                padding: theme.spacing.md,
                borderRadius: theme.borderRadius.medium,
                marginBottom: theme.spacing.md,
                border: '1px solid #c3e6cb'
              }}>
                Video uploaded successfully! Thank you for contributing.
              </div>
            )}

            <form onSubmit={handleUploadSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              <div>
                <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                  Video File *
                </label>
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileSelect}
                  required
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    borderRadius: theme.borderRadius.medium,
                    border: `1px solid ${theme.colors.surfaceVariant}`,
                    fontSize: theme.typography.body1.fontSize
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                  Title *
                </label>
                <input
                  type="text"
                  value={uploadData.title}
                  onChange={(e) => setUploadData({...uploadData, title: e.target.value})}
                  placeholder="e.g., Friendly Customer Service Example"
                  required
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    borderRadius: theme.borderRadius.medium,
                    border: `1px solid ${theme.colors.surfaceVariant}`,
                    fontSize: theme.typography.body1.fontSize
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                  Description
                </label>
                <textarea
                  value={uploadData.description}
                  onChange={(e) => setUploadData({...uploadData, description: e.target.value})}
                  placeholder="Describe the context and what learners can gain from this example"
                  rows={3}
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    borderRadius: theme.borderRadius.medium,
                    border: `1px solid ${theme.colors.surfaceVariant}`,
                    fontSize: theme.typography.body1.fontSize,
                    resize: 'vertical'
                  }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: theme.spacing.md }}>
                <div>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                    Primary Emotion *
                  </label>
                  <select
                    value={uploadData.emotion}
                    onChange={(e) => setUploadData({...uploadData, emotion: e.target.value})}
                    required
                    style={{
                      width: '100%',
                      padding: theme.spacing.md,
                      borderRadius: theme.borderRadius.medium,
                      border: `1px solid ${theme.colors.surfaceVariant}`,
                      fontSize: theme.typography.body1.fontSize
                    }}
                  >
                    <option value="">Select emotion</option>
                    {emotions.map(emotion => (
                      <option key={emotion} value={emotion}>
                        {emotion.charAt(0).toUpperCase() + emotion.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                    Difficulty Level
                  </label>
                  <select
                    value={uploadData.difficulty}
                    onChange={(e) => setUploadData({...uploadData, difficulty: e.target.value})}
                    style={{
                      width: '100%',
                      padding: theme.spacing.md,
                      borderRadius: theme.borderRadius.medium,
                      border: `1px solid ${theme.colors.surfaceVariant}`,
                      fontSize: theme.typography.body1.fontSize
                    }}
                  >
                    {difficulties.map(diff => (
                      <option key={diff.value} value={diff.value}>
                        {diff.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: theme.spacing.sm, fontWeight: 'bold' }}>
                  Speaker Information
                </label>
                <input
                  type="text"
                  value={uploadData.speaker_info}
                  onChange={(e) => setUploadData({...uploadData, speaker_info: e.target.value})}
                  placeholder="e.g., Native English speaker, professional background"
                  style={{
                    width: '100%',
                    padding: theme.spacing.md,
                    borderRadius: theme.borderRadius.medium,
                    border: `1px solid ${theme.colors.surfaceVariant}`,
                    fontSize: theme.typography.body1.fontSize
                  }}
                />
              </div>

              <button
                type="submit"
                disabled={isUploading || !uploadFile}
                style={{
                  padding: theme.spacing.lg,
                  background: isUploading || !uploadFile ? theme.colors.surfaceVariant : theme.colors.accent,
                  color: theme.colors.onAccent,
                  border: 'none',
                  borderRadius: theme.borderRadius.medium,
                  fontSize: theme.typography.button.fontSize,
                  fontWeight: 'bold',
                  cursor: isUploading || !uploadFile ? 'not-allowed' : 'pointer',
                  transition: 'all 0.3s ease'
                }}
              >
                {isUploading ? 'Uploading...' : 'Upload Video'}
              </button>
            </form>
          </div>

          {/* Video Library */}
          <div style={{
            background: theme.colors.surface,
            borderRadius: theme.borderRadius.large,
            padding: theme.spacing.xl,
            boxShadow: theme.shadows.medium,
            border: `2px solid ${theme.colors.primary}`
          }}>
            <h2 style={{ 
              color: theme.colors.primary, 
              marginBottom: theme.spacing.lg,
              fontSize: theme.typography.h2.fontSize
            }}>
              Learning Examples
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              {videos.map(video => (
                <div
                  key={video.id}
                  style={{
                    background: theme.colors.backgroundGradient,
                    borderRadius: theme.borderRadius.medium,
                    padding: theme.spacing.lg,
                    border: `1px solid ${theme.colors.surfaceVariant}`,
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                  onClick={() => analyzeVideo(video)}
                  onMouseEnter={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = theme.shadows.medium;
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: theme.spacing.sm }}>
                    <h3 style={{ margin: 0, color: theme.colors.accent, fontSize: theme.typography.h3.fontSize }}>
                      {video.title}
                    </h3>
                    <span style={{ 
                      background: theme.colors.primary, 
                      color: theme.colors.onPrimary,
                      padding: '4px 8px',
                      borderRadius: theme.borderRadius.small,
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}>
                      {video.emotion.toUpperCase()}
                    </span>
                  </div>
                  
                  <p style={{ 
                    margin: `${theme.spacing.sm}px 0`, 
                    color: theme.colors.onSurfaceVariant,
                    fontSize: theme.typography.body2.fontSize 
                  }}>
                    {video.description}
                  </p>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: theme.colors.onSurfaceVariant }}>
                    <span>Level: {video.difficulty}</span>
                    <span>Duration: {video.duration}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Analysis Modal */}
        {selectedVideo && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'rgba(0,0,0,0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <div style={{
              background: theme.colors.surface,
              borderRadius: theme.borderRadius.large,
              padding: theme.spacing.xl,
              maxWidth: 600,
              width: '90%',
              maxHeight: '80%',
              overflow: 'auto'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: theme.spacing.lg }}>
                <h2 style={{ margin: 0, color: theme.colors.primary }}>
                  {selectedVideo.title}
                </h2>
                <button
                  onClick={() => {
                    setSelectedVideo(null);
                    setAnalysis(null);
                  }}
                  style={{
                    background: 'none',
                    border: 'none',
                    fontSize: '24px',
                    cursor: 'pointer',
                    color: theme.colors.onSurface
                  }}
                >
                  ×
                </button>
              </div>

              {/* Mock Video Player */}
              <div style={{
                width: '100%',
                height: 200,
                background: '#000',
                borderRadius: theme.borderRadius.medium,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: theme.spacing.lg,
                color: '#fff'
              }}>
                🎥 Video Player Placeholder
              </div>

              {isAnalyzing ? (
                <div style={{ textAlign: 'center', padding: theme.spacing.xl }}>
                  <div style={{ fontSize: '24px', marginBottom: theme.spacing.md }}>🔍</div>
                  <p>Analyzing video for tone and emotion patterns...</p>
                </div>
              ) : analysis ? (
                <div>
                  <h3 style={{ color: theme.colors.accent, marginBottom: theme.spacing.lg }}>
                    Analysis Results
                  </h3>
                  
                  <div style={{ marginBottom: theme.spacing.lg }}>
                    <h4 style={{ color: theme.colors.primary }}>Detected Emotion</h4>
                    <p style={{ 
                      background: theme.colors.primaryLight, 
                      padding: theme.spacing.md, 
                      borderRadius: theme.borderRadius.medium 
                    }}>
                      <strong>{analysis.emotion_detected.toUpperCase()}</strong> 
                      ({Math.round(analysis.confidence * 100)}% confidence)
                    </p>
                  </div>

                  <div style={{ marginBottom: theme.spacing.lg }}>
                    <h4 style={{ color: theme.colors.primary }}>Tone Characteristics</h4>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: theme.spacing.sm }}>
                      {Object.entries(analysis.tone_characteristics).map(([key, value]) => (
                        <div key={key} style={{ 
                          background: theme.colors.backgroundGradient, 
                          padding: theme.spacing.sm, 
                          borderRadius: theme.borderRadius.small 
                        }}>
                          <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {value}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 style={{ color: theme.colors.primary }}>Learning Points</h4>
                    <ul style={{ paddingLeft: theme.spacing.lg }}>
                      {analysis.learning_points.map((point, index) => (
                        <li key={index} style={{ marginBottom: theme.spacing.sm }}>
                          {point}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: theme.spacing.xl }}>
                  <button
                    onClick={() => analyzeVideo(selectedVideo)}
                    style={{
                      padding: theme.spacing.lg,
                      background: theme.colors.primary,
                      color: theme.colors.onPrimary,
                      border: 'none',
                      borderRadius: theme.borderRadius.medium,
                      fontSize: theme.typography.button.fontSize,
                      fontWeight: 'bold',
                      cursor: 'pointer'
                    }}
                  >
                    Analyze This Video
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
