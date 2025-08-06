import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatPage.css';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Yo! What's good? � I'm your AI homie here to help you master slang and catch all that sarcasm. Drop me a message and let's see what you're working with! 💪",
      sender: 'bot',
      timestamp: new Date(),
      analysis: null
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = (userMessage, analysis) => {
    // Different personality responses - you can modify these!
    const responses = [
      "Yo, that's pretty dope! I dig what you're saying.",
      "For real? That's actually fire, not gonna lie.",
      "I'm picking up what you're putting down!",
      "That hits different! I totally get you.",
      "Damn, that's a whole vibe right there!",
      "I'm here for this energy you're bringing!",
      "Okay, I see you! That's straight facts.",
      "Bruh, you're speaking my language now!",
      "That's actually lowkey genius, no cap.",
      "I'm vibing with this conversation for sure!"
    ];

    // Add context based on analysis
    let contextualResponse = responses[Math.floor(Math.random() * responses.length)];
    
    // Add specific responses based on tone - CUSTOMIZE THESE!
    if (analysis?.tone) {
      const tone = analysis.tone.toLowerCase();
      if (tone.includes('sarcastic') || tone.includes('cautionary')) {
        contextualResponse = "Ooh, I see the sass! � " + contextualResponse;
      } else if (tone.includes('appreciative') || tone.includes('inspirational')) {
        contextualResponse = "Your energy is absolutely contagious! ⚡ " + contextualResponse;
      } else if (tone.includes('diplomatic')) {
        contextualResponse = "I appreciate how thoughtful you're being! 🧠 " + contextualResponse;
      } else if (tone.includes('direct')) {
        contextualResponse = "I love how straight up you are! 💯 " + contextualResponse;
      }
    }

    // Add slang acknowledgment - CUSTOMIZE THIS TOO!
    if (analysis?.slang && Object.keys(analysis.slang).length > 0) {
      const slangCount = Object.keys(analysis.slang).length;
      if (slangCount === 1) {
        contextualResponse += " Nice slang usage! You're keeping it real! 🔥";
      } else {
        contextualResponse += ` Wow, ${slangCount} slang terms! You're really speaking the language! 🗣️�`;
      }
    }

    return contextualResponse;
  };

  const analyzeMessage = async (text) => {
    try {
      const response = await axios.post("http://localhost:5001/analyze", {
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

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
      analysis: null
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText;
    setInputText('');
    setIsLoading(true);

    try {
      // Analyze the user's message
      const analysis = await analyzeMessage(currentInput);
      
      // Update user message with analysis
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id 
          ? { ...msg, analysis }
          : msg
      ));

      // Generate and add bot response
      setTimeout(() => {
        const botResponse = {
          id: Date.now() + 1,
          text: generateBotResponse(currentInput, analysis),
          sender: 'bot',
          timestamp: new Date(),
          analysis: null
        };

        setMessages(prev => [...prev, botResponse]);
        setIsLoading(false);
      }, 1000); // Simulate thinking time

    } catch (error) {
      console.error("Error sending message:", error);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessageWithHighlights = (message) => {
    if (!message.analysis || message.sender === 'bot') {
      return <span>{message.text}</span>;
    }

    let highlightedText = message.text;
    const slangWords = message.analysis.slang || {};
    
    // Highlight slang words
    Object.keys(slangWords).forEach(slangWord => {
      const regex = new RegExp(`\\b${slangWord}\\b`, 'gi');
      highlightedText = highlightedText.replace(regex, 
        `<span class="slang-highlight" title="${slangWords[slangWord]}">${slangWord}</span>`
      );
    });

    // Add sarcasm detection
    const tone = message.analysis.tone?.toLowerCase() || '';
    if (tone.includes('sarcastic') || tone.includes('cautionary')) {
      highlightedText = `<span class="sarcasm-highlight">${highlightedText}</span>`;
    }

    return <span dangerouslySetInnerHTML={{ __html: highlightedText }} />;
  };

  const getToneEmoji = (tone) => {
    if (!tone) return '';
    const toneMap = {
      'appreciative': '😊',
      'cautionary': '⚠️',
      'diplomatic': '🤝',
      'direct': '💪',
      'informative': '📚',
      'inspirational': '✨',
      'sarcastic': '😏',
      'neutral': '😐',
      'happy': '😄',
      'sad': '😢',
      'angry': '😠'
    };
    
    const lowerTone = tone.toLowerCase();
    for (const [key, emoji] of Object.entries(toneMap)) {
      if (lowerTone.includes(key)) {
        return emoji;
      }
    }
    return '💬';
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>🤖 AI Chat Assistant</h2>
        <p>Chat with me and I'll help you understand slang, sarcasm, and communication patterns!</p>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className="message-content">
              <div className="message-text">
                {renderMessageWithHighlights(message)}
              </div>
              
              {message.analysis && message.sender === 'user' && (
                <div className="message-analysis">
                  <div className="tone-indicator">
                    <span className="tone-emoji">{getToneEmoji(message.analysis.tone)}</span>
                    <span className="tone-text">{message.analysis.tone}</span>
                  </div>
                  
                  {Object.keys(message.analysis.slang || {}).length > 0 && (
                    <div className="slang-indicator">
                      <span className="slang-count">
                        🗣️ {Object.keys(message.analysis.slang).length} slang term(s) detected
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="input-wrapper">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Press Enter to send)"
            className="chat-input"
            rows="2"
            disabled={isLoading}
          />
          <button 
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        
        <div className="legend">
          <div className="legend-item">
            <span className="legend-color slang-sample"></span>
            <span>Slang words (hover for meaning)</span>
          </div>
          <div className="legend-item">
            <span className="legend-color sarcasm-sample"></span>
            <span>Sarcasm/Caution detected</span>
          </div>
        </div>
      </div>
    </div>
  );
}
