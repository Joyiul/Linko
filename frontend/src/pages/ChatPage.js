import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatPage.css';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your language learning assistant. 👋 Send me any English phrase, slang, or sentence and I'll break it down for you - explaining the meaning, tone, cultural context, and any hidden meanings like sarcasm. Perfect for learning English nuances!",
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
    let response = "📚 **Phrase Analysis:**\n\n";
    
    // Add the original message
    response += `**Your message:** "${userMessage}"\n\n`;
    
    // Priority: Check for sarcasm first
    if (analysis?.sarcasm_analysis?.sarcasm_detected) {
      const sarcasm = analysis.sarcasm_analysis;
      response += `🎭 **SARCASM DETECTED!** (Confidence: ${(sarcasm.confidence * 100).toFixed(0)}%)\n\n`;
      response += `**Sarcasm Type:** ${sarcasm.sarcasm_type || 'General'}\n\n`;
      
      if (sarcasm.reasons && sarcasm.reasons.length > 0) {
        response += `**Why this is sarcastic:**\n`;
        sarcasm.reasons.forEach(reason => {
          response += `• ${reason}\n`;
        });
        response += "\n";
      }
      
      response += `**What you really mean:** You're expressing frustration or dissatisfaction, but using positive words ironically. You don't literally mean what you're saying - you mean the opposite!\n\n`;
      
      if (sarcasm.sarcasm_type === 'economic' || sarcasm.sarcasm_type === 'work_related') {
        response += `**Context:** This is **economic sarcasm** - you're frustrated about work or money issues. This is very common when people feel underpaid or overworked.\n\n`;
      }
      
      response += `**Cultural Note:** Sarcasm is very common in English, especially when expressing frustration about work, money, or daily life. Native speakers use it to vent feelings without being directly negative.\n\n`;
    }
    
    // Analyze tone with detailed explanation
    if (analysis?.tone) {
      const tone = analysis.tone.toLowerCase();
      const toneEmoji = getToneEmoji(analysis.tone);
      
      if (!tone.includes('sarcastic')) {
        response += `**Tone Analysis:** ${analysis.tone}\n`;
        
        if (tone.includes('appreciative') || tone.includes('inspirational')) {
          response += `This shows a **positive, grateful tone** - you're expressing appreciation or trying to inspire others. This creates a warm, encouraging feeling.\n\n`;
        } else if (tone.includes('angry') || tone.includes('direct')) {
          response += `This has a **direct, assertive tone** - you're being straightforward and serious. This isn't necessarily rude, but it shows you mean business.\n\n`;
        } else if (tone.includes('diplomatic')) {
          response += `This shows **diplomatic communication** - you're being polite, respectful, and trying to avoid conflict. This is great for professional or sensitive conversations.\n\n`;
        } else if (tone.includes('cautionary')) {
          response += `This has a **warning or cautious tone** - you're trying to alert someone to potential problems or giving advice to be careful.\n\n`;
        } else if (tone.includes('informative')) {
          response += `This is **informative and educational** - you're sharing knowledge or explaining something to help others learn.\n\n`;
        } else {
          response += `This has a **neutral, conversational tone** - friendly and casual without strong emotions.\n\n`;
        }
      }
    }
    
    // Analyze slang and difficult words
    if (analysis?.slang && Object.keys(analysis.slang).length > 0) {
      response += `**🗣️ Slang & Cultural Terms Found:**\n`;
      
      Object.entries(analysis.slang).forEach(([word, slangData]) => {
        // Handle both old format (string) and new format (object)
        const meaning = typeof slangData === 'string' ? slangData : slangData?.meaning || slangData;
        response += `• **"${word}"** means: ${meaning}\n`;
        response += `  Context: This is informal language you might hear in casual conversations.\n`;
      });
      response += "\n";
    }
    
    // Break down sentence structure and meaning
    response += `**📝 Complete Meaning:**\n`;
    const messageLength = userMessage.length;
    const complexity = messageLength > 50 ? "complex" : messageLength > 20 ? "moderate" : "simple";
    
    response += `This is a ${complexity} sentence. `;
    
    // Provide cultural context
    if (analysis?.sarcasm_analysis?.sarcasm_detected) {
      response += `The sarcasm here means the speaker doesn't literally mean what they're saying - they're being ironic or expressing frustration. In English culture, sarcasm is very common, especially about work and money, but can be confusing for non-native speakers.`;
    } else if (analysis?.tone?.toLowerCase().includes('sarcastic')) {
      response += `The sarcasm here means the speaker doesn't literally mean what they're saying - they're being ironic or mocking. In English culture, sarcasm is common but can be confusing for non-native speakers.`;
    } else {
      response += `The speaker is communicating directly and genuinely - what they say is what they mean.`;
    }
    
    // Add learning tip
    response += `\n\n**💡 Learning Tip:** `;
    const tips = [
      "Pay attention to context clues and body language to understand the full meaning.",
      "Practice recognizing tone patterns - they're crucial for English communication.",
      "Slang changes frequently, so don't worry if you don't know every term.",
      "When in doubt, it's okay to ask 'What do you mean by that?' - most people are happy to explain.",
      "Notice how tone can completely change the meaning of the same words."
    ];
    
    response += tips[Math.floor(Math.random() * tips.length)];
    
    return response;
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
      // Format bot messages with proper line breaks and bold text
      if (message.sender === 'bot') {
        const formattedText = message.text
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text
          .replace(/\n/g, '<br>'); // Line breaks
        return <span dangerouslySetInnerHTML={{ __html: formattedText }} />;
      }
      return <span>{message.text}</span>;
    }

    let highlightedText = message.text;
    const slangWords = message.analysis.slang || {};
    
    // Highlight slang words with enhanced tooltips
    Object.keys(slangWords).forEach(slangWord => {
      const regex = new RegExp(`\\b${slangWord}\\b`, 'gi');
      highlightedText = highlightedText.replace(regex, 
        `<span class="slang-highlight" title="💡 '${slangWord}' means: ${slangWords[slangWord]}">${slangWord}</span>`
      );
    });

    // Enhanced sarcasm detection with clear visual indicator
    const tone = message.analysis.tone?.toLowerCase() || '';
    const hasSarcasm = message.analysis.sarcasm_analysis?.sarcasm_detected || tone.includes('sarcastic');
    
    if (hasSarcasm) {
      const confidence = message.analysis.sarcasm_analysis?.confidence || 0.5;
      const confidencePercent = Math.round(confidence * 100);
      highlightedText = `<span class="sarcasm-highlight" title="🎭 Sarcasm detected (${confidencePercent}% confidence)! This person doesn't literally mean what they're saying - they're being ironic or expressing frustration.">${highlightedText}</span>`;
    } else if (tone.includes('cautionary') || tone.includes('warning')) {
      highlightedText = `<span class="warning-highlight" title="⚠️ Warning tone detected">${highlightedText}</span>`;
    } else if (tone.includes('angry') || tone.includes('direct')) {
      highlightedText = `<span class="direct-highlight" title="💪 Direct/Assertive tone">${highlightedText}</span>`;
    }

    return <span dangerouslySetInnerHTML={{ __html: highlightedText }} />;
  };

  const getToneEmoji = (tone) => {
    if (!tone) return '💬';
    const toneMap = {
      'appreciative': '�',
      'cautionary': '⚠️',
      'diplomatic': '🤝',
      'direct': '💪',
      'informative': '📚',
      'inspirational': '✨',
      'sarcastic': '😏',
      'neutral': '😐',
      'happy': '�',
      'sad': '😢',
      'angry': '😠',
      'excited': '🎉',
      'confused': '😕',
      'friendly': '😄',
      'professional': '👔',
      'casual': '😎'
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
        <h2>Language Learning Assistant</h2>
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
                    <span className="tone-text">{message.analysis.tone}</span>
                    <span className="tone-text">Tone: {message.analysis.tone}</span>
                  </div>
                  
                  {Object.keys(message.analysis.slang || {}).length > 0 && (
                    <div className="slang-indicator">
                      <span className="slang-count">
                        🗣️ Found {Object.keys(message.analysis.slang).length} slang/cultural term(s)
                      </span>
                    </div>
                  )}
                  
                  {(message.analysis.tone?.toLowerCase().includes('sarcastic') || message.analysis.sarcasm_analysis?.sarcasm_detected) && (
                    <div className="sarcasm-warning">
                      <span className="sarcasm-alert">
                        🎭 Sarcasm Alert: Not literal meaning! 
                        {message.analysis.sarcasm_analysis?.confidence && 
                          ` (${Math.round(message.analysis.sarcasm_analysis.confidence * 100)}% confidence)`
                        }
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
            placeholder="Type any English phrase here for analysis... (Press Enter to send)"
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
            <span>Slang/Cultural terms (hover for definition)</span>
          </div>
          <div className="legend-item">
            <span className="legend-color sarcasm-sample"></span>
            <span>Sarcasm (not literal meaning!)</span>
          </div>
          <div className="legend-item">
            <span className="legend-color warning-sample"></span>
            <span>Warning/Cautionary tone</span>
          </div>
          <div className="legend-item">
            <span className="legend-color direct-sample"></span>
            <span>Direct/Assertive tone</span>
          </div>
        </div>
      </div>
    </div>
  );
}
