import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './LearningLibraryPage.css';

export default function LearningLibraryPage() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Add error boundary for this component
  useEffect(() => {
    const handleError = (event) => {
      console.error('LearningLibraryPage error:', event.error);
      setError('An unexpected error occurred in the Learning Library');
    };

    const handleUnhandledRejection = (event) => {
      console.error('LearningLibraryPage unhandled promise rejection:', event.reason);
      setError('A network error occurred. Please refresh the page.');
      event.preventDefault();
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  // Load videos from backend on component mount
  useEffect(() => {
    loadVideos().catch(error => {
      console.error('Failed to load videos in useEffect:', error);
      setError('Failed to initialize video library');
      setLoading(false);
    });
  }, []);

  const loadVideos = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get('http://localhost:5002/learning-library/videos', {
        timeout: 10000, // 10 second timeout
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.data && response.data.videos) {
        setVideos(response.data.videos);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Error loading videos:', err);
      let errorMessage = 'Failed to load videos. Please try again.';
      
      if (err.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. Please check your connection.';
      } else if (err.response) {
        errorMessage = `Server error: ${err.response.status}`;
      } else if (err.request) {
        errorMessage = 'Cannot connect to server. Make sure the backend is running.';
      }
      
      setError(errorMessage);
      setVideos([]); // Clear videos on error
    } finally {
      setLoading(false);
    }
  };

  const videoCategories = [
    { id: 'all', name: 'All Lessons', icon: '📚' },
    { id: 'tones', name: 'Tones & Emotions', icon: '🎭' },
    { id: 'slang', name: 'Slang & Expressions', icon: '💬' },
    { id: 'pronunciation', name: 'Pronunciation', icon: '🗣️' },
    { id: 'conversation', name: 'Conversation Skills', icon: '💭' },
    { id: 'workplace', name: 'Workplace English', icon: '💼' },
    { id: 'cultural', name: 'Cultural Context', icon: '🌍' }
  ];

  const filteredVideos = selectedCategory === 'all' 
    ? videos 
    : videos.filter(video => video.category === selectedCategory);

  const openVideoModal = (video) => {
    setSelectedVideo(video);
  };

  const closeVideoModal = () => {
    setSelectedVideo(null);
  };

  const getLevelColor = (level) => {
    switch(level?.toLowerCase()) {
      case 'beginner': return '#28a745';
      case 'intermediate': return '#ffc107';
      case 'advanced': return '#dc3545';
      default: return '#6c757d';
    }
  };

  if (loading) {
    return (
      <div className="learning-library-container">
        <div className="loading-state">
          <h2>Loading Learning Library...</h2>
          <p>Getting the latest educational videos for you</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="learning-library-container">
        <div className="error-state">
          <h2>Error Loading Videos</h2>
          <p>{error}</p>
          <button onClick={loadVideos} className="retry-btn">Try Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-library-container">
      <div className="library-header">
        <h2>Learning Library</h2>
        <p>Master English communication through expert-led video lessons</p>
        <div className="stats">
          <span>📊 {videos.length} Lessons</span>
          <span>👥 Expert Instructors</span>
          <span>⭐ Real Educational Content</span>
          <span>🎥 Interactive Videos</span>
        </div>
      </div>

      {/* Category Filter */}
      <div className="category-filter">
        {videoCategories.map(category => (
          <button
            key={category.id}
            className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(category.id)}
          >
            <span className="category-icon">{category.icon}</span>
            <span className="category-name">{category.name}</span>
          </button>
        ))}
      </div>

      {/* Results Summary */}
      <div className="results-summary">
        <p>Showing {filteredVideos.length} lesson{filteredVideos.length !== 1 ? 's' : ''} 
        {selectedCategory !== 'all' && ` in ${videoCategories.find(cat => cat.id === selectedCategory)?.name}`}
        </p>
      </div>

      {/* Video Grid */}
      <div className="video-grid">
        {filteredVideos.map(video => (
          <div key={video.id} className="video-card" onClick={() => openVideoModal(video)}>
            <div className="video-thumbnail">
              <span className="thumbnail-icon">{video.thumbnail}</span>
              <div className="video-duration">{video.duration}</div>
              <div className="play-button">▶</div>
              <div className="video-overlay">
                <span className="views">👁 {video.views} views</span>
              </div>
            </div>
            <div className="video-info">
              <h3 className="video-title">{video.title}</h3>
              <p className="video-instructor">by {video.instructor}</p>
              <p className="video-description">{video.description}</p>
              <div className="video-meta">
                <span 
                  className="video-level" 
                  style={{ backgroundColor: getLevelColor(video.level) }}
                >
                  {video.level}
                </span>
                <div className="video-skills">
                  {video.skills.slice(0, 2).map(skill => (
                    <span key={skill} className="skill-tag">{skill}</span>
                  ))}
                  {video.skills.length > 2 && (
                    <span className="skill-tag more">+{video.skills.length - 2}</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Video Modal */}
      {selectedVideo && (
        <div className="video-modal-overlay" onClick={closeVideoModal}>
          <div className="video-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title-section">
                <h3>{selectedVideo.title}</h3>
                <p className="modal-instructor">by {selectedVideo.instructor}</p>
              </div>
              <button className="close-btn" onClick={closeVideoModal}>×</button>
            </div>
            <div className="modal-content">
              <div className="video-player">
                {selectedVideo.real_video && selectedVideo.videoUrl ? (
                  <div>
                    <iframe
                      width="100%"
                      height="400"
                      src={selectedVideo.videoUrl}
                      title={selectedVideo.title}
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      style={{ borderRadius: '8px' }}
                      onError={() => console.log('Video failed to load')}
                    ></iframe>
                    <div style={{ marginTop: '10px', textAlign: 'center' }}>
                      <a 
                        href={selectedVideo.videoUrl.replace('/embed/', '/watch?v=')} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ 
                          color: '#007bff', 
                          textDecoration: 'none',
                          fontSize: '14px'
                        }}
                      >
                        🔗 Open video in YouTube →
                      </a>
                    </div>
                  </div>
                ) : (
                  <div className="video-placeholder">
                    <span className="placeholder-icon">{selectedVideo.thumbnail}</span>
                    <div className="player-controls">
                      <button className="play-video-btn">
                        <span>▶</span> Start Lesson
                      </button>
                    </div>
                    <p className="video-note">
                      {selectedVideo.real_video ? 'Loading Video Player...' : 'Interactive Video Player'}
                    </p>
                  </div>
                )}
              </div>
              <div className="video-details">
                <div className="video-stats-row">
                  <div className="stat-item">
                    <span className="stat-label">Duration:</span>
                    <span className="stat-value">{selectedVideo.duration}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Views:</span>
                    <span className="stat-value">{selectedVideo.views}</span>
                  </div>
                  <div className="stat-item">
                    <span 
                      className="level-badge"
                      style={{ backgroundColor: getLevelColor(selectedVideo.level) }}
                    >
                      {selectedVideo.level}
                    </span>
                  </div>
                </div>
                
                <div className="description-section">
                  <h4>About this lesson:</h4>
                  <p className="video-description-full">{selectedVideo.description}</p>
                </div>
                
                <div className="skills-section">
                  <h4>What you'll learn:</h4>
                  <div className="skills-list">
                    {selectedVideo.skills.map(skill => (
                      <span key={skill} className="skill-badge">{skill}</span>
                    ))}
                  </div>
                </div>
                
                <div className="action-buttons">
                  <button 
                    className="primary-btn"
                    onClick={() => {
                      if (selectedVideo.real_video && selectedVideo.videoUrl) {
                        // Video is already playing in iframe
                        closeVideoModal();
                      } else {
                        alert('This video will be available soon!');
                      }
                    }}
                  >
                    {selectedVideo.real_video ? 'Close Video' : 'Coming Soon'}
                  </button>
                  <button className="secondary-btn">Save for Later</button>
                  <button className="secondary-btn">Share Lesson</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
