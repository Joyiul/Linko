import React, { useState } from 'react';
import './LearningLibraryPage.css';

export default function LearningLibraryPage() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedVideo, setSelectedVideo] = useState(null);

  const videoCategories = [
    { id: 'all', name: 'All Lessons', icon: '📚' },
    { id: 'tones', name: 'Tones & Emotions', icon: '🎭' },
    { id: 'slang', name: 'Slang & Expressions', icon: '💬' },
    { id: 'pronunciation', name: 'Pronunciation', icon: '🗣️' },
    { id: 'conversation', name: 'Conversation Skills', icon: '💭' },
    { id: 'workplace', name: 'Workplace English', icon: '💼' },
    { id: 'cultural', name: 'Cultural Context', icon: '🌍' }
  ];

  const videoLibrary = [
    {
      id: 1,
      title: "Understanding Sarcasm in English",
      description: "Learn to identify and use sarcasm appropriately in conversations. Master the subtle cues and context clues.",
      category: 'tones',
      duration: '8:32',
      level: 'Intermediate',
      thumbnail: '🎭',
      instructor: 'Sarah Chen',
      videoUrl: 'https://example.com/sarcasm-video',
      skills: ['Tone Recognition', 'Cultural Context', 'Social Cues'],
      views: '12.5K'
    },
    {
      id: 2,
      title: "Common American Slang Expressions",
      description: "Master popular slang terms used in everyday American conversations, from 'lit' to 'no cap'.",
      category: 'slang',
      duration: '12:45',
      level: 'Beginner',
      thumbnail: '💬',
      instructor: 'Mike Rodriguez',
      videoUrl: 'https://example.com/slang-video',
      skills: ['Vocabulary', 'Informal Language', 'Youth Culture'],
      views: '25.3K'
    },
    {
      id: 3,
      title: "Expressing Emotions Naturally",
      description: "Learn how to express different emotions in English with proper intonation, facial expressions, and body language.",
      category: 'tones',
      duration: '15:20',
      level: 'Intermediate',
      thumbnail: '😊',
      instructor: 'Emma Watson',
      videoUrl: 'https://example.com/emotions-video',
      skills: ['Emotional Expression', 'Intonation', 'Body Language'],
      views: '18.7K'
    },
    {
      id: 4,
      title: "Professional Email Communication",
      description: "Master the art of writing professional emails in workplace settings. Templates and examples included.",
      category: 'workplace',
      duration: '10:15',
      level: 'Advanced',
      thumbnail: '💼',
      instructor: 'David Kim',
      videoUrl: 'https://example.com/email-video',
      skills: ['Business Writing', 'Formal Language', 'Email Etiquette'],
      views: '8.9K'
    },
    {
      id: 5,
      title: "Pronunciation: TH Sounds Mastery",
      description: "Perfect your pronunciation of difficult 'th' sounds in English through targeted exercises and practice.",
      category: 'pronunciation',
      duration: '6:30',
      level: 'Beginner',
      thumbnail: '🗣️',
      instructor: 'Lisa Thompson',
      videoUrl: 'https://example.com/pronunciation-video',
      skills: ['Phonetics', 'Speech Training', 'Accent Reduction'],
      views: '33.1K'
    },
    {
      id: 6,
      title: "Small Talk & Social Conversations",
      description: "Build confidence in casual conversations and small talk situations. Perfect for networking and socializing.",
      category: 'conversation',
      duration: '14:22',
      level: 'Intermediate',
      thumbnail: '💭',
      instructor: 'Alex Johnson',
      videoUrl: 'https://example.com/smalltalk-video',
      skills: ['Social Skills', 'Conversation Starters', 'Cultural Awareness'],
      views: '21.4K'
    },
    {
      id: 7,
      title: "Understanding Passive-Aggressive Communication",
      description: "Recognize and respond to passive-aggressive communication styles in workplace and personal settings.",
      category: 'tones',
      duration: '11:18',
      level: 'Advanced',
      thumbnail: '😤',
      instructor: 'Dr. Rachel Green',
      videoUrl: 'https://example.com/passive-aggressive-video',
      skills: ['Communication Styles', 'Conflict Resolution', 'Workplace Dynamics'],
      views: '15.6K'
    },
    {
      id: 8,
      title: "Internet Slang & Text Speak",
      description: "Decode modern internet slang, abbreviations, and text messaging language used on social media.",
      category: 'slang',
      duration: '9:45',
      level: 'Beginner',
      thumbnail: '📱',
      instructor: 'Zoe Martinez',
      videoUrl: 'https://example.com/internet-slang-video',
      skills: ['Digital Communication', 'Abbreviations', 'Online Culture'],
      views: '29.8K'
    },
    {
      id: 9,
      title: "American vs British Cultural Context",
      description: "Understand the cultural differences in communication styles between American and British English.",
      category: 'cultural',
      duration: '13:55',
      level: 'Intermediate',
      thumbnail: '🌍',
      instructor: 'James Oxford',
      videoUrl: 'https://example.com/cultural-video',
      skills: ['Cultural Awareness', 'Regional Differences', 'Context Clues'],
      views: '11.2K'
    },
    {
      id: 10,
      title: "Confident Public Speaking",
      description: "Develop confidence and clarity in public speaking situations, from presentations to job interviews.",
      category: 'conversation',
      duration: '18:30',
      level: 'Advanced',
      thumbnail: '🎤',
      instructor: 'Maria Santos',
      videoUrl: 'https://example.com/public-speaking-video',
      skills: ['Public Speaking', 'Confidence Building', 'Presentation Skills'],
      views: '16.3K'
    },
    {
      id: 11,
      title: "Dealing with Difficult Customers",
      description: "Learn professional tone and language for handling challenging customer service situations.",
      category: 'workplace',
      duration: '12:08',
      level: 'Intermediate',
      thumbnail: '📞',
      instructor: 'Robert Wilson',
      videoUrl: 'https://example.com/customer-service-video',
      skills: ['Customer Service', 'Conflict Resolution', 'Professional Tone'],
      views: '9.7K'
    },
    {
      id: 12,
      title: "Vowel Sounds for Clear Speech",
      description: "Master English vowel sounds to improve your speaking clarity and reduce accent interference.",
      category: 'pronunciation',
      duration: '14:45',
      level: 'Beginner',
      thumbnail: '🔤',
      instructor: 'Jennifer Adams',
      videoUrl: 'https://example.com/vowels-video',
      skills: ['Vowel Pronunciation', 'Speech Clarity', 'Accent Training'],
      views: '27.4K'
    }
  ];

  const filteredVideos = selectedCategory === 'all' 
    ? videoLibrary 
    : videoLibrary.filter(video => video.category === selectedCategory);

  const openVideoModal = (video) => {
    setSelectedVideo(video);
  };

  const closeVideoModal = () => {
    setSelectedVideo(null);
  };

  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return '#28a745';
      case 'Intermediate': return '#ffc107';
      case 'Advanced': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div className="learning-library-container">
      <div className="library-header">
        <h2>Learning Library</h2>
        <p>Master English communication through expert-led video lessons</p>
        <div className="stats">
          <span>📊 {videoLibrary.length} Lessons</span>
          <span>👥 12 Expert Instructors</span>
          <span>⭐ 4.8 Average Rating</span>
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
                <div className="video-placeholder">
                  <span className="placeholder-icon">{selectedVideo.thumbnail}</span>
                  <div className="player-controls">
                    <button className="play-video-btn">
                      <span>▶</span> Start Lesson
                    </button>
                  </div>
                  <p className="video-note">Interactive Video Player</p>
                </div>
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
                  <button className="primary-btn">Start Learning</button>
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
