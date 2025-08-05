import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './ListeningPage.css';

export default function ListeningPage() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    await axios.post("http://localhost:5000/upload", formData);
  };

  const handleAnalyze = async () => {
    const res = await axios.post("http://localhost:5000/analyze", {
      transcript,
    });
    setResults(res.data);

    // Save results for analysis page (optional)
    localStorage.setItem("analysisResults", JSON.stringify(res.data));
    navigate("/analyze");
  };

  return (
  <div className="listening-container">
    <h2 className="listening-title">Upload or record</h2>
    <div className="upload-area">
      <input
        type="file"
        className="upload-input"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className="record-btn" onClick={handleUpload}>
        Upload File
      </button>
    </div>

    <h4>Transcript</h4>
    <textarea
      rows="6"
      className="upload-input"
      onChange={(e) => setTranscript(e.target.value)}
    />

    <button className="action-btn" onClick={handleAnalyze}>
      Analyze
    </button>
  </div>
);
}
