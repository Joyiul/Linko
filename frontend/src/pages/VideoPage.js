import React from 'react';
import VoiceRecorder from '../components/VoiceRecorder';

export default function VideoPage() {
  return (
    <div style={{ padding: 20 }}>
      <h2>Examples</h2>
      <video controls src="/sample-clip.mp4" width="100%" />
      <br /><br />
      <VoiceRecorder />
    </div>
  );
}
