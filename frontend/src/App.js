import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ListeningPage from './pages/ListeningPage';
import AnalysisPage from './pages/AnalysisPage';
import VideoPage from './pages/VideoPage';
import Logo from './components/Logo';
import { theme } from './theme';
// import ChatPage from './pages/ChatPage';

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
        {/* Logo Section - Just the earth icon */}
        <Link to="/" style={{ textDecoration: 'none' }}>
          <Logo size="medium" showText={false} />
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
            <Route path="/" element={<HomePage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
