import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import VoiceRecorder from '../components/VoiceRecorder';
import { theme } from '../theme';

export default function ListeningPage() {
  const [file, setFile] = useState(null);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("upload"); // "upload", "record", or "text"
  const [previewAnalysis, setPreviewAnalysis] = useState(null); // New state for real-time analysis
  const [previewLoading, setPreviewLoading] = useState(false);
  const navigate = useNavigate();

  // Handle recorded audio from VoiceRecorder component
  const handleRecordingComplete = (blob) => {
    setRecordedBlob(blob);
    setFile(null); // Clear any uploaded file
    setError("");
  };

  // Real-time text analysis for preview
  const analyzeTextPreview = async (text) => {
    if (!text.trim() || text.length < 3) {
      setPreviewAnalysis(null);
      return;
    }

    setPreviewLoading(true);
    try {
      // Call comprehensive slang analysis
      const slangResponse = await axios.post("http://localhost:5002/analyze-comprehensive-slang", {
        text: text
      });

      // Call formality analysis
      const formalityResponse = await axios.post("http://localhost:5002/analyze-formality", {
        text: text
      });

      setPreviewAnalysis({
        slang: slangResponse.data,
        formality: formalityResponse.data,
        highlightedText: highlightSlangWords(text, slangResponse.data)
      });
    } catch (error) {
      console.error("Preview analysis error:", error);
      setPreviewAnalysis(null);
    } finally {
      setPreviewLoading(false);
    }
  };

  // Function to highlight slang words in text
  const highlightSlangWords = (text, slangData) => {
    if (!slangData || !slangData.found_terms) return text;
    
    let highlightedText = text;
    Object.keys(slangData.found_terms).forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi');
      highlightedText = highlightedText.replace(regex, `<span style="background-color: #FFE066; padding: 2px 4px; border-radius: 4px; font-weight: bold;">${word}</span>`);
    });
    
    return highlightedText;
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
        const response = await axios.post("http://localhost:5002/upload-and-analyze", formData, {
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

        // Save complete results for analysis page
        const resultData = {
          transcript: data.transcript,
          tone: data.analysis.tone,
          slang: data.analysis.slang,
          analysis: data.analysis, // Save the complete analysis object
          filename: data.filename || (recordedBlob ? "Recorded Audio" : file?.name)
        };
        
        localStorage.setItem("analysisResults", JSON.stringify(resultData));
        console.log("Complete results saved to localStorage");
        
        // Navigate to results
        setTimeout(() => {
          navigate("/analyze");
        }, 100);
        
      } else if (transcript.trim()) {
        // Handle manual text analysis
        console.log("Analyzing text:", transcript.substring(0, 50) + "...");
        
        const res = await axios.post("http://localhost:5002/analyze", {
          transcript,
        }, {
          timeout: 30000, // 30 second timeout
        });
        
        console.log("Analysis response received:", res.status);
        
        if (!res.data) {
          throw new Error("Empty response from server");
        }
        
        setResults(res.data);

        // Save complete results for analysis page
        const resultData = {
          transcript: transcript,
          tone: res.data.tone,
          slang: res.data.slang,
          analysis: res.data // Save the complete analysis response
        };
        
        localStorage.setItem("analysisResults", JSON.stringify(resultData));
        console.log("Complete manual analysis results saved to localStorage");
        
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
    <div style={{
      background: theme.colors.backgroundGradient,
      minHeight: '100vh',
      color: theme.colors.onBackground,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: theme.spacing.lg,
      fontFamily: theme.typography.body1.fontFamily
    }}>
      <h2 style={{ 
        ...theme.typography.h2,
        textAlign: 'center', 
        marginBottom: theme.spacing.xl, 
        color: theme.colors.primary,
        fontWeight: '600'
      }}>
        Audio Analysis & Slang Detection
      </h2>
      
      {error && (
        <div style={{
          color: theme.colors.error, 
          marginBottom: theme.spacing.lg,
          padding: theme.spacing.md,
          background: 'rgba(255, 107, 107, 0.1)',
          borderRadius: theme.borderRadius.bubble,
          border: `2px solid ${theme.colors.error}`,
          boxShadow: theme.shadows.light,
          fontWeight: '500'
        }}>
          {error}
        </div>
      )}
      
      {/* Tab Navigation */}
      <div style={{ marginBottom: theme.spacing.xl }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: theme.spacing.sm,
          marginBottom: theme.spacing.lg,
          borderBottom: `2px solid ${theme.colors.surfaceVariant}`,
          borderRadius: theme.borderRadius.medium
        }}>
          <button
            onClick={() => setActiveTab("upload")}
            style={{
              ...theme.typography.button,
              padding: theme.spacing.md,
              backgroundColor: activeTab === "upload" ? theme.colors.primary : 'transparent',
              color: activeTab === "upload" ? 'white' : theme.colors.primary,
              border: `2px solid ${theme.colors.primary}`,
              borderRadius: theme.borderRadius.bubble,
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: activeTab === "upload" ? theme.shadows.light : 'none'
            }}
            onMouseEnter={(e) => {
              if (activeTab !== "upload") {
                e.target.style.backgroundColor = theme.colors.primaryLight;
                e.target.style.color = 'white';
              }
            }}
            onMouseLeave={(e) => {
              if (activeTab !== "upload") {
                e.target.style.backgroundColor = 'transparent';
                e.target.style.color = theme.colors.primary;
              }
            }}
          >
            Upload File
          </button>
          <button
            onClick={() => setActiveTab("record")}
            style={{
              ...theme.typography.button,
              padding: theme.spacing.md,
              backgroundColor: activeTab === "record" ? theme.colors.secondary : 'transparent',
              color: activeTab === "record" ? 'white' : theme.colors.secondary,
              border: `2px solid ${theme.colors.secondary}`,
              borderRadius: theme.borderRadius.bubble,
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: activeTab === "record" ? theme.shadows.light : 'none'
            }}
            onMouseEnter={(e) => {
              if (activeTab !== "record") {
                e.target.style.backgroundColor = theme.colors.secondaryLight;
                e.target.style.color = 'white';
              }
            }}
            onMouseLeave={(e) => {
              if (activeTab !== "record") {
                e.target.style.backgroundColor = 'transparent';
                e.target.style.color = theme.colors.secondary;
              }
            }}
          >
            Record Audio
          </button>
          <button
            onClick={() => setActiveTab("text")}
            style={{
              ...theme.typography.button,
              padding: theme.spacing.md,
              backgroundColor: activeTab === "text" ? theme.colors.accent : 'transparent',
              color: activeTab === "text" ? 'white' : theme.colors.accent,
              border: `2px solid ${theme.colors.accent}`,
              borderRadius: theme.borderRadius.bubble,
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: activeTab === "text" ? theme.shadows.light : 'none'
            }}
            onMouseEnter={(e) => {
              if (activeTab !== "text") {
                e.target.style.backgroundColor = theme.colors.accentLight;
                e.target.style.color = 'white';
              }
            }}
            onMouseLeave={(e) => {
              if (activeTab !== "text") {
                e.target.style.backgroundColor = 'transparent';
                e.target.style.color = theme.colors.accent;
              }
            }}
          >
            Enter Text
          </button>
        </div>
      </div>

      {/* Content Based on Active Tab */}
      <div style={{ minHeight: '200px', marginBottom: theme.spacing.xl, maxWidth: '600px', width: '100%' }}>
        {activeTab === "upload" && (
          <div style={{ 
            textAlign: 'center', 
            padding: theme.spacing.xxl, 
            border: `3px dashed ${theme.colors.primary}`, 
            borderRadius: theme.borderRadius.bubble,
            background: theme.colors.surface,
            boxShadow: theme.shadows.bubble,
            backdropFilter: 'blur(10px)'
          }}>
            <h3 style={{ ...theme.typography.h3, marginBottom: theme.spacing.md, color: theme.colors.primary }}>
              Upload Audio or Video File
            </h3>
            <p style={{ 
              ...theme.typography.body1,
              color: theme.colors.onSurfaceVariant, 
              marginBottom: theme.spacing.lg
            }}>
              Supports: WAV, MP3, MP4, AVI, MOV, FLAC, M4A, OGG
            </p>
            <input
              type="file"
              accept="audio/*,video/*,.wav,.mp3,.mp4,.avi,.mov,.flac,.m4a,.ogg"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setRecordedBlob(null); // Clear any recorded audio
                setError("");
              }}
              disabled={loading}
              style={{
                ...theme.typography.body1,
                marginBottom: theme.spacing.md,
                padding: theme.spacing.sm,
                borderRadius: theme.borderRadius.medium,
                border: `2px solid ${theme.colors.primary}`,
                background: 'rgba(255,255,255,0.7)',
                cursor: loading ? 'not-allowed' : 'pointer'
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
      <div style={{ textAlign: 'center', marginTop: theme.spacing.xl }}>
        <button 
          onClick={handleDecipher}
          disabled={loading || (!file && !recordedBlob && !transcript.trim())}
          style={{
            ...theme.typography.button,
            padding: `${theme.spacing.lg}px ${theme.spacing.xxl}px`,
            backgroundColor: loading ? theme.colors.onSurfaceVariant : theme.colors.accent,
            color: 'white',
            border: 'none',
            borderRadius: theme.borderRadius.bubble,
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '20px',
            fontWeight: '700',
            boxShadow: loading ? 'none' : theme.shadows.bubble,
            transform: loading ? 'none' : 'scale(1)',
            transition: 'all 0.3s ease'
          }}
          onMouseOver={(e) => {
            if (!loading) {
              e.target.style.transform = 'scale(1.05) translateY(-2px)';
              e.target.style.boxShadow = theme.shadows.heavy;
            }
          }}
          onMouseOut={(e) => {
            if (!loading) {
              e.target.style.transform = 'scale(1)';
              e.target.style.boxShadow = theme.shadows.bubble;
            }
          }}
        >
          {loading ? 'Deciphering...' : 'DECIPHER'}
        </button>
        
        {loading && (
          <div style={{ 
            marginTop: '15px', 
            color: '#A8D8A8',
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
