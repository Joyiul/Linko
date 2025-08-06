import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/OnboardingPage';
import ListeningPage from './pages/ListeningPage';
import AnalysisPage from './pages/AnalysisPage';
import VideoPage from './pages/VideoPage';
import ChatPage from './pages/ChatPage';
import LearningLibraryPage from './pages/LearningLibraryPage';
import EmotionAccuracyDemo from './components/EmotionAccuracyDemo';
import Logo from './components/Logo';
import LinkoLogo from './components/LinkoLogo';
import { theme } from './theme';

function Navbar() {
  return (
    <nav style={{
      background: theme.colors.heroGradient,
      padding: '15px 0',
      boxShadow: theme.shadows.medium,
      borderBottom: `2px solid ${theme.colors.primaryDark}`
    }}>
      <div style={{ 
        maxWidth: 1200, 
        margin: '0 auto', 
        display: 'flex', 
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 20px'
      }}>
        {/* Logo Section - Your uploaded Linko logo */}
        <Link to="/" style={{ textDecoration: 'none' }}>
          <img 
            src="/CC753331-5C2B-4868-98C6-ABBD4196200E.png" 
            alt="Linko Logo" 
            style={{ 
              height: '40px',
              width: 'auto',
              filter: 'drop-shadow(1px 1px 2px rgba(0,0,0,0.2))'
            }} 
          />
        </Link>
        
        {/* Navigation Links */}
        <div style={{ display: 'flex', gap: 30 }}>
          <Link 
            to="/" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            Home
          </Link>
          <Link 
            to="/listen" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            Listen & Learn
          </Link>
          <Link 
            to="/videos" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            Practice Speaking
          </Link>
          <Link 
            to="/analyze" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            View Results
          </Link>
          <Link 
            to="/learning-library" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            Learning Library
          </Link>
          <Link 
            to="/emotion-demo" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            Emotion Demo
          </Link>
          <Link 
            to="/chat" 
            style={{ 
              color: theme.colors.onBackground, 
              textDecoration: 'none', 
              fontWeight: 'bold',
              padding: '8px 16px',
              borderRadius: theme.borderRadius.large,
              transition: 'all 0.3s ease',
              fontSize: theme.typography.button.fontSize
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.target.style.background = 'transparent'}
          >
            AI Chat
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  useEffect(() => {
    // Apply global styles to body
    document.body.style.fontFamily = theme.typography.fontFamily;
    document.body.style.backgroundColor = theme.colors.background;
    document.body.style.color = theme.colors.onBackground;
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    
    // Global error handlers
    const handleUnhandledRejection = (event) => {
      console.error('Unhandled promise rejection:', event.reason);
      console.error('Promise:', event.promise);
      // Prevent the default behavior (which would log to console)
      event.preventDefault();
    };

    const handleError = (event) => {
      console.error('Global error caught:', event.error);
    };

    // Add event listeners
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    window.addEventListener('error', handleError);

    // Cleanup
    return () => {
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
      window.removeEventListener('error', handleError);
    };
  }, []);

  return (
    <div style={{ 
      minHeight: '100vh',
      background: theme.colors.backgroundGradient
    }}>
      <BrowserRouter>
        <Navbar />
        <main style={{ 
          minHeight: 'calc(100vh - 80px)',
          padding: theme.spacing.md
        }}>
          <Routes>
            <Route path="/listen" element={<ListeningPage />} />
            <Route path="/analyze" element={<AnalysisPage />} />
            <Route path="/videos" element={<VideoPage />} />
            <Route path="/learning-library" element={<LearningLibraryPage />} />
            <Route path="/emotion-demo" element={<EmotionAccuracyDemo />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/" element={<HomePage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
