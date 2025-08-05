import React, { useRef } from "react";

function App() {
  const fileInputRef = useRef(null);

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      alignItems: "center",
      background: "#f7f9fb",
      fontFamily: "Inter, Arial, sans-serif",
      padding: "32px"
    }}>
      {/* Title */}
      <h1 style={{
        margin: 0,
        fontWeight: 700,
        fontSize: "2.5rem",
        color: "#222",
        letterSpacing: "0.05em"
      }}>
        linko
      </h1>

      {/* Upload + Record */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: "16px",
        marginTop: "48px"
      }}>
        <input
          type="file"
          ref={fileInputRef}
          style={{
            padding: "8px",
            borderRadius: "6px",
            border: "1px solid #ddd",
            background: "#fff",
            fontSize: "1rem"
          }}
        />
        <button
          style={{
            padding: "10px 20px",
            borderRadius: "6px",
            border: "none",
            background: "#4f8cff",
            color: "#fff",
            fontWeight: 600,
            fontSize: "1rem",
            cursor: "pointer",
            boxShadow: "0 2px 8px rgba(79,140,255,0.08)"
          }}
        >
          Start Recording
        </button>
      </div>

      {/* Decipher Button */}
      <button
        style={{
          marginBottom: "32px",
          padding: "14px 40px",
          borderRadius: "8px",
          border: "none",
          background: "#222",
          color: "#fff",
          fontWeight: 700,
          fontSize: "1.2rem",
          cursor: "pointer",
          boxShadow: "0 2px 8px rgba(34,34,34,0.08)"
        }}
      >
        Decipher
      </button>
    </div>
  );
}

export default App;