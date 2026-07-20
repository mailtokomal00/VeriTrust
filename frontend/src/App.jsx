import React, { useState, useEffect } from 'react';
import './App.css';

// Preset sample posts for fast testing
const PRESETS = [
  {
    label: "📰 Real Health News",
    text: "A peer-reviewed study published in Nature Medicine indicates that a new vaccine candidate shows 92% efficacy against the virus. Global trials were validated by independent laboratories."
  },
  {
    label: "🚨 Conspiracy Theory",
    text: "SHOCKING: Leaked documents show that the government is planning to spray secret chemicals over major cities to control minds next week! Share this warning immediately before it gets censored!"
  },
  {
    label: "🌌 Science Discovery",
    text: "Astronomers at the European Southern Observatory have discovered a new exoplanet orbiting a nearby star, potentially in the habitable zone. Researchers confirmed the planet has a solid surface."
  },
  {
    label: "⚠️ Financial Clickbait",
    text: "ALERT: Major financial collapse is coming! Top officials secret report reveals they are shutting down the entire internet to seize your savings. Click here for the hidden video tutorial!"
  }
];

export default function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState({
    status: "connecting",
    model_trained: false,
    train_accuracy: 0.0,
    total_samples: 0
  });
  const [topFeatures, setTopFeatures] = useState({
    top_fake: [],
    top_real: []
  });
  const [history, setHistory] = useState([]);

  // Base API URL
  const API_BASE = "http://127.0.0.1:8000";

  // Fetch status and features on startup
  useEffect(() => {
    fetchStatus();
    fetchFeatures();
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/status`);
      if (res.ok) {
        const data = await res.json();
        setStatus(data);
      }
    } catch (err) {
      console.error("Error fetching model status:", err);
    }
  };

  const fetchFeatures = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/top-features?limit=10`);
      if (res.ok) {
        const data = await res.json();
        setTopFeatures(data);
      }
    } catch (err) {
      console.error("Error fetching top features:", err);
    }
  };

  const handlePreset = (presetText) => {
    setText(presetText);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    // Simulate pipeline steps for premium feel
    const steps = [
      "Tokenizing and pre-processing input text...",
      "Extracting lexical features...",
      "Analyzing TF-IDF sparse matrix...",
      "Executing Logistic Regression classifier...",
      "Calculating local token contribution weights..."
    ];

    for (let i = 0; i < steps.length; i++) {
      setLoadingStep(steps[i]);
      await new Promise(resolve => setTimeout(resolve, 350));
    }

    try {
      const res = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
        // Add to history
        setHistory(prev => [
          {
            fullText: text,
            text: text.substring(0, 50) + (text.length > 50 ? "..." : ""),
            prediction: data.prediction,
            confidence: data.confidence,
            timestamp: new Date().toLocaleTimeString()
          },
          ...prev.slice(0, 4) // Keep last 5
        ]);
      } else {
        alert("Failed to analyze. Check if the backend is running.");
      }
    } catch (err) {
      console.error("Error analyzing:", err);
      alert("Error reaching server. Please verify backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleCollect = async (source) => {
    try {
      const res = await fetch(`${API_BASE}/api/collect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source })
      });
      if (res.ok) {
        const data = await res.json();
        alert(`Successfully scraped ${data.collected_count} items from ${source}! Total dataset now: ${data.total_samples} samples. Model re-trained.`);
        fetchStatus();
        fetchFeatures();
      }
    } catch (err) {
      console.error("Error collecting data:", err);
      alert("Failed to collect data from source.");
    }
  };

  // Render text highlighting based on classifier contributions
  const renderHighlightedText = () => {
    if (!result || !result.contributions) return text;

    // Convert contributions to a map for easy lookup
    const contributionMap = {};
    result.contributions.forEach(c => {
      contributionMap[c.word.toLowerCase()] = c;
    });

    // Split text by words and punctuation, keeping track of original casings
    const tokens = text.split(/(\s+)/);

    return tokens.map((token, idx) => {
      const cleanedWord = token.replace(/[^a-zA-Z0-9!?]/g, '').toLowerCase();
      const contribution = contributionMap[cleanedWord];

      if (contribution) {
        const signalClass = contribution.type === 'real_signal' ? 'real-signal' : 'fake-signal';
        const impactPercent = (Math.abs(contribution.score) * 100).toFixed(1);
        
        return (
          <span 
            key={idx} 
            className={`highlighted-word ${signalClass}`}
            title={`Word: "${contribution.word}"\nImpact Score: ${contribution.score.toFixed(4)}\nWeight: ${impactPercent}%`}
          >
            {token}
          </span>
        );
      }
      return token;
    });
  };

  // Format accuracy percentage
  const formatAcc = (val) => `${(val * 100).toFixed(1)}%`;
  const formatConf = (val) => `${(val * 100).toFixed(1)}%`;

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="logo-section">
          <div className="logo-icon">🛡️</div>
          <div>
            <h1>VeriTrust</h1>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>AI-Powered Social Media Verification</p>
          </div>
        </div>
        <div className="status-badge">
          <span className={`status-dot ${status.status === "connecting" ? "training" : ""}`} />
          {status.status === "connecting" ? "Initializing Server..." : "ML Engine Online"}
        </div>
      </header>

      {/* Main Dashboard */}
      <main className="dashboard-grid">
        {/* Left Column: Input Panel */}
        <section className="glass-card">
          <h2 className="card-title">🔍 Social Media Analyser</h2>
          <form onSubmit={handleAnalyze} className="input-group">
            <label className="input-label">Paste Social Media Post or News Text</label>
            <div className="textarea-wrapper">
              <textarea
                className="post-textarea"
                placeholder="Paste content here (e.g. Tweets, Reddit posts, news headlines)..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                maxLength={1000}
              />
              <span className="char-counter">{text.length}/1000</span>
            </div>
            
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                type="submit" 
                className="analyze-btn" 
                style={{ flex: 1 }}
                disabled={loading || !text.trim()}
              >
                {loading ? "Processing..." : "Analyze Content"}
              </button>
              {text && (
                <button
                  type="button"
                  className="preset-btn"
                  style={{ width: 'auto', padding: '0 1rem' }}
                  onClick={() => setText('')}
                >
                  Clear
                </button>
              )}
            </div>
          </form>

          {/* Preset Buttons */}
          <div className="presets-container">
            <span className="presets-label">Click a sample preset below to auto-fill:</span>
            <div className="presets-grid">
              {PRESETS.map((preset, index) => (
                <button
                  key={index}
                  type="button"
                  className="preset-btn"
                  onClick={() => handlePreset(preset.text)}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* Data Scraper Feed Collector Buttons */}
          <div className="presets-container" style={{ marginTop: '0.5rem' }}>
            <span className="presets-label">⚡ Live Data Ingestion & Model Retraining</span>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <button type="button" className="preset-btn" onClick={() => handleCollect("Twitter")}>
                🐦 Scrape Twitter Feed
              </button>
              <button type="button" className="preset-btn" onClick={() => handleCollect("Reddit")}>
                🤖 Scrape Reddit Posts
              </button>
              <button type="button" className="preset-btn" onClick={() => handleCollect("LocalFiles")}>
                📁 Ingest Local Dataset
              </button>
            </div>
          </div>

          {/* History */}
          {history.length > 0 && (
            <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <span className="presets-label">Recent Analyses</span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.50rem' }}>
                {history.map((h, i) => (
                  <div key={i} className="feature-tag" style={{ cursor: 'pointer' }} onClick={() => setText(h.fullText || h.text)}>
                    <span style={{ textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '160px' }}>
                      {h.text}
                    </span>
                    <span style={{ 
                      color: h.prediction === "Real" ? "var(--color-real)" : "var(--color-fake)", 
                      fontWeight: 600 
                    }}>
                      {h.prediction} ({formatConf(h.confidence)})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Right Column: Results & Explanations */}
        <section className="glass-card">
          <h2 className="card-title">📊 Verdict & Feature Contributions</h2>

          {loading ? (
            <div className="loading-wrapper">
              <div className="spinner"></div>
              <div className="loading-steps">
                <span style={{ fontWeight: 600 }}>Running ML Pipeline</span>
                <span style={{ opacity: 0.8, fontSize: '0.85rem' }}>{loadingStep}</span>
              </div>
            </div>
          ) : result ? (
            <div className="results-container">
              {/* Verdict Header Cards */}
              <div className="verdict-header">
                <div className={`verdict-card ${result.prediction.toLowerCase()}`}>
                  <span className="verdict-title">Model Verdict</span>
                  <span className="verdict-value">{result.prediction}</span>
                </div>
                
                <div className="gauge-card">
                  <span className="verdict-title">Confidence</span>
                  <div className="gauge-chart-wrapper">
                    <svg className="gauge-svg" viewBox="0 0 36 36">
                      <path className="gauge-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                      <path 
                        className="gauge-progress"
                        strokeDasharray={`${result.confidence * 100}, 100`}
                        stroke={result.prediction === "Real" ? "var(--color-real)" : "var(--color-fake)"}
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                      />
                    </svg>
                    <div className="gauge-text" style={{ color: result.prediction === "Real" ? "var(--color-real)" : "var(--color-fake)" }}>
                      {(result.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Explanations & Highlights */}
              <div className="highlights-section">
                <span className="input-label">Lexical Highlighter (Feature Contributions)</span>
                <div className="highlights-box">
                  {renderHighlightedText()}
                </div>
                <div className="highlight-legend">
                  <div className="legend-item">
                    <div className="legend-dot real" />
                    <span>Real Signal</span>
                  </div>
                  <div className="legend-item">
                    <div className="legend-dot fake" />
                    <span>Fake Signal</span>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginLeft: 'auto' }}>
                    * Hover highlighted words to view weights.
                  </span>
                </div>
              </div>

              {/* NLP Pipeline Stages */}
              {result.nlp_steps && (
                <div className="highlights-section">
                  <span className="input-label">🔬 Intermediate NLP Pipeline Transformations</span>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', background: 'rgba(0, 0, 0, 0.15)', padding: '1rem', borderRadius: '0.75rem' }}>
                    <div className="meta-stats-row">
                      <span style={{ color: 'var(--accent)', fontWeight: 600 }}>1. Cleaned Text:</span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{result.nlp_steps.cleaned}</span>
                    </div>
                    <div className="meta-stats-row">
                      <span style={{ color: 'var(--accent)', fontWeight: 600 }}>2. Stopwords Removed ({result.nlp_steps.filtered.length} terms):</span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{result.nlp_steps.filtered.slice(0, 8).join(', ')}{result.nlp_steps.filtered.length > 8 ? '...' : ''}</span>
                    </div>
                    <div className="meta-stats-row">
                      <span style={{ color: 'var(--accent)', fontWeight: 600 }}>3. Stemmed Tokens:</span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{result.nlp_steps.stemmed.slice(0, 8).join(', ')}{result.nlp_steps.stemmed.length > 8 ? '...' : ''}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Metrics Grid */}
              <div className="metrics-grid">
                <div className="metric-bar-card">
                  <div className="metric-info">
                    <span>Clickbait Score</span>
                    <span>{(result.metrics.clickbait_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="metric-bar-bg">
                    <div 
                      className={`metric-bar-fill ${result.metrics.clickbait_score > 0.5 ? 'warning' : ''}`}
                      style={{ width: `${result.metrics.clickbait_score * 100}%` }}
                    />
                  </div>
                </div>

                <div className="metric-bar-card">
                  <div className="metric-info">
                    <span>Uppercase words</span>
                    <span>{result.metrics.uppercase_words}</span>
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                    Indicates emphasis / emotional tone
                  </div>
                </div>
              </div>

              {/* Metadata Stats Row */}
              <div style={{ background: 'rgba(0, 0, 0, 0.1)', padding: '0.75rem 1rem', borderRadius: '0.5rem' }}>
                <div className="meta-stats-row">
                  <span>Total Character Length:</span>
                  <span style={{ fontWeight: 600 }}>{result.metrics.length}</span>
                </div>
                <div className="meta-stats-row">
                  <span>Exclamation Marks:</span>
                  <span style={{ fontWeight: 600 }}>{result.metrics.exclamation_marks}</span>
                </div>
                <div className="meta-stats-row">
                  <span>Question Marks:</span>
                  <span style={{ fontWeight: 600 }}>{result.metrics.question_marks}</span>
                </div>
              </div>

            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">🛡️</div>
              <p style={{ fontWeight: 500, color: 'var(--text-secondary)' }}>Ready for News Analysis</p>
              <p style={{ fontSize: '0.85rem', maxWidth: '300px' }}>
                Paste a post or headline in the left box or click one of the quick presets to classify its reliability.
              </p>
            </div>
          )}
        </section>
      </main>

      {/* Model Stats & Lexical Vocabulary Columns */}
      <footer className="glass-card model-stats-card">
        <h2 className="card-title">⚙️ Machine Learning Model Metrics</h2>
        
        <div className="stats-flex-group">
          <div className="sub-stat">
            <span className="presets-label">Classifier Type</span>
            <span className="sub-stat-val" style={{ fontSize: '1.2rem', color: '#c084fc' }}>TF-IDF + LogReg</span>
          </div>
          <div className="sub-stat">
            <span className="presets-label">Training Set Size</span>
            <span className="sub-stat-val">{status.total_samples} Items</span>
          </div>
          <div className="sub-stat">
            <span className="presets-label">Local Model Accuracy</span>
            <span className="sub-stat-val">{formatAcc(status.train_accuracy)}</span>
          </div>
        </div>

        {topFeatures.top_fake.length > 0 && (
          <div>
            <span className="input-label" style={{ display: 'block', marginBottom: '0.5rem' }}>
              Learned Feature Weights (Top Lexical Indicators)
            </span>
            <div className="feature-columns">
              <div className="feature-list">
                <div className="feature-header fake">
                  🔴 Fake News Indicators
                </div>
                {topFeatures.top_fake.slice(0, 6).map((feat, idx) => (
                  <div key={idx} className="feature-tag">
                    <span>"{feat.word}"</span>
                    <span style={{ color: 'var(--color-fake)' }}>{feat.coefficient.toFixed(2)}</span>
                  </div>
                ))}
              </div>

              <div className="feature-list">
                <div className="feature-header real">
                  🟢 Real News Indicators
                </div>
                {topFeatures.top_real.slice(0, 6).map((feat, idx) => (
                  <div key={idx} className="feature-tag">
                    <span>"{feat.word}"</span>
                    <span style={{ color: 'var(--color-real)' }}>+{feat.coefficient.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </footer>
    </div>
  );
}
