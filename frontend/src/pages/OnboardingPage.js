import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function OnboardingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: 40, textAlign: 'center' }}>
      <h1>Welcome</h1>
      <button onClick={() => navigate('/listen')}>Listener</button>
      <br /><br />
      <button onClick={() => navigate('/listen')}>Learner</button>
    </div>
  );
}
