import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Sparkles, Trash2, Zap, Clock, MessageSquare } from 'lucide-react';
import { motion } from 'framer-motion';

// --- CONFIGURATION ---
const API_URL = 'http://127.0.0.1:8000/chat';
const QUICK_SUGGESTIONS = [
  "I'm feeling overwhelmed",
  "I can't sleep",
  "Help me with a panic attack",
  "I have too much homework"
];

export default function ChatPage() {
  // --- STATE ---
  const [history, setHistory] = useState([
    { 
      role: 'bot', 
      text: "Hello! I'm MindEase AI. I'm here to listen and help you navigate your stress. How are you feeling right now?",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // --- EFFECTS ---
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, loading]);

  // --- HANDLERS ---
  const send = async (msgText = input) => {
    if (!msgText.trim()) return;
    
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { role: 'user', text: msgText, time: timestamp };

    setHistory(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    
    try {
      const contextDocs = history.map(h => h.text);
      const { data } = await axios.post(API_URL, { message: msgText, history: contextDocs });
      
      const botMsg = { 
        role: 'bot', 
        text: data.reply, 
        advice: data.advice,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };

      setHistory(prev => [...prev, botMsg]);
    } catch (err) {
      setHistory(prev => [...prev, { 
        role: 'bot', 
        text: "I'm having trouble connecting to the server. Please check if the backend is running.",
        time: timestamp 
      }]);
    }
    setLoading(false);
  };

  const clearChat = () => {
    if(window.confirm("Are you sure you want to clear the conversation?")) {
      setHistory([{ 
        role: 'bot', 
        text: "Chat cleared. How can I support you now?",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    }
  };

  // --- RENDER ---
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={styles.container}>
      
      {/* HEADER */}
      <div style={styles.headerContainer}>
        <div style={styles.titleWrapper}>
          <div style={styles.iconBox}>
            <MessageSquare size={28} color="#c084fc" />
          </div>
          <h1 style={styles.title}>AI Wellness Companion</h1>
        </div>
        <p style={{ color: '#94a3b8' }}>Powered by NLP & Sentiment Analysis</p>
        
        <button onClick={clearChat} style={styles.clearButton} onMouseOver={(e) => e.target.style.background = 'rgba(239, 68, 68, 0.2)'} onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.05)'}>
          <Trash2 size={16} /> Clear
        </button>
      </div>

      {/* CHAT WINDOW */}
      <div className="card" style={styles.chatWindow}>
        
        {/* MESSAGES AREA */}
        <div style={styles.messagesArea}>
          {history.map((m, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} style={{ ...styles.messageRow, flexDirection: m.role === 'user' ? 'row-reverse' : 'row' }}>
              
              {/* Avatar */}
              <div style={{ ...styles.avatar, background: m.role === 'user' ? 'linear-gradient(135deg, #8b5cf6, #ec4899)' : 'rgba(30, 41, 59, 1)' }}>
                {m.role === 'user' ? <User size={20} color="white" /> : <Bot size={20} color="#a78bfa" />}
              </div>

              {/* Message Bubble */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: m.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }}>
                <div style={{ 
                  ...styles.bubble, 
                  background: m.role === 'user' ? 'linear-gradient(135deg, #8b5cf6, #ec4899)' : 'rgba(255,255,255,0.05)',
                  borderTopRightRadius: m.role === 'user' ? '4px' : '20px',
                  borderTopLeftRadius: m.role === 'bot' ? '4px' : '20px',
                  border: m.role === 'bot' ? '1px solid rgba(255,255,255,0.05)' : 'none'
                }}>
                  {m.text}
                </div>

                {/* Advice Card */}
                {m.advice && (
                  <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} style={styles.adviceCard}>
                    <div style={styles.adviceHeader}><Sparkles size={16} /> Wellness Tip</div>
                    <span style={{ color: '#fde047', fontSize: '0.95rem' }}>{m.advice}</span>
                  </motion.div>
                )}

                {/* Timestamp */}
                <div style={styles.timestamp}><Clock size={10} /> {m.time}</div>
              </div>
            </motion.div>
          ))}
          
          {loading && (
            <div style={{ display: 'flex', gap: '15px', alignSelf: 'flex-start', marginLeft: '10px' }}>
               <div style={{ ...styles.avatar, background: 'rgba(30, 41, 59, 1)' }}><Bot size={20} color="#a78bfa" /></div>
               <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5 }} style={styles.loadingBubble}>
                <Zap size={14} /> Generating response...
              </motion.div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT AREA */}
        <div style={styles.inputArea}>
          {/* Quick Suggestions */}
          <div style={styles.suggestionsWrapper}>
            {QUICK_SUGGESTIONS.map((s, i) => (
              <motion.button key={i} whileHover={{ scale: 1.05, backgroundColor: 'rgba(139, 92, 246, 0.2)' }} whileTap={{ scale: 0.95 }} onClick={() => send(s)} style={styles.suggestionChip}>
                {s}
              </motion.button>
            ))}
          </div>

          <div style={styles.inputWrapper}>
            <input 
              value={input} 
              onChange={e => setInput(e.target.value)} 
              placeholder="Type your message..." 
              onKeyPress={e => e.key === 'Enter' && send()}
              disabled={loading}
              style={styles.textInput} 
            />
            <motion.button 
              whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={() => send()} disabled={loading || !input.trim()}
              style={{ ...styles.sendButton, background: input.trim() ? 'linear-gradient(135deg, #8b5cf6, #ec4899)' : 'rgba(255,255,255,0.1)', opacity: input.trim() ? 1 : 0.5 }}
            >
              <Send size={20} color="white" />
            </motion.button>
          </div>
        </div>

      </div>
    </motion.div>
  );
}

// --- STYLES OBJECT ---
const styles = {
  // CHANGED: Increased height to 85vh to fill more screen space
  container: { height: '85vh', display: 'flex', flexDirection: 'column', maxWidth: '1000px', margin: '0 auto', width: '100%' },
  
  headerContainer: { textAlign: 'center', marginBottom: '1.5rem', position: 'relative' },
  titleWrapper: { display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '0.5rem' },
  iconBox: { background: 'rgba(139, 92, 246, 0.2)', padding: '10px', borderRadius: '12px', display: 'flex' },
  title: { fontSize: '2.5rem', margin: 0, background: 'linear-gradient(to right, #a78bfa, #f472b6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 800 },
  clearButton: { position: 'absolute', right: 0, top: '50%', transform: 'translateY(-50%)', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: '#94a3b8', padding: '8px 12px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', transition: 'all 0.2s' },
  
  // CHANGED: Added minHeight to ensure it feels tall even on larger screens
  chatWindow: { flex: 1, minHeight: '600px', display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 0, background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8))', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.05)', boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)' },
  
  messagesArea: { flex: 1, overflowY: 'auto', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' },
  messageRow: { display: 'flex', gap: '15px' },
  avatar: { width: '42px', height: '42px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 12px rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.1)', flexShrink: 0 },
  bubble: { padding: '14px 20px', borderRadius: '20px', color: 'white', lineHeight: '1.6', boxShadow: '0 4px 15px rgba(0,0,0,0.1)', fontSize: '1rem' },
  adviceCard: { marginTop: '12px', background: 'rgba(250, 204, 21, 0.05)', border: '1px solid rgba(250, 204, 21, 0.2)', padding: '15px', borderRadius: '16px', display: 'flex', flexDirection: 'column', gap: '8px', maxWidth: '100%', boxShadow: '0 4px 15px rgba(250, 204, 21, 0.05)' },
  adviceHeader: { display: 'flex', alignItems: 'center', gap: '8px', color: '#facc15', fontWeight: '600', fontSize: '0.9rem' },
  timestamp: { display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', color: '#64748b', marginTop: '6px', margin: '0 5px' },
  loadingBubble: { padding: '12px 20px', borderRadius: '20px', background: 'rgba(255,255,255,0.03)', color: '#94a3b8', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' },
  inputArea: { padding: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)', background: 'rgba(15, 23, 42, 0.8)' },
  suggestionsWrapper: { display: 'flex', gap: '10px', marginBottom: '1rem', overflowX: 'auto', paddingBottom: '5px' },
  suggestionChip: { whiteSpace: 'nowrap', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: '#e2e8f0', padding: '8px 16px', borderRadius: '20px', cursor: 'pointer', fontSize: '0.85rem', transition: 'border-color 0.2s' },
  inputWrapper: { display: 'flex', gap: '10px', alignItems: 'center', background: 'rgba(0,0,0,0.3)', padding: '8px', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 4px 20px rgba(0,0,0,0.2)' },
  textInput: { flex: 1, padding: '12px 16px', background: 'transparent', border: 'none', color: 'white', fontSize: '1rem', outline: 'none' },
  sendButton: { border: 'none', borderRadius: '12px', width: '45px', height: '45px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 4px 15px rgba(236, 72, 153, 0.3)', transition: 'opacity 0.2s' }
};