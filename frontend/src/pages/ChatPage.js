import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatPage.css';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "yo what's good! I'm here to break down how you're communicating - like analyzing your tone, catching your slang, and explaining what vibe you're giving off. just talk natural and I'll tell you exactly what energy you're bringing to the conversation",
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
    // Start with casual acknowledgment
    const casualOpeners = [
      "Yooo", "Aight so", "Okay I see you", "Hold up", "Damn", "Yo listen", 
      "Real talk", "Nah but fr", "Wait wait", "Bruh", "Okay so"
    ];
    
    let response = casualOpeners[Math.floor(Math.random() * casualOpeners.length)];
    
    // Add detailed explanation of what they said
    const messageLength = userMessage.length;
    if (messageLength < 20) {
      response += ", you kept it short and sweet there";
    } else if (messageLength < 50) {
      response += ", you're getting straight to the point";
    } else {
      response += ", you really went into detail with that one";
    }
    
    // Analyze and explain their tone with casual language
    if (analysis?.tone) {
      const tone = analysis.tone.toLowerCase();
      response += ". ";
      
      if (tone.includes('sarcastic')) {
        response += "I can tell you're being sarcastic af right now 😏 Like you're not even trying to hide that attitude. The way you said that has mad sassy energy";
      } else if (tone.includes('appreciative') || tone.includes('inspirational')) {
        response += "Your whole vibe is so positive rn! Like you're genuinely being appreciative and that energy is contagious. You sound mad grateful and uplifting";
      } else if (tone.includes('angry') || tone.includes('direct')) {
        response += "You're coming with some serious direct energy - no sugar coating, just straight facts. You sound like you mean business and you're not playing around";
      } else if (tone.includes('diplomatic')) {
        response += "You're being super diplomatic about this, like trying to keep things smooth and respectful. That's some mature communication right there";
      } else if (tone.includes('cautionary')) {
        response += "You're throwing out some warning vibes, like you're trying to give me a heads up about something. That cautionary tone is real";
      } else if (tone.includes('informative')) {
        response += "You're dropping knowledge bombs rn, like you're really trying to educate and inform. That teacher energy is strong";
      } else {
        response += "Your tone is pretty chill and neutral - just having a regular conversation without any extra drama";
      }
    }
    
    // Explain slang usage in detail
    if (analysis?.slang && Object.keys(analysis.slang).length > 0) {
      const slangWords = Object.keys(analysis.slang);
      const slangCount = slangWords.length;
      
      response += ". And yo, ";
      
      if (slangCount === 1) {
        const word = slangWords[0];
        const meaning = analysis.slang[word];
        response += `you dropped "${word}" in there which means "${meaning}" - that's some solid slang usage right there`;
      } else if (slangCount === 2) {
        response += `you used ${slangCount} slang terms: "${slangWords.join('" and "')}" - you're really speaking the language`;
      } else {
        response += `you went off with ${slangCount} different slang words! "${slangWords.slice(0,2).join('", "')}" and more - your vocabulary is absolutely unmatched`;
      }
    }
    
    // Add a casual reaction/follow-up
    const reactions = [
      ". That's actually fire", ". I respect that energy", ". You're valid for that",
      ". That hits different", ". I see you", ". That's a whole mood",
      ". No cap that's real", ". I'm here for this vibe", ". Facts though"
    ];
    
    if (Math.random() > 0.3) { // 70% chance to add reaction
      response += reactions[Math.floor(Math.random() * reactions.length)];
    }
    
    // Sometimes add follow-up questions (40% chance)
    if (Math.random() > 0.6) {
      const questions = [
        ". What made you feel that way though?", 
        ". You wanna talk more about that?",
        ". How long you been feeling like this?",
        ". What's your take on the whole situation?",
        ". You think I'm reading this right?",
        ". Am I picking up what you're putting down?"
      ];
      response += questions[Math.floor(Math.random() * questions.length)];
    }
    
    return response;
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

      // Generate and add bot response with more realistic delay
      const delay = Math.random() * 2000 + 1000; // 1-3 seconds
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
      }, delay);

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
        <h2>💬 Chat</h2>
        <p>Just having a regular conversation - see what gets highlighted!</p>
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
