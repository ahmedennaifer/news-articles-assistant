import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your AI assistant. I can help you with questions about BBC articles, web searches, database queries, and general knowledge. What would you like to know?",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/generate/${encodeURIComponent(inputValue)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      console.log('Full API Response:', data);
      console.log('Response type:', typeof data.response);
      console.log('Response content:', data.response);

      // Your backend returns {"response": ["text here"]}
      let responseContent = '';
      if (data && data.response) {
        if (Array.isArray(data.response) && data.response.length > 0) {
          responseContent = data.response[0];
        } else if (typeof data.response === 'string') {
          responseContent = data.response;
        }
      }

      console.log('Final response content:', responseContent);

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: responseContent || 'Sorry, I couldn\'t generate a response.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-blue-900 flex">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-400/8 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-500/8 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-3/4 left-3/4 w-64 h-64 bg-indigo-400/8 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      <div className="relative w-full h-[100vh] backdrop-blur-xl bg-white/5 border border-white/10 rounded-none shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="relative p-6 border-b border-white/10 bg-gradient-to-r from-blue-600/15 to-teal-600/15">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-teal-500 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white flex items-center space-x-2">
                <span>AI Assistant</span>
                <Sparkles className="w-5 h-5 text-yellow-300 animate-pulse" />
              </h1>
              <p className="text-sm text-white/70">BBC Articles • Web Search • Database • General Knowledge</p>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 h-[calc(100vh-200px)]">
          {messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fadeInUp`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`flex max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'} items-start space-x-3`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-green-400 to-blue-500 ml-3'
                    : 'bg-gradient-to-r from-blue-500 to-teal-500 mr-3'
                }`}>
                  {message.type === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>

                {/* Message Bubble */}
                <div className={`relative group ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-blue-600 to-teal-600'
                    : 'bg-white/10 backdrop-blur-sm border border-white/20'
                } rounded-2xl px-4 py-3 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-[1.02]`}>
                  <p className="text-white text-sm leading-relaxed whitespace-pre-wrap">
                    {message.content}
                  </p>
                  <span className="text-xs text-white/50 mt-1 block">
                    {formatTime(message.timestamp)}
                  </span>

                  {/* Message tail */}
                  <div className={`absolute top-4 ${
                    message.type === 'user'
                      ? 'right-0 translate-x-1'
                      : 'left-0 -translate-x-1'
                  } w-3 h-3 ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-blue-600 to-teal-600'
                      : 'bg-white/10 border-l border-t border-white/20'
                  } rotate-45`}></div>
                </div>
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex justify-start animate-fadeInUp">
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-teal-500 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-white/10 bg-white/5">
          <div className="relative">
            <div className="flex space-x-3">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about BBC articles, web searches, or general questions..."
                  className="w-full bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl px-6 py-4 pr-16 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-300 resize-none min-h-[60px] max-h-32"
                  rows="1"
                  disabled={isLoading}
                />

                {/* Send button */}
                <button
                  onClick={sendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-gradient-to-r from-blue-500 to-teal-500 rounded-xl flex items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 group"
                >
                  <Send className="w-5 h-5 text-white group-hover:translate-x-0.5 transition-transform duration-200" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.6s ease-out forwards;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
          width: 8px;
        }

        ::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.3);
          border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.5);
        }

        /* Auto-resize textarea */
        textarea {
          field-sizing: content;
        }
      `}</style>
    </div>
  );
};

export default ChatInterface;
