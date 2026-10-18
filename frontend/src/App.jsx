import { useEffect, useState } from "react";
import Auth from "./components/Auth";
import Landing from "./components/Landing";
import Calculator from "./components/Calculator";
import CommunityCalculator from "./components/CommunityCalculator";
import { EmissionChart, ForecastChart } from "./components/Charts";
import {
  calculateCarbon,
  calculateCommunity,
  downloadReport,
  getHistory,
  getLatest,
  loginUser,
  registerUser,
} from "./services/api";
import "./styles.css";

const individualInitial = {
  travel_mode: "car", travel_km: 10, fuel_liters: 20, electricity_kwh: 150,
  lpg_kg: 6, water_liters: 100, waste_kg: 10, food_type: "mixed",
  flights: 0, paper_kg: 2, trees: 0,
};

const communityInitial = {
  entity_name: "", population: 100, travel_mode: "bus", travel_km: 5000,
  fuel_liters: 100, electricity_kwh: 5000, lpg_kg: 100, water_liters: 120000,
  waste_kg: 500, food_type: "mixed", flights: 0, paper_kg: 100, trees: 20,
};

const icons = { dashboard: "⌂", calculator: "▣", history: "◷", reports: "▤" };

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("gp_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [authMode, setAuthMode] = useState("login");
  const [showLanding, setShowLanding] = useState(true);
  const [mode, setMode] = useState("individual");
  const [page, setPage] = useState("dashboard");
  const [individualForm, setIndividualForm] = useState(individualInitial);
  const [communityForm, setCommunityForm] = useState(communityInitial);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user) loadMode(mode);
  }, [user, mode]);

  async function loadMode(nextMode) {
    try {
      setError("");
      const [latest, rows] = await Promise.all([
        getLatest(user.user_id, nextMode),
        getHistory(user.user_id, nextMode),
      ]);
      setResult(latest.record ? latest : null);
      setHistory(rows);
    } catch {
      setError("Backend is not reachable. Start FastAPI and refresh the page.");
    }
  }

  async function handleAuth(data) {
    setLoading(true); setError("");
    try {
      const account = authMode === "login"
        ? await loginUser({ email: data.email, password: data.password })
        : await registerUser(data);
      localStorage.setItem("gp_user", JSON.stringify(account));
      setUser(account);
      setPage("dashboard");
    } catch (e) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  async function handleCalculate(e) {
    e.preventDefault(); setLoading(true); setError("");
    try {
      const data = mode === "individual"
        ? await calculateCarbon(user.user_id, individualForm)
        : await calculateCommunity(user.user_id, communityForm);
      setResult(data);
      setHistory(await getHistory(user.user_id, mode));
      setPage("dashboard");
    } catch (e) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  function switchMode(nextMode) {
    if (nextMode === mode) return;
    setMode(nextMode);
    setPage("dashboard");
    setError("");
  }

  function logout() {
    localStorage.removeItem("gp_user");
    setUser(null); setResult(null); setHistory([]); setPage("dashboard");
  }

  async function report(id = result?.id) {
    if (!id) { setError("Create a calculation before downloading a report."); return; }
    try { await downloadReport(id); } catch (e) { setError(e.message); }
  }

  if (!user && showLanding) {
    return <Landing
      onGetStarted={() => { setAuthMode("register"); setShowLanding(false); }}
      onLogin={() => { setAuthMode("login"); setShowLanding(false); }}
    />;
  }

  if (!user) {
    return (
      <Auth
        mode={authMode}
        onSubmit={handleAuth}
        error={error}
        loading={loading}
        onBack={() => { setError(""); setShowLanding(true); }}
        switchMode={() => {
          setError("");
          setAuthMode((m) => m === "login" ? "register" : "login");
        }}
      />
    );
  }

  const title = page === "dashboard" ? (mode === "individual" ? "Personal Dashboard" : "Community Dashboard")
    : page === "calculator" ? (mode === "individual" ? "Personal Calculator" : "Community Calculator")
    : page === "history" ? "Calculation History" : "Reports";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="leaf-logo">G</div>
          <div><strong>GreenPulse</strong><small>Carbon Intelligence</small></div>
        </div>

        <div className="mode-switch">
          <div className="menu-label">MODE</div>
          <div className="mode-toggle">
            <button className={mode === "individual" ? "selected" : ""} onClick={() => switchMode("individual")}>Person</button>
            <button className={mode === "community" ? "selected" : ""} onClick={() => switchMode("community")}>Community</button>
          </div>
          <p>{mode === "individual" ? "Your personal lifestyle footprint" : "Shared impact for a group or campus"}</p>
        </div>

        <div className="sidebar-menu">
          <div className="menu-label">WORKSPACE</div>
          {["dashboard", "calculator", "history", "reports"].map((item) => (
            <button key={item} className={`side-link ${page === item ? "active" : ""}`} onClick={() => setPage(item)}>
              <span className="side-icon">{icons[item]}</span>
              <span>{item[0].toUpperCase() + item.slice(1)}</span>
              {item === "reports" && history.length > 0 && <em>{history.length}</em>}
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">
          <div className="impact-card">
            <div className="impact-icon">♧</div>
            <strong>{mode === "individual" ? "Small actions matter" : "Collective action matters"}</strong>
            <p>{mode === "individual" ? "Track. Reduce. Repeat." : "Measure. Mobilize. Improve."}</p>
          </div>
          <button className="logout-btn" onClick={logout}><span>↪</span> Logout</button>
        </div>
      </aside>

      <div className="main-shell">
        <header className="topbar">
          <span className="topbar-title">{title}</span>
          <div className="top-user">
            <div className="mode-badge">{mode === "individual" ? "PERSON" : "COMMUNITY"}</div>
            <div className="avatar">{user.name?.charAt(0)?.toUpperCase() || "U"}</div>
            <div className="user-copy"><strong>{user.name}</strong><small>{user.email}</small></div>
          </div>
        </header>

        <main className="content">
          {error && <div className="error-box global-error"><span>{error}</span><button onClick={() => setError("")}>×</button></div>}

          {page === "dashboard" && (
            <Dashboard result={result} user={user} mode={mode} onCalculate={() => setPage("calculator")} onReport={() => report()} />
          )}

          {page === "calculator" && (
            <>
              <PageHeader
                eyebrow={mode === "individual" ? "PERSONAL CALCULATOR" : "COMMUNITY CALCULATOR"}
                title={mode === "individual" ? "Measure your footprint" : "Measure a shared footprint"}
                description={mode === "individual"
                  ? "Enter your normal activity levels and get a transparent monthly and annual CO₂e estimate."
                  : "Measure the combined footprint of a campus, NGO, school, village, office or community using aggregate monthly activity data."}
              />
              {mode === "individual"
                ? <Calculator form={individualForm} setForm={setIndividualForm} onSubmit={handleCalculate} loading={loading} />
                : <CommunityCalculator form={communityForm} setForm={setCommunityForm} onSubmit={handleCalculate} loading={loading} />}
            </>
          )}

          {page === "history" && <HistoryPage rows={history} mode={mode} onReport={report} onCalculate={() => setPage("calculator")} />}
          {page === "reports" && <ReportsPage rows={history} mode={mode} onReport={report} onCalculate={() => setPage("calculator")} />}
        </main>

        <footer className="app-footer">
          <span>GreenPulse</span>
          <span>{mode === "individual" ? "Personal sustainability" : "Sustainable communities"} • Climate Action</span>
        </footer>
      </div>
    </div>
  );
}

function PageHeader({ eyebrow, title, description }) {
  return <div className="page-header"><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{description}</p></div>;
}

function Dashboard({ result, user, mode, onCalculate, onReport }) {
  if (!result) {
    return (
      <div className={`empty-dashboard ${mode === "community" ? "empty-community" : ""}`}>
        <div className="empty-orbit"><div className="empty-illustration">{mode === "individual" ? "G" : "◎"}</div></div>
        <span className="eyebrow">{mode === "individual" ? "PERSONAL MODE" : "COMMUNITY MODE"}</span>
        <h1>{mode === "individual" ? "Start measuring your footprint" : "Start measuring your community"}</h1>
        <p>{mode === "individual"
          ? "Create your first assessment to understand your impact, discover your biggest sources and build a practical reduction plan."
          : "Create a community assessment to see total emissions, per-person impact and the highest-value reduction opportunities."}</p>
        <div className="empty-actions">
          <button className="primary-btn compact" onClick={onCalculate}>Start a new assessment <span>→</span></button>
          <span>Free • Private • Built for real-world sustainability</span>
        </div>
      </div>
    );
  }

  const breakdown = result.breakdown || {};
  const topContributor = Object.entries(breakdown)
    .filter(([key, value]) => !["Total", "Tree offset"].includes(key) && Number(value) > 0)
    .sort((a, b) => Number(b[1]) - Number(a[1]))[0];
  const peer = Number(result.peer_average || 0);
  const annual = Number(result.annual_emissions || 0);
  const score = Math.max(0, Math.min(100, Number(result.sustainability_score || 0)));
  const benchmarkText = peer > 0
    ? annual <= peer ? `${((1 - annual / peer) * 100).toFixed(0)}% below benchmark` : `${((annual / peer - 1) * 100).toFixed(0)}% above benchmark`
    : "Based on your latest assessment";
  const scoreLabel = score >= 80 ? "Excellent" : score >= 60 ? "Good progress" : score >= 40 ? "Growing" : "Getting started";

  return (
    <div className="dashboard-page">
      <section className={`dashboard-hero ${mode === "community" ? "community-dashboard-hero" : ""}`}>
        <div className="dashboard-hero-copy">
          <span className="eyebrow">{mode === "individual" ? "YOUR SUSTAINABILITY SPACE" : "COMMUNITY IMPACT SPACE"}</span>
          <h1>{mode === "individual" ? `Good to see you, ${user.name}!` : `Welcome to ${result.entity_name || "your community"}`}</h1>
          <p>{mode === "individual"
            ? "Your latest footprint is ready. Explore what is driving it and choose one action to improve your next score."
            : "Your shared footprint is ready. Turn collective data into clear priorities for your campus, NGO, school or community."}</p>
          <div className="hero-inline-actions">
            <button className="hero-action primary" onClick={onCalculate}>New assessment <span>↗</span></button>
            <button className="hero-action" onClick={onReport}>Download report <span>↓</span></button>
          </div>
        </div>
        <div className="score-orb">
          <div className="score-ring" style={{"--score": `${score * 3.6}deg`}}><div><strong>{score.toFixed(0)}</strong><span>score / 100</span></div></div>
          <small>{scoreLabel}</small>
        </div>
        <div className="hero-decoration"><span>+</span><span>•</span><span>+</span></div>
      </section>

      <div className="dashboard-context">
        <div><span className="context-dot" /> Latest assessment <strong>{mode === "individual" ? "Personal footprint" : result.entity_name || "Community footprint"}</strong></div>
        <span>Updated from your most recent calculation</span>
      </div>

      <div className="metric-grid enhanced-metrics">
        <Metric label="Monthly Emission" value={Number(result.monthly_emissions).toFixed(1)} unit="kg CO₂e" note={mode === "individual" ? "Your current monthly impact" : "Combined community impact"} icon="◒" tone="green" />
        <Metric label="Annual Emission" value={Number(result.annual_emissions).toFixed(1)} unit="kg CO₂e" note={mode === "individual" ? "Projected from this month" : `${result.population || 1} people included`} icon="◫" tone="blue" />
        <Metric label={mode === "individual" ? "Sustainability Score" : "Per-Person / Month"} value={mode === "individual" ? score.toFixed(0) : Number(result.per_person_monthly || 0).toFixed(1)} unit={mode === "individual" ? "/ 100" : "kg CO₂e"} note={mode === "individual" ? scoreLabel : "Community intensity"} icon="↗" tone="purple" />
        <Metric label="Annual Projection" value={Number(result.prediction).toFixed(1)} unit="kg CO₂e" note={benchmarkText} icon="◇" tone="orange" />
      </div>

      {result.fusion && (
        <section className="card fusion-card modern-card">
          <div className="section-title-row">
            <div><span className="eyebrow">ADAPTIVE FUSION</span><h2>How your final estimate was built</h2><p>The formula and Random Forest are combined using a dynamic confidence weight.</p></div>
            <div className={`fusion-confidence ${Number(result.fusion.confidence_weight) >= 0.6 ? "high" : Number(result.fusion.confidence_weight) >= 0.35 ? "medium" : "low"}`}>{(Number(result.fusion.confidence_weight) * 100).toFixed(0)}% AI confidence</div>
          </div>
          <div className="fusion-grid">
            <div><span>Final fused estimate</span><strong>{Number(result.fusion.fused_estimate).toFixed(1)} kg</strong><small>Primary result</small></div>
            <div><span>Deterministic formula</span><strong>{Number(result.fusion.deterministic_estimate).toFixed(1)} kg</strong><small>D — rule-based estimate</small></div>
            <div><span>Random Forest</span><strong>{Number(result.fusion.ml_estimate).toFixed(1)} kg</strong><small>M — learned estimate</small></div>
            <div><span>Trust signals</span><strong>S1 {Number(result.fusion.s1_distance).toFixed(2)} · S2 {Number(result.fusion.s2_density).toFixed(2)} · S3 {Number(result.fusion.s3_residual).toFixed(2)}</strong><small>{result.fusion.divergence_flag ? "Divergence detected and recorded" : "Estimates within the dynamic threshold"}</small></div>
          </div>
        </section>
      )}

      {mode === "community" && (
        <div className="community-strip enhanced-community-strip">
          <div><span>Community size</span><strong>{result.population || 0} people</strong><small>Included in this assessment</small></div>
          <div><span>Per-person annual</span><strong>{Number(result.per_person_annual || 0).toFixed(1)} kg</strong><small>Annual impact intensity</small></div>
          <div><span>Impact focus</span><strong>{topContributor?.[0] || "Building profile"}</strong><small>Largest current contributor</small></div>
        </div>
      )}

      <div className="dashboard-section-heading"><div><span className="eyebrow">UNDERSTAND YOUR IMPACT</span><h2>Where your emissions come from</h2></div><p>Use the charts to spot the areas where a small change can create the biggest difference.</p></div>
      <div className="chart-grid"><EmissionChart breakdown={breakdown} /><ForecastChart forecast={result.forecast} /></div>

      <div className="dashboard-section-heading compact-heading"><div><span className="eyebrow">TAKE ACTION</span><h2>Turn insight into progress</h2></div></div>
      <div className="lower-grid enhanced-lower-grid">
        <div className="card lifestyle-card modern-card">
          <div className="card-heading"><div><h3>{mode === "individual" ? "Your lifestyle pattern" : "Community pattern"}</h3><p>Based on the activity in this assessment</p></div><span className="people-icon">●●</span></div>
          <div className="lifestyle-value">{result.cluster}</div>
          <p className="lifestyle-copy">{mode === "individual" ? "Your activity is grouped with similar emission patterns to make benchmarking easier." : "This community is grouped with similar activity patterns to support practical comparison."}</p>
          <div className="score-bar"><div style={{ width: `${score}%` }} /></div>
          <div className="score-caption"><span>Sustainability score</span><strong>{score.toFixed(0)} / 100</strong></div>
        </div>

        <div className="card contributor-card modern-card">
          <div className="card-heading"><div><h3>Biggest opportunity</h3><p>Your highest emission source</p></div><span className="bolt">ϟ</span></div>
          <div className="contributor-name">{topContributor?.[0] || "—"}</div>
          <div className="contributor-value">{topContributor ? Number(topContributor[1]).toFixed(1) : "0.0"} kg CO₂e</div>
          <p>{topContributor && breakdown.Total ? `${((Number(topContributor[1]) / Number(breakdown.Total)) * 100).toFixed(1)}% of ${mode === "individual" ? "your" : "the community's"} monthly emissions` : "Complete another calculation to compare sources."}</p>
        </div>

        <div className="card recommendations-card modern-card">
          <div className="card-heading"><div><h3>Smart recommendations</h3><p>Practical actions based on your footprint</p></div><span className="check-icon">✓</span></div>
          <div className="mini-recommendations">{(result.recommendations || []).slice(0, 4).map((item, index) => <div key={index}><span>✓</span><p>{item}</p></div>)}</div>
        </div>
      </div>

      <div className="card breakdown-card modern-breakdown">
        <div className="section-title-row"><div><span className="eyebrow">TRANSPARENT DATA</span><h2>Emission breakdown</h2><p>Every category contributing to the latest calculation.</p></div><span className="total-pill">Total {Number(breakdown.Total || 0).toFixed(2)} kg CO₂e</span></div>
        <div className="breakdown-grid">{Object.entries(breakdown).map(([key, value]) => <div className="breakdown-item" key={key}><span>{key}</span><strong>{Number(value).toFixed(2)} kg</strong></div>)}</div>
      </div>

      <div className="dashboard-bottom-note"><span>♧</span><div><strong>One better choice at a time.</strong><p>Come back after your next assessment to see how your footprint changes.</p></div><button onClick={onCalculate}>Update footprint →</button></div>
    </div>
  );
}
function Metric({ label, value, unit, note, icon, tone }) {
  return <div className={`metric-card ${tone}`}><div className="metric-top"><span>{label}</span><i>{icon}</i></div><strong>{value}</strong><small>{unit}</small><p>{note}</p></div>;
}

function HistoryPage({ rows, mode, onReport, onCalculate }) {
  return <div><PageHeader eyebrow="HISTORY" title={`${mode === "individual" ? "Personal" : "Community"} calculation history`} description="Review previous assessments and compare your progress over time." /><HistoryTable rows={rows} mode={mode} onReport={onReport} onCalculate={onCalculate} /></div>;
}

function ReportsPage({ rows, mode, onReport, onCalculate }) {
  return <div><PageHeader eyebrow="REPORTS" title={`${mode === "individual" ? "Personal" : "Community"} reports`} description="Download a clean PDF report for any completed assessment." />
    {rows.length === 0 ? <div className="empty-card"><div className="empty-icon">▤</div><h2>No reports yet</h2><p>Complete an assessment to generate a downloadable PDF.</p><button className="green-btn" onClick={onCalculate}>Create report</button></div>
      : <div className="report-grid">{rows.map((row, index) => <div className="report-card" key={row.id}><div className="report-file-icon">PDF</div><div className="report-main"><strong>{mode === "individual" ? "Personal" : row.entity_name || "Community"} Report #{rows.length - index}</strong><span>{row.date}</span><div><b>{Number(row.monthly_emissions).toFixed(1)} kg</b><span>monthly • score {Number(row.score).toFixed(1)}/100</span></div></div><button className="download-icon-btn" onClick={() => onReport(row.id)} title="Download PDF">↓</button></div>)}</div>}
  </div>;
}

function HistoryTable({ rows, mode, onReport, onCalculate }) {
  return <div className="card history-card">{rows.length === 0 ? <div className="table-empty"><h2>No calculations yet</h2><p>Your completed assessments will appear here.</p><button className="green-btn" onClick={onCalculate}>Create first calculation</button></div>
    : <div className="table-scroll"><table><thead><tr><th>Date</th>{mode === "community" && <th>Community</th>}<th>Monthly</th><th>Annual</th><th>Score</th><th>Pattern</th><th>Report</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id}><td>{row.date}</td>{mode === "community" && <td>{row.entity_name}</td>}<td>{Number(row.monthly_emissions).toFixed(1)} kg</td><td>{Number(row.annual_emissions).toFixed(1)} kg</td><td><span className="score-chip">{Number(row.score).toFixed(1)}</span></td><td>{row.cluster}</td><td><button className="download-text-btn" onClick={() => onReport(row.id)}>Download PDF</button></td></tr>)}</tbody></table></div>}
  </div>;
}
