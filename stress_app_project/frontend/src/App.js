import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Activity, BarChart2, MessageSquare, BookOpen } from 'lucide-react';
import PredictionPage from './pages/PredictionPage';
import MonitoringPage from './pages/MonitoringPage';
import ChatPage from './pages/ChatPage';
import ReferencePage from './pages/ReferencePage';
import './App.css';

export default function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="sidebar">
          
          {/* --- NEW MIND EASE LOGO SECTION --- */}
          <div className="logo" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '3rem', paddingLeft: '5px' }}>
            <div style={{
              background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.2))',
              padding: '10px',
              borderRadius: '12px',
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              border: '1px solid rgba(255,255,255,0.1)',
              boxShadow: '0 4px 15px rgba(139, 92, 246, 0.1)'
            }}>
              <Activity size={26} color="#f472b6" strokeWidth={2.5} />
            </div>
            <span style={{ 
              fontSize: '1.5rem', 
              fontWeight: '800', 
              background: 'linear-gradient(to right, #a78bfa, #f472b6)', 
              WebkitBackgroundClip: 'text', 
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.5px'
            }}>
              MindEase
            </span>
          </div>

          {/* --- NAVIGATION LINKS --- */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <NavLink to="/" className={({isActive})=>isActive?"nav-link active":"nav-link"}>
              <Activity size={20}/> Check Stress
            </NavLink>
            <NavLink to="/monitoring" className={({isActive})=>isActive?"nav-link active":"nav-link"}>
              <BarChart2 size={20}/> Monitoring
            </NavLink>
            <NavLink to="/chat" className={({isActive})=>isActive?"nav-link active":"nav-link"}>
              <MessageSquare size={20}/> AI Chat
            </NavLink>
            <NavLink to="/reference" className={({isActive})=>isActive?"nav-link active":"nav-link"}>
              <BookOpen size={20}/> Reference
            </NavLink>
          </div>
          
        </nav>

        {/* --- MAIN CONTENT AREA --- */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<PredictionPage />} />
            <Route path="/monitoring" element={<MonitoringPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/reference" element={<ReferencePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}