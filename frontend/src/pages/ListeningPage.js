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
      
      console.log("Uploading file:", file.name);
      
      // Call the complete pipeline endpoint
      const response = await axios.post("http://localhost:5001/upload-and-analyze", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 second timeout
      });
      
      console.log("Response received:", response.status);
      
      if (!response.data) {
        throw new Error("Empty response from server");
      }
      
      const data = response.data;
      
      // Validate response structure
      if (!data.transcript || !data.analysis) {
        throw new Error("Invalid response structure from server");
      }
      
      setTranscript(data.transcript);
      setResults({
        transcript: data.transcript,
        tone: data.analysis.tone,
        slang: data.analysis.slang,
        filename: data.filename
      });

      // Save results for analysis page
      const resultData = {
        transcript: data.transcript,
        tone: data.analysis.tone,
        slang: data.analysis.slang,
        filename: data.filename
      };
      
      localStorage.setItem("analysisResults", JSON.stringify(resultData));
      console.log("Results saved to localStorage");
      
      // Small delay before navigation to ensure state is set
      setTimeout(() => {
        navigate("/analyze");
      }, 100);
      
    } catch (err) {
      console.error("Upload and analyze error:", err);
      let errorMessage = "An error occurred processing your file";
      
      if (err.code === 'ECONNABORTED') {
        errorMessage = "Request timed out. Please try with a smaller file.";
      } else if (err.response) {
        errorMessage = err.response.data?.error || `Server error: ${err.response.status}`;
      } else if (err.request) {
        errorMessage = "Cannot connect to server. Please check if the backend is running.";
      } else {
        errorMessage = err.message || errorMessage;
      }
      
      setError(errorMessage);
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
      console.log("Analyzing text:", transcript.substring(0, 50) + "...");
      
      const res = await axios.post("http://localhost:5001/analyze", {
        transcript,
      }, {
        timeout: 30000, // 30 second timeout
      });
      
      console.log("Analysis response received:", res.status);
      
      if (!res.data) {
        throw new Error("Empty response from server");
      }
      
      setResults(res.data);

      // Save results for analysis page
      const resultData = {
        transcript: transcript,
        tone: res.data.tone,
        slang: res.data.slang
      };
      
      localStorage.setItem("analysisResults", JSON.stringify(resultData));
      console.log("Manual analysis results saved to localStorage");
      
      // Small delay before navigation
      setTimeout(() => {
        navigate("/analyze");
      }, 100);
      
    } catch (err) {
      console.error("Manual analyze error:", err);
      let errorMessage = "An error occurred analyzing your text";
      
      if (err.code === 'ECONNABORTED') {
        errorMessage = "Request timed out. Please try again.";
      } else if (err.response) {
        errorMessage = err.response.data?.error || `Server error: ${err.response.status}`;
      } else if (err.request) {
        errorMessage = "Cannot connect to server. Please check if the backend is running.";
      } else {
        errorMessage = err.message || errorMessage;
      }
      
      setError(errorMessage);
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
