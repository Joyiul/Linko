import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './ListeningPage.css';

export default function ListeningPage() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Complete end-to-end pipeline: Upload → Speech-to-Text → Analysis
  const handleUploadAndAnalyze = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const formData = new FormData();
      formData.append("file", file);
      
      // Call the complete pipeline endpoint
      const response = await axios.post("http://localhost:5001/upload-and-analyze", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const data = response.data;
      setTranscript(data.transcript);
      setResults({
        transcript: data.transcript,
        tone: data.analysis.tone,
        slang: data.analysis.slang,
        filename: data.filename
      });

      // Save results for analysis page
      localStorage.setItem("analysisResults", JSON.stringify({
        transcript: data.transcript,
        tone: data.analysis.tone,
        slang: data.analysis.slang,
        filename: data.filename
      }));
      
      // Navigate to results
      navigate("/analyze");
      
    } catch (err) {
      console.error("Error:", err);
      setError(err.response?.data?.error || "An error occurred processing your file");
    } finally {
      setLoading(false);
    }
  };

  // Legacy manual analysis (for when users want to type their own text)
  const handleManualAnalyze = async () => {
    if (!transcript.trim()) {
      setError("Please enter some text to analyze");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const res = await axios.post("http://localhost:5001/analyze", {
        transcript,
      });
      setResults(res.data);

      // Save results for analysis page
      localStorage.setItem("analysisResults", JSON.stringify({
        transcript: transcript,
        tone: res.data.tone,
        slang: res.data.slang
      }));
      navigate("/analyze");
      
    } catch (err) {
      console.error("Error:", err);
      setError("An error occurred analyzing your text");
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="listening-container">
    <h2 className="listening-title">Upload Audio for Analysis</h2>
    
    {error && <div className="error-message" style={{color: 'red', marginBottom: '10px'}}>{error}</div>}
    
    <div className="upload-area">
      <input
        type="file"
        className="upload-input"
        accept="audio/*,video/*,.wav,.mp3,.mp4,.avi,.mov,.flac,.m4a,.ogg"
        onChange={(e) => setFile(e.target.files[0])}
        disabled={loading}
      />
      {file && <p>Selected: {file.name}</p>}
      
      <button 
        className="record-btn" 
        onClick={handleUploadAndAnalyze}
        disabled={!file || loading}
        style={{
          backgroundColor: loading ? '#ccc' : '#007bff',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Processing...' : '🎤 Upload & Analyze Audio'}
      </button>
    </div>

    <div className="divider" style={{margin: '30px 0', textAlign: 'center'}}>
      <hr />
      <span style={{background: 'white', padding: '0 20px', color: '#666'}}>OR</span>
      <hr />
    </div>

    <h4>Manual Text Analysis</h4>
    <textarea
      rows="6"
      className="upload-input"
      placeholder="Type or paste text here for analysis..."
      value={transcript}
      onChange={(e) => setTranscript(e.target.value)}
      disabled={loading}
    />

    <button 
      className="action-btn" 
      onClick={handleManualAnalyze}
      disabled={loading || !transcript.trim()}
      style={{
        backgroundColor: loading ? '#ccc' : '#28a745',
        cursor: loading ? 'not-allowed' : 'pointer'
      }}
    >
      {loading ? 'Analyzing...' : '📝 Analyze Text'}
    </button>

    {transcript && (
      <div className="preview" style={{marginTop: '20px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '5px'}}>
        <h5>Current Transcript:</h5>
        <p>"{transcript}"</p>
      </div>
    )}
  </div>
);
}
