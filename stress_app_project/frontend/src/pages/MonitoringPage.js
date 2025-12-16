import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Database, TrendingUp, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

// --- CONFIGURATION ---
const API_URL = 'http://127.0.0.1:8000/monitoring-data';

export default function MonitoringPage() {
  // --- STATE ---
  const [data, setData] = useState([]);

  // --- EFFECTS ---
  useEffect(() => {
    axios.get(API_URL)
      .then(res => setData(res.data))
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  // --- HELPERS ---
  const chartData = [
    { name: 'Low Stress', count: data.filter(d => d.predicted_label === 'Low Stress').length, color: '#4ade80' },
    { name: 'Medium Stress', count: data.filter(d => d.predicted_label === 'Medium Stress').length, color: '#facc15' },
    { name: 'High Stress', count: data.filter(d => d.predicted_label === 'High Stress').length, color: '#ef4444' },
  ];

  const getBadgeStyle = (label) => ({
    ...styles.badgeBase,
    backgroundColor: label === 'High Stress' ? 'rgba(239, 68, 68, 0.15)' : label === 'Medium Stress' ? 'rgba(250, 204, 21, 0.15)' : 'rgba(74, 222, 128, 0.15)',
    color: label === 'High Stress' ? '#fca5a5' : label === 'Medium Stress' ? '#fde047' : '#86efac',
    border: `1px solid ${label === 'High Stress' ? 'rgba(239, 68, 68, 0.3)' : label === 'Medium Stress' ? 'rgba(250, 204, 21, 0.3)' : 'rgba(74, 222, 128, 0.3)'}`
  });

  // --- RENDER ---
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      
      {/* HERO SECTION */}
      <div style={styles.heroContainer}>
        <div style={styles.titleWrapper}>
            <div style={styles.iconBox}>
                <Activity size={40} color="#38bdf8" strokeWidth={2.5} />
            </div>
            <h1 style={styles.title}>MindEase Monitor</h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem', marginTop: '10px' }}>
          Real-time analytics and student data history.
        </p>
      </div>

      {/* CHARTS CARD */}
      <motion.div className="card" style={{ height: '400px', marginBottom: '2rem' }} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.1 }}>
        <h3 style={styles.cardHeader}>
          <TrendingUp size={20} color="#38bdf8" /> Stress Distribution
        </h3>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={{stroke: '#475569'}} />
            <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={{stroke: '#475569'}} />
            <Tooltip contentStyle={styles.tooltip} itemStyle={{ color: '#fff' }} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
            <Bar dataKey="count" radius={[8, 8, 0, 0]}>
              {chartData.map((entry, index) => (<Cell key={`cell-${index}`} fill={entry.color} />))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* TABLE CARD */}
      <motion.div className="card" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }}>
        <div style={styles.tableHeaderWrapper}>
          <h3 style={styles.cardHeader}>
            <Database size={20} color="#f472b6" /> Recent Predictions
          </h3>
          <span style={styles.recordCount}>Total Records: {data.length}</span>
        </div>
        
        <div style={styles.tableContainer}>
          <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '900px' }}>
            <thead style={{ background: 'rgba(15, 23, 42, 0.8)' }}>
              <tr>
                {/* CHANGED: Only 3 headers now */}
                {['ID', 'Result', 'Key Factors'].map(h => (
                  <th key={h} style={styles.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.length === 0 ? (
                // CHANGED: colSpan reduced from 6 to 3
                <tr><td colSpan="3" style={styles.emptyState}><Activity size={40} color="#475569" /><p>No data recorded yet.</p></td></tr>
              ) : (
                [...data].reverse().map((row, i) => (
                  <tr key={row.id} style={{ background: i % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent' }}>
                    <td style={styles.td}>#{row.id}</td>
                    <td style={styles.td}><span style={getBadgeStyle(row.predicted_label)}>{row.predicted_label}</span></td>
                    {/* CHANGED: Removed Anxiety, Sleep, Load columns */}
                    <td style={{ ...styles.td, color: '#94a3b8', maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {row.predicted_factors}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </motion.div>
    </motion.div>
  );
}

// --- STYLES OBJECT ---
const styles = {
  heroContainer: { textAlign: 'center', marginBottom: '3rem' },
  titleWrapper: { display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '15px', marginBottom: '0.5rem' },
  iconBox: { background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(139, 92, 246, 0.2))', padding: '12px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 20px rgba(56, 189, 248, 0.15)', border: '1px solid rgba(255,255,255,0.1)' },
  title: { fontSize: '2.8rem', margin: 0, background: 'linear-gradient(to right, #38bdf8, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 800, letterSpacing: '-0.5px' },
  cardHeader: { display: 'flex', alignItems: 'center', gap: '10px', marginTop: 0, color: '#e2e8f0', margin: 0 },
  tooltip: { backgroundColor: '#1e293b', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', color: '#fff' },
  tableHeaderWrapper: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' },
  recordCount: { fontSize: '0.85rem', color: '#94a3b8', background: 'rgba(0,0,0,0.3)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(255,255,255,0.05)' },
  tableContainer: { overflowX: 'auto', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' },
  th: { textAlign: 'left', padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: '#a78bfa', whiteSpace: 'nowrap', fontWeight: 600 },
  td: { padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)', color: '#e2e8f0', fontSize: '0.9rem' },
  emptyState: { textAlign: 'center', padding: '4rem', color: '#94a3b8' },
  badgeBase: { padding: '6px 12px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: '600' }
};
