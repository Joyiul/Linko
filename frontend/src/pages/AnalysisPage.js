import React, { useEffect, useState } from 'react';
import EmojiToneBar from '../components/EmojiToneBar';
import HighlightedText from '../components/HighlightedText';
import './AnalysisPage.css';

export default function AnalysisPage() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem("analysisResults");
    if (stored) setResults(JSON.parse(stored));
  }, []);

  if (!results) return <p>Loading analysis...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h2>Analysis Results</h2>
      <EmojiToneBar tone={results.tone || "😐 Neutral"} />

      <h4>Transcript with Highlights:</h4>
      <HighlightedText text={results.transcript || "No transcript found."} />

      <h4>Slang Definitions</h4>
      <ul>
        {Object.entries(results.slang || {}).map(([word, meaning]) => (
          <li key={word}><strong>{word}</strong>: {meaning}</li>
        ))}
      </ul>
    </div>
  );
}
