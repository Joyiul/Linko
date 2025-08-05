import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import OnboardingPage from './pages/OnboardingPage';
import ListeningPage from './pages/ListeningPage';
import AnalysisPage from './pages/AnalysisPage';
import VideoPage from './pages/VideoPage';

function FrontPage() {
  return <h1>This is the front page</h1>;
}

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link> | 
      <Link to="/onboarding">Onboarding</Link> | 
      <Link to="/listen">Listen</Link> | 
      <Link to="/analyze">Analyze</Link> | 
      <Link to="/videos">Videos</Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/listen" element={<ListeningPage />} />
        <Route path="/analyze" element={<AnalysisPage />} />
        <Route path="/videos" element={<VideoPage />} />
        <Route path="/" element={<FrontPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
