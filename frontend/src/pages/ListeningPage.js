import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import VoiceRecorder from '../components/VoiceRecorder';
import './ListeningPage.css';

export default function ListeningPage() {
  const [file, setFile] = useState(null);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("upload"); // "upload", "record", or "text"
  const navigate = useNavigate();

  // Handle recorded audio from VoiceRecorder component
  const handleRecordingComplete = (blob) => {
    setRecordedBlob(blob);
    setFile(null); // Clear any uploaded file
    setError("");
  };

  // Main decipher function that handles both uploaded files and recorded audio
  const handleDecipher = async () => {
    const audioSource = file || recordedBlob;
    
    if (!audioSource && !transcript.trim()) {
      setError("Please provide audio or text to analyze");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      if (audioSource) {
        // Handle file upload or recorded audio
        const formData = new FormData();
        
        if (file) {
          formData.append("file", file);
        } else if (recordedBlob) {
          // Convert blob to file for upload
          const recordedFile = new File([recordedBlob], "recorded_audio.wav", {
            type: "audio/wav"
          });
          formData.append("file", recordedFile);
        }
        
        console.log("Processing audio...");
        
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
          filename: data.filename || (recordedBlob ? "Recorded Audio" : file?.name)
        });

        // Save results for analysis page
        const resultData = {
          transcript: data.transcript,
          tone: data.analysis.tone,
          slang: data.analysis.slang,
          filename: data.filename || (recordedBlob ? "Recorded Audio" : file?.name)
        };
        
        localStorage.setItem("analysisResults", JSON.stringify(resultData));
        console.log("Results saved to localStorage");
        
        // Navigate to results
        setTimeout(() => {
          navigate("/analyze");
        }, 100);
        
      } else if (transcript.trim()) {
        // Handle manual text analysis
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
        
        // Navigate to results
        setTimeout(() => {
          navigate("/analyze");
        }, 100);
      }
      
    } catch (err) {
      console.error("Decipher error:", err);
      let errorMessage = "An error occurred processing your request";
      
      if (err.code === 'ECONNABORTED') {
        errorMessage = "Request timed out. Please try with a smaller file or check your connection.";
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
      <h2 className="listening-title">Audio Analysis & Slang Detection</h2>
      
      {error && (
        <div className="error-message" style={{
          color: 'red', 
          marginBottom: '20px',
          padding: '15px',
          backgroundColor: '#ffe6e6',
          borderRadius: '8px',
          border: '1px solid #ff9999'
        }}>
          {error}
        </div>
      )}
      
      {/* Tab Navigation */}
      <div style={{ marginBottom: '30px' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: '10px',
          marginBottom: '20px',
          borderBottom: '2px solid #e9ecef'
        }}>
          <button
            onClick={() => setActiveTab("upload")}
            style={{
              padding: '12px 24px',
              backgroundColor: activeTab === "upload" ? '#007bff' : 'transparent',
              color: activeTab === "upload" ? 'white' : '#007bff',
              border: 'none',
              borderBottom: activeTab === "upload" ? '3px solid #007bff' : '3px solid transparent',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold'
            }}
          >
            Upload File
          </button>
          <button
            onClick={() => setActiveTab("record")}
            style={{
              padding: '12px 24px',
              backgroundColor: activeTab === "record" ? '#007bff' : 'transparent',
              color: activeTab === "record" ? 'white' : '#007bff',
              border: 'none',
              borderBottom: activeTab === "record" ? '3px solid #007bff' : '3px solid transparent',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold'
            }}
          >
            Record Audio
          </button>
          <button
            onClick={() => setActiveTab("text")}
            style={{
              padding: '12px 24px',
              backgroundColor: activeTab === "text" ? '#007bff' : 'transparent',
              color: activeTab === "text" ? 'white' : '#007bff',
              border: 'none',
              borderBottom: activeTab === "text" ? '3px solid #007bff' : '3px solid transparent',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold'
            }}
          >
            Enter Text
          </button>
        </div>
      </div>

      {/* Content Based on Active Tab */}
      <div style={{ minHeight: '200px', marginBottom: '30px' }}>
        {activeTab === "upload" && (
          <div className="upload-area" style={{ 
            textAlign: 'center', 
            padding: '40px', 
            border: '2px dashed #007bff', 
            borderRadius: '10px',
            backgroundColor: '#f8f9fa'
          }}>
            <h3>Upload Audio or Video File</h3>
            <p style={{ color: '#666', marginBottom: '20px' }}>
              Supports: WAV, MP3, MP4, AVI, MOV, FLAC, M4A, OGG
            </p>
            <input
              type="file"
              className="upload-input"
              accept="audio/*,video/*,.wav,.mp3,.mp4,.avi,.mov,.flac,.m4a,.ogg"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setRecordedBlob(null); // Clear any recorded audio
                setError("");
              }}
              disabled={loading}
              style={{
                marginBottom: '15px',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '5px',
                fontSize: '16px'
              }}
            />
            {file && (
              <div style={{ 
                marginTop: '15px', 
                padding: '10px', 
                backgroundColor: '#d4edda', 
                borderRadius: '5px',
                color: '#155724'
              }}>
                Selected: {file.name}
              </div>
            )}
          </div>
        )}

        {activeTab === "record" && (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px', 
            border: '2px solid #dc3545', 
            borderRadius: '10px',
            backgroundColor: '#fff5f5'
          }}>
            <h3>Record Your Voice</h3>
            <p style={{ color: '#666', marginBottom: '20px' }}>
              Click the button below to start recording audio
            </p>
            <VoiceRecorder onRecordingComplete={handleRecordingComplete} />
          </div>
        )}

        {activeTab === "text" && (
          <div style={{ 
            padding: '20px', 
            border: '2px solid #28a745', 
            borderRadius: '10px',
            backgroundColor: '#f8fff8'
          }}>
            <h3>Enter Text for Analysis</h3>
            <textarea
              rows="6"
              className="upload-input"
              placeholder="Type or paste your text here for slang detection and tone analysis..."
              value={transcript}
              onChange={(e) => {
                setTranscript(e.target.value);
                setFile(null);
                setRecordedBlob(null);
                setError("");
              }}
              disabled={loading}
              style={{
                width: '100%',
                padding: '15px',
                border: '1px solid #28a745',
                borderRadius: '8px',
                fontSize: '16px',
                fontFamily: 'inherit',
                resize: 'vertical'
              }}
            />
          </div>
        )}
      </div>

      {/* Main Decipher Button */}
      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <button 
          onClick={handleDecipher}
          disabled={loading || (!file && !recordedBlob && !transcript.trim())}
          style={{
            padding: '20px 40px',
            backgroundColor: loading ? '#6c757d' : '#ff6b35',
            color: 'white',
            border: 'none',
            borderRadius: '50px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '20px',
            fontWeight: 'bold',
            boxShadow: '0 4px 15px rgba(255, 107, 53, 0.3)',
            transform: loading ? 'none' : 'scale(1)',
            transition: 'all 0.3s ease'
          }}
          onMouseOver={(e) => {
            if (!loading) {
              e.target.style.transform = 'scale(1.05)';
              e.target.style.boxShadow = '0 6px 20px rgba(255, 107, 53, 0.4)';
            }
          }}
          onMouseOut={(e) => {
            if (!loading) {
              e.target.style.transform = 'scale(1)';
              e.target.style.boxShadow = '0 4px 15px rgba(255, 107, 53, 0.3)';
            }
          }}
        >
          {loading ? 'Deciphering...' : 'DECIPHER'}
        </button>
        
        {loading && (
          <div style={{ 
            marginTop: '15px', 
            color: '#007bff',
            fontSize: '16px',
            fontWeight: 'bold'
          }}>
            Processing your {file ? 'file' : recordedBlob ? 'recording' : 'text'}... Please wait.
          </div>
        )}
      </div>

      {/* Current Preview */}
      {transcript && activeTab === "text" && (
        <div style={{
          marginTop: '30px', 
          padding: '20px', 
          backgroundColor: '#e9ecef', 
          borderRadius: '8px',
          border: '1px solid #adb5bd'
        }}>
          <h5 style={{ marginBottom: '10px', color: '#495057' }}>Current Text:</h5>
          <p style={{ 
            fontStyle: 'italic', 
            color: '#6c757d',
            lineHeight: '1.5',
            margin: 0
          }}>
            "{transcript}"
          </p>
        </div>
      )}
    </div>
  );
}
