import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import FormalityAnalysis from '../components/FormalityAnalysis';
import './ChatPage.css';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "hey there! 👋 welcome to your SMS-style English learning chat! I'm here to help you practice modern English with all the latest slang, idioms, and cultural expressions! 📱✨\n\nJust text me like you would text a friend, and I'll respond using trendy phrases, slang, and cultural references - then break down what everything means! Perfect for learning how young people actually talk 😎\n\nWhat's on your mind today bestie?",
      sender: 'bot',
      timestamp: new Date(),
      analysis: null,
      messageType: 'welcome'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getSMSBotResponse = async (userMessage) => {
    try {
      const response = await axios.post("http://localhost:5002/sms-chat", {
        message: userMessage,
        timestamp: new Date().toISOString()
      }, {
        timeout: 15000,
      });
      
      return response.data.bot_response;
    } catch (error) {
      console.error("SMS Bot error:", error);
      // Fallback response with slang
      return "Oop, my bad bestie! Something went wrong on my end 😅 But no cap, you can keep chatting with me! Try asking about slang, modern phrases, or just tell me about your day! ✨";
    }
  };

  const analyzeMessage = async (text) => {
    try {
      const response = await axios.post("http://localhost:5002/analyze", {
        transcript: text,
      }, {
        timeout: 15000,
      });
      return response.data;
    } catch (error) {
      console.error("Analysis error:", error);
      return { tone: "Neutral", slang: {} };
    }
  };

  const getPracticeSuggestion = async () => {
    try {
      const response = await axios.get("http://localhost:5002/practice-suggestion");
      return response.data.practice_suggestion;
    } catch (error) {
      console.error("Practice suggestion error:", error);
      return {
        scenario: "Express excitement about something",
        slang_response: "OMG that's so fire! I'm literally obsessed! 🔥",
        explanation: "'Fire' means amazing, 'literally obsessed' means you really love something"
      };
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
      analysis: null,
      messageType: 'user'
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText;
    setInputText('');
    setIsLoading(true);

    try {
      // Get SMS-style bot response and analysis in parallel
      const [botResponseText, analysis] = await Promise.all([
        getSMSBotResponse(currentInput),
        analyzeMessage(currentInput)
      ]);
      
      // Update user message with analysis
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id 
          ? { ...msg, analysis }
          : msg
      ));

      // Add bot response with realistic SMS delay
      const delay = Math.random() * 1500 + 800; // 0.8-2.3 seconds (realistic SMS timing)
      setTimeout(() => {
        const botResponse = {
          id: Date.now() + 1,
          text: botResponseText,
          sender: 'bot',
          timestamp: new Date(),
          analysis: null,
          messageType: 'sms_response'
        };

        setMessages(prev => [...prev, botResponse]);
        setIsLoading(false);
      }, delay);

    } catch (error) {
      console.error("Error sending message:", error);
      setIsLoading(false);
      
      // Add error message in SMS style
      const errorResponse = {
        id: Date.now() + 1,
        text: "oops bestie! something went wrong but we're still good! 😅 try again or ask me anything about English slang! no cap I'm here to help! ✨",
        sender: 'bot',
        timestamp: new Date(),
        analysis: null,
        messageType: 'error'
      };
      setMessages(prev => [...prev, errorResponse]);
    }
  };

  const handlePracticeSuggestion = async () => {
    setIsLoading(true);
    try {
      const suggestion = await getPracticeSuggestion();
      
      const practiceMessage = {
        id: Date.now(),
        text: `💭 **Practice Scenario**: ${suggestion.scenario}\n\n📱 **Try this response**: "${suggestion.slang_response}"\n\n📚 **What it means**: ${suggestion.explanation}\n\nNow you try! Use some of these phrases in your next message! ✨`,
        sender: 'bot',
        timestamp: new Date(),
        analysis: null,
        messageType: 'practice'
      };
      
      setMessages(prev => [...prev, practiceMessage]);
    } catch (error) {
      console.error("Practice suggestion error:", error);
    }
    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessageWithHighlights = (message) => {
    if (message.sender === 'bot') {
      // Format bot messages with proper styling for SMS responses
      const formattedText = message.text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text
        .replace(/\n/g, '<br>') // Line breaks
        .replace(/📚 \*\*Slang breakdown:\*\*/g, '<div class="slang-breakdown-title">📚 <strong>Slang breakdown:</strong></div>')
        .replace(/• "(.*?)" = (.*?)(<br>|$)/g, '<div class="slang-explanation">• <span class="slang-term">"$1"</span> = <span class="slang-meaning">$2</span></div>');
      
      return <span dangerouslySetInnerHTML={{ __html: formattedText }} />;
    }

    // Highlight user messages with analysis
    if (!message.analysis) {
      return <span>{message.text}</span>;
    }

    let highlightedText = message.text;
    const slangWords = message.analysis.slang || {};
    
    // Highlight slang words with enhanced tooltips
    Object.keys(slangWords).forEach(slangWord => {
      const regex = new RegExp(`\\b${slangWord}\\b`, 'gi');
      const meaning = typeof slangWords[slangWord] === 'string' ? slangWords[slangWord] : slangWords[slangWord]?.meaning || slangWords[slangWord];
      highlightedText = highlightedText.replace(regex, 
        `<span class="slang-highlight" title="💡 '${slangWord}' means: ${meaning}">${slangWord}</span>`
      );
    });

    // Enhanced sarcasm detection
    const tone = message.analysis.tone?.toLowerCase() || '';
    const hasSarcasm = message.analysis.sarcasm_analysis?.sarcasm_detected || tone.includes('sarcastic');
    
    if (hasSarcasm) {
      const confidence = message.analysis.sarcasm_analysis?.confidence || 0.5;
      const confidencePercent = Math.round(confidence * 100);
      highlightedText = `<span class="sarcasm-highlight" title="🎭 Sarcasm detected (${confidencePercent}% confidence)! This person doesn't literally mean what they're saying - they're being ironic.">${highlightedText}</span>`;
    }

    return <span dangerouslySetInnerHTML={{ __html: highlightedText }} />;
  };

  const getMessageBubbleClass = (message) => {
    let baseClass = `message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`;
    
    if (message.messageType === 'welcome') {
      baseClass += ' welcome-message';
    } else if (message.messageType === 'practice') {
      baseClass += ' practice-message';
    } else if (message.messageType === 'sms_response') {
      baseClass += ' sms-response';
    }
    
    return baseClass;
  };

  return (
    <div className="chat-container sms-style">
      <div className="chat-header sms-header">
        <div className="chat-title">
          <h2>📱 SMS English Practice</h2>
          <p>Learn modern English through conversational texting! 💬✨</p>
        </div>
        <div className="chat-controls">
          <button 
            className="practice-btn" 
            onClick={handlePracticeSuggestion}
            disabled={isLoading}
          >
            💡 Get Practice Suggestion
          </button>
          <button 
            className="analysis-toggle" 
            onClick={() => setShowAnalysis(!showAnalysis)}
          >
            {showAnalysis ? '🔍 Hide Analysis' : '🔍 Show Analysis'}
          </button>
        </div>
      </div>

      <div className="messages-container sms-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={getMessageBubbleClass(message)}
          >
            <div className="message-content">
              <div className="message-text">
                {renderMessageWithHighlights(message)}
              </div>
              
              {message.analysis && message.sender === 'user' && showAnalysis && (
                <div className="message-analysis sms-analysis">
                  <div className="analysis-header">📊 Quick Analysis:</div>
                  
                  <div className="tone-indicator">
                    <span className="analysis-label">Tone:</span>
                    <span className="tone-text">{message.analysis.tone}</span>
                  </div>
                  
                  {Object.keys(message.analysis.slang || {}).length > 0 && (
                    <div className="slang-indicator">
                      <span className="analysis-label">Slang found:</span>
                      <span className="slang-count">
                        {Object.keys(message.analysis.slang).length} term(s) 🗣️
                      </span>
                    </div>
                  )}
                  
                  {(message.analysis.tone?.toLowerCase().includes('sarcastic') || message.analysis.sarcasm_analysis?.sarcasm_detected) && (
                    <div className="sarcasm-warning">
                      <span className="sarcasm-alert">
                        🎭 Sarcasm detected
                        {message.analysis.sarcasm_analysis?.confidence && 
                          ` (${Math.round(message.analysis.sarcasm_analysis.confidence * 100)}%)`
                        }
                      </span>
                    </div>
                  )}

                  {/* Formality Analysis for Chat Messages */}
                  <div style={{ marginTop: 12 }}>
                    <FormalityAnalysis 
                      text={message.text}
                      initialData={message.analysis.formality_analysis ? { 
                        formality_analysis: message.analysis.formality_analysis,
                        explicit_formality_breakdown: message.analysis.explicit_formality_breakdown,
                        success: true 
                      } : null}
                      showTitle={false}
                    />
                  </div>
                </div>
              )}
            </div>
            
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              {message.sender === 'user' && <span className="read-indicator">✓✓</span>}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot-message typing-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div className="typing-text">typing...</div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container sms-input">
        <div className="input-wrapper">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Text me anything! Ask about slang, share your thoughts, or practice English... 💬"
            className="chat-input sms-input-field"
            rows="2"
            disabled={isLoading}
          />
          <button 
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="send-button sms-send"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
        
        <div className="sms-legend">
          <div className="legend-item">
            <span className="legend-color slang-sample"></span>
            <span>Slang terms (hover for meaning)</span>
          </div>
          <div className="legend-item">
            <span className="legend-color sarcasm-sample"></span>
            <span>Sarcasm (ironic meaning)</span>
          </div>
          <div className="legend-item">
            <span className="emoji-indicator">🔥✨💯</span>
            <span>Modern expressions & emojis</span>
          </div>
        </div>

        {/* AI Disclaimer */}
        <div style={{
          marginTop: '20px',
          padding: '12px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          border: '1px solid #dee2e6',
          textAlign: 'center'
        }}>
          <p style={{
            margin: 0,
            fontSize: '13px',
            color: '#6c757d',
            fontStyle: 'italic'
          }}>
            ⚠️ This response was generated using AI. Please use responsibly.
          </p>
        </div>
      </div>
    </div>
  );
}
