import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Brain, Activity, HeartPulse, Users, BarChart2 } from 'lucide-react';

export default function ReferencePage() {
  
  // --- DATA CONFIGURATION ---
  const ANXIETY_DATA = [
    ["0–4", "Minimal", "Low Stress"], 
    ["5–9", "Mild", "Moderate Stress"], 
    ["10–14", "Moderate", "High Stress"], 
    ["15–21", "Severe", "Very High"]
  ];
  
  const DEPRESSION_DATA = [
    ["0–4", "Minimal", "Low Risk"], 
    ["5–9", "Mild", "Mild Risk"], 
    ["10–14", "Moderate", "Medium Risk"], 
    ["15–19", "Mod. Severe", "High Risk"], 
    ["20–27", "Severe", "Critical Risk"]
  ];
  
  const SELF_ESTEEM_DATA = [
    ["0–10", "Low", "Vulnerable"], 
    ["11–20", "Moderate", "Normal"], 
    ["21–30", "High", "Strong"]
  ];
  
  const BP_DATA = [
    ["0", "Normal", "Low"], 
    ["1", "Elevated", "Moderate"], 
    ["2", "Stage 1", "High"], 
    ["3", "Stage 2", "Very High"]
  ];
  
  const SOCIAL_DATA = [
    ["0", "None", "None (High Risk)"], 
    ["1", "Weak", "Low"], 
    ["2", "Good", "Moderate"], 
    ["3", "Strong", "High (Safe)"]
  ];
  
  const LIKERT_DATA = [
    ["0", "Very Low / None"], 
    ["1", "Low / Poor"], 
    ["2", "Slightly Low"], 
    ["3", "Moderate"], 
    ["4", "High / Good"], 
    ["5", "Very High / Excellent"]
  ];

  // --- RENDER ---
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      
      {/* HERO SECTION */}
      <div style={styles.heroContainer}>
        <div style={styles.titleWrapper}>
            <div style={styles.iconBox}>
                <Activity size={32} color="#ec4899" strokeWidth={2.5} />
            </div>
            <h1 style={styles.title}>MindEase Library</h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '1rem', marginTop: '8px' }}>
          Standardized clinical scales and interpretation metrics.
        </p>
      </div>

      {/* MAIN GRID */}
      <div style={styles.grid}>
        
        <ReferenceCard 
          icon={<Brain size={22} color="#a78bfa" />} 
          title="Anxiety (GAD-7)" 
          headers={['Score', 'Severity', 'Impact']} 
          data={ANXIETY_DATA} 
          link="https://www.mdcalc.com/calc/1727/gad7-general-anxiety-disorder7" 
        />
        
        <ReferenceCard 
          icon={<Activity size={22} color="#f472b6" />} 
          title="Depression (PHQ-9)" 
          headers={['Score', 'Severity', 'Impact']} 
          data={DEPRESSION_DATA} 
          link="https://www.mdcalc.com/calc/1725/phq9-patient-health-questionnaire-9" 
        />
        
        <ReferenceCard 
          icon={<Users size={22} color="#38bdf8" />} 
          title="Self-Esteem Scale" 
          headers={['Score', 'Level', 'Resilience']} 
          data={SELF_ESTEEM_DATA} 
        />
        
        <ReferenceCard 
          icon={<HeartPulse size={22} color="#ef4444" />} 
          title="Blood Pressure" 
          desc="Simplified categorization for stress impact analysis." 
          headers={['Input', 'Category', 'Stress Load']} 
          data={BP_DATA} 
        />
        
        <ReferenceCard 
          icon={<Users size={22} color="#facc15" />} 
          title="Social Support" 
          headers={['Input', 'Level', 'Protective Factor']} 
          data={SOCIAL_DATA} 
        />
        
        <ReferenceCard 
          icon={<BarChart2 size={22} color="#4ade80" />} 
          title="Standard Likert Scale" 
          desc="Used for subjective metrics like Sleep Quality and Study Load." 
          headers={['Input', 'Meaning']} 
          data={LIKERT_DATA} 
        />

      </div>
    </motion.div>
  );
}

// --- SUB-COMPONENT ---
const ReferenceCard = ({ icon, title, desc, headers, data, link }) => (
  <motion.div 
    className="card" 
    style={styles.card} 
    initial={{ y: 20, opacity: 0 }} 
    whileInView={{ y: 0, opacity: 1 }} 
    viewport={{ once: true }}
  >
    <h3 style={styles.cardTitle}>{icon} {title}</h3>
    {desc && <p style={styles.cardDesc}>{desc}</p>}
    
    <table style={styles.table}>
      <thead>
        <tr>
          {headers.map((h, i) => <th key={i} style={styles.th}>{h}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.map((r, i) => (
          <tr key={i}>
            {r.map((c, j) => <td key={j} style={styles.td}>{c}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
    
    {link && (
      <a href={link} target="_blank" rel="noreferrer" style={styles.link}>
        Open Official Calculator <ExternalLink size={14} />
      </a>
    )}
  </motion.div>
);

// --- STYLES OBJECT ---
const styles = {
  heroContainer: { textAlign: 'center', marginBottom: '2.5rem', paddingTop: '0.5rem' },
  titleWrapper: { display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '0.5rem' },
  iconBox: { background: 'linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(244, 114, 182, 0.2))', padding: '10px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 20px rgba(236, 72, 153, 0.15)', border: '1px solid rgba(255,255,255,0.1)' },
  title: { fontSize: '2.2rem', margin: 0, background: 'linear-gradient(to right, #ec4899, #f472b6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 800, letterSpacing: '-0.5px' },
  
  // Grid layout with tighter gaps
  grid: { 
    display: 'grid', 
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
    gap: '1.5rem', 
    alignItems: 'start' 
  },
  
  // Compact card style
  card: { padding: '1.5rem', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column' },
  cardTitle: { margin: 0, marginBottom: '1rem', fontSize: '1.1rem', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.8rem' },
  cardDesc: { fontSize: '0.85rem', color: '#94a3b8', marginBottom: '1rem', lineHeight: '1.4' },
  
  // Compact table
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', color: '#cbd5e1', marginBottom: 'auto' },
  th: { textAlign: 'left', padding: '8px 10px', borderBottom: '1px solid rgba(255, 255, 255, 0.2)', color: '#a78bfa', fontWeight: 600, fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' },
  td: { padding: '8px 10px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)', verticalAlign: 'top' },
  
  link: { color: '#ec4899', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', marginTop: '1.5rem', padding: '8px 12px', background: 'rgba(236, 72, 153, 0.1)', borderRadius: '6px', transition: 'all 0.2s', fontWeight: 500 }
};