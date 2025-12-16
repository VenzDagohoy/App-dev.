import React, { useState, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { ExternalLink, Info, Brain, HeartPulse, GraduationCap, Users, Home, ChevronDown, ChevronUp, Activity, Loader2 } from 'lucide-react';

// --- CONFIGURATION ---
const fieldGroups = [
  {
    title: "Mental & Emotional",
    icon: <Brain size={20} color="#a78bfa" />,
    fields: [
      { name: "anxiety_level", label: "Anxiety (GAD-7)", max: 21, desc: "0 (None) → 21 (Severe)" },
      { name: "depression", label: "Depression (PHQ-9)", max: 27, desc: "0 (None) → 27 (Severe)" },
      { name: "self_esteem", label: "Self Esteem", max: 30, desc: "0 (Low) → 30 (High)" },
      { name: "mental_health_history", label: "History of Illness", max: 1, desc: "0 (No) / 1 (Yes)" },
    ]
  },
  {
    title: "Physical Health",
    icon: <HeartPulse size={20} color="#f472b6" />,
    fields: [
      { name: "headache", label: "Headache Freq.", max: 5, desc: "0 (Never) → 5 (Constant)" },
      { name: "blood_pressure", label: "Blood Pressure", max: 3, desc: "0 (Normal) → 3 (High)" },
      { name: "sleep_quality", label: "Sleep Quality", max: 5, desc: "1 (Poor) → 5 (Great)" },
      { name: "breathing_problem", label: "Breathing Issues", max: 5, desc: "0 (None) → 5 (Severe)" },
    ]
  },
  {
    title: "Academic Life",
    icon: <GraduationCap size={20} color="#38bdf8" />,
    fields: [
      { name: "academic_performance", label: "Performance/Grades", max: 5, desc: "0 (Low) → 5 (High)" },
      { name: "study_load", label: "Study Load", max: 5, desc: "0 (Light) → 5 (Heavy)" },
      { name: "teacher_student_relationship", label: "Teacher Relationship", max: 5, desc: "0 (Poor) → 5 (Great)" },
      { name: "future_career_concerns", label: "Career Worry", max: 5, desc: "0 (Calm) → 5 (Worried)" },
    ]
  },
  {
    title: "Social Context",
    icon: <Users size={20} color="#facc15" />,
    fields: [
      { name: "social_support", label: "Support System", max: 3, desc: "0 (None) → 3 (Strong)" },
      { name: "peer_pressure", label: "Peer Pressure", max: 5, desc: "0 (None) → 5 (High)" },
      { name: "extracurricular_activities", label: "Activities", max: 5, desc: "0 (None) → 5 (Many)" },
      { name: "bullying", label: "Bullying", max: 5, desc: "0 (Never) → 5 (Often)" },
    ]
  },
  {
    title: "Environment",
    icon: <Home size={20} color="#4ade80" />,
    fields: [
      { name: "noise_level", label: "Noise Level", max: 5, desc: "0 (Quiet) → 5 (Loud)" },
      { name: "living_conditions", label: "Living Condition", max: 5, desc: "0 (Poor) → 5 (Great)" },
      { name: "safety", label: "Safety", max: 5, desc: "0 (Unsafe) → 5 (Safe)" },
      { name: "basic_needs", label: "Basic Needs", max: 5, desc: "0 (Not Met) → 5 (Met)" },
    ]
  }
];

const allFields = fieldGroups.flatMap(g => g.fields);

export default function PredictionPage() {
  // --- STATE ---
  const [form, setForm] = useState(allFields.reduce((acc, f) => ({ ...acc, [f.name]: 0 }), {}));
  const [result, setResult] = useState(null);
  const [showRef, setShowRef] = useState(false);
  const [loading, setLoading] = useState(false); // <--- NEW STATE
  
  // --- REF FOR SCROLLING ---
  const topRef = useRef(null);

  // --- HANDLERS ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // <--- START LOADING
    
    try {
      const { data } = await axios.post('http://127.0.0.1:8000/predict', form);
      const exp = await axios.post('http://127.0.0.1:8000/explain', { label: data.label, factors: data.factors });
      setResult({ ...data, explanation: exp.data.explanation });
      
      // Scroll result into view
      if (topRef.current) {
        topRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } catch { 
      alert("Backend offline. Please start the FastAPI server."); 
    } finally {
      setLoading(false); // <--- END LOADING
    }
  };

  // --- RENDER ---
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      
      {/* SCROLL ANCHOR */}
      <div ref={topRef} />

      {/* HERO SECTION */}
      <div style={styles.heroContainer}>
        <div style={styles.titleWrapper}>
            <div style={styles.iconBox}>
                <Activity size={32} color="#f472b6" strokeWidth={2.5} />
            </div>
            <h1 style={styles.title}>MindEase Check</h1>
        </div>
        <p style={styles.subTitle}>AI-powered stress analysis based on daily metrics.</p>
      </div>

      {/* RESULTS SECTION */}
      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="card" style={{ ...styles.resultCard, borderLeft: `6px solid ${result.prediction === 2 ? '#ef4444' : '#4ade80'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h2 style={{ margin: 0, color: result.prediction === 2 ? '#ef4444' : '#4ade80', fontSize: '1.5rem' }}>{result.label}</h2>
                <p style={{ color: '#cbd5e1', marginTop: '0.25rem', fontSize: '0.9rem' }}><strong>Key Factors:</strong> {result.factors.join(", ")}</p>
              </div>
              <Activity size={32} color={result.prediction === 2 ? '#ef4444' : '#4ade80'} style={{ opacity: 0.8 }} />
            </div>
            <div style={styles.aiInsightBox}>
              <h4 style={styles.aiHeader}><Brain size={16} /> AI Insight</h4>
              <p style={{ lineHeight: 1.5, whiteSpace: 'pre-line', color: '#e2e8f0', fontSize: '0.95rem' }}>{result.explanation}</p>
            </div>
            <button onClick={() => setResult(null)} style={styles.closeButton}>Close Result</button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* COLLAPSIBLE REFERENCE GUIDE */}
      <div className="card" style={styles.collapsibleCard}>
        <div onClick={() => setShowRef(!showRef)} style={styles.collapsibleHeader}>
          <h3 style={styles.refTitle}><Info size={18} color="#facc15" /> {showRef ? "Hide Guide" : "Show Reference Guide"}</h3>
          {showRef ? <ChevronUp size={18} color="#94a3b8"/> : <ChevronDown size={18} color="#94a3b8"/>}
        </div>
        <AnimatePresence>
          {showRef && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} style={{ overflow: 'hidden' }}>
              <div style={{ paddingTop: '1.5rem' }}>
                 <div style={styles.refGrid}>
                  {[
                    { title: "Anxiety (0-21)", rows: ["0–4 Minimal", "5–9 Mild", "10–14 Moderate", "15+ Severe"], link: "https://www.mdcalc.com/calc/1727/gad7-general-anxiety-disorder7" },
                    { title: "Depression (0-27)", rows: ["0–4 None", "5–9 Mild", "10–14 Moderate", "15+ Severe"], link: "https://www.mdcalc.com/calc/1725/phq9-patient-health-questionnaire-9" },
                    { title: "Likert (0-5)", rows: ["0 Very Low", "1 Low", "3 Moderate", "5 High"], link: null }
                  ].map((item, i) => (
                    <div key={i}>
                      <h4 style={styles.refColHeader}>🔹 {item.title}</h4>
                      <table style={styles.refTable}><tbody>{item.rows.map((r,j)=><tr key={j}><td style={styles.refTd}>{r}</td></tr>)}</tbody></table>
                      {item.link && <a href={item.link} target="_blank" rel="noreferrer" style={styles.refLink}>Calculator <ExternalLink size={10}/></a>}
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* MAIN INPUT FORM */}
      <form onSubmit={handleSubmit}>
        <div style={styles.grid}>
          {fieldGroups.map((group, idx) => (
            <motion.div key={idx} className="card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }} style={styles.inputCard}>
              <div style={styles.groupHeader}>
                {group.icon} <h3 style={styles.groupTitle}>{group.title}</h3>
              </div>
              <div style={{ display: 'grid', gap: '1rem' }}>
                {group.fields.map(f => (
                  <div key={f.name} className="input-group">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', alignItems: 'center' }}>
                      <label style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{f.label}</label>
                      <span style={styles.descBadge}>{f.desc}</span>
                    </div>
                    <input type="number" min="0" max={f.max} value={form[f.name]} onChange={e => setForm({...form, [f.name]: +e.target.value})} style={styles.inputField} />
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
        
        {/* ANIMATED LOADING BUTTON */}
        <motion.button 
          whileHover={!loading ? { scale: 1.02 } : {}} 
          whileTap={!loading ? { scale: 0.98 } : {}} 
          className="btn-primary" 
          disabled={loading}
          style={{ 
            ...styles.submitBtn, 
            opacity: loading ? 0.7 : 1, 
            cursor: loading ? 'not-allowed' : 'pointer' 
          }}
        >
          {loading ? (
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
              <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                <Loader2 size={20} /> 
              </motion.div>
              Analyzing...
            </span>
          ) : (
            "Run Analysis"
          )}
        </motion.button>

      </form>
    </motion.div>
  );
}

// --- STYLES ---
const styles = {
  heroContainer: { textAlign: 'center', marginBottom: '2.5rem', paddingTop: '0.5rem' },
  titleWrapper: { display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '0.5rem' },
  iconBox: { background: 'linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(244, 114, 182, 0.2))', padding: '10px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(255,255,255,0.1)' },
  title: { fontSize: '2.2rem', margin: 0, background: 'linear-gradient(to right, #a78bfa, #f472b6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 800, letterSpacing: '-0.5px' },
  subTitle: { color: '#94a3b8', fontSize: '1rem', marginTop: '5px' },
  resultCard: { background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9))', padding: '1.5rem', marginBottom: '2rem' },
  aiInsightBox: { background: 'rgba(255, 255, 255, 0.05)', padding: '1.2rem', marginTop: '1.2rem', borderRadius: '12px' },
  aiHeader: { marginTop: 0, color: '#facc15', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', marginBottom: '0.5rem' },
  closeButton: { marginTop: '1rem', background: 'transparent', border: '1px solid rgba(255,255,255,0.2)', color: '#94a3b8', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem' },
  collapsibleCard: { padding: '1rem 1.5rem', cursor: 'pointer', display: 'flex', flexDirection: 'column', marginBottom: '2rem' },
  collapsibleHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' },
  refTitle: { display: 'flex', alignItems: 'center', gap: '8px', margin: 0, fontSize: '1rem', color: '#e2e8f0' },
  refGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', alignItems: 'start' },
  refColHeader: { color: '#c4b5fd', marginTop: 0, fontSize: '0.9rem', marginBottom: '0.5rem' },
  refTable: { width: '100%', fontSize: '0.8rem', borderCollapse: 'collapse', color: '#cbd5e1' },
  refTd: { padding: '4px 0', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' },
  refLink: { color:'#ec4899', fontSize:'0.75rem', display: 'inline-flex', alignItems: 'center', gap: '4px', marginTop: '8px', textDecoration: 'none' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', alignItems: 'start' },
  inputCard: { padding: '1.5rem', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column' },
  groupHeader: { display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.2rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' },
  groupTitle: { margin: 0, fontSize: '1.1rem', color: '#e2e8f0' },
  descBadge: { fontSize: '0.7rem', color: '#64748b', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px' },
  inputField: { background: 'rgba(0, 0, 0, 0.2)', border: '1px solid rgba(255,255,255,0.1)', padding: '8px 12px', borderRadius: '8px', color: 'white', width: '100%', fontSize: '0.9rem' },
  submitBtn: { marginTop: '2rem', fontSize: '1.1rem', padding: '1rem', background: 'linear-gradient(to right, #8b5cf6, #ec4899)', boxShadow: '0 4px 20px rgba(236, 72, 153, 0.4)', width: '100%', border: 'none', borderRadius: '12px', color: 'white', cursor: 'pointer', fontWeight: 600 }
};
