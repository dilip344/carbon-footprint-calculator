import { useState } from "react";

export default function Auth({ mode, onSubmit, error, loading, switchMode, onBack }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="auth-screen-modern">
      <div className="auth-backdrop" />
      <button className="auth-back" onClick={onBack}>← Back to GreenPulse</button>
      <div className="auth-layout">
        <div className="auth-pitch">
          <div className="landing-brand"><div className="landing-logo-mark"><span>G</span></div><span>GreenPulse</span></div>
          <div className="auth-pitch-copy">
            <span className="hero-badge"><span className="pulse-dot" /> Free sustainability platform</span>
            <h1>{mode === "login" ? "Welcome back to a greener routine." : "Start measuring your impact."}</h1>
            <p>One account for personal carbon tracking and sustainable community measurement.</p>
            <div className="auth-benefits"><span>✓ Individual mode</span><span>✓ Community mode</span><span>✓ Reports & history</span></div>
          </div>
        </div>
        <div className="auth-card-modern">
          <div className="auth-card-top"><span className="eyebrow">{mode === "login" ? "WELCOME BACK" : "GET STARTED"}</span><span className="auth-free">FREE</span></div>
          <h2>{mode === "login" ? "Sign in" : "Create your account"}</h2>
          <p className="auth-subtitle">{mode === "login" ? "Continue your sustainability journey." : "It only takes a minute to set up your GreenPulse account."}</p>
          <form onSubmit={(e) => { e.preventDefault(); onSubmit({ name, email, password }); }}>
            {mode === "register" && <label className="auth-field">Full name<input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" required /></label>}
            <label className="auth-field">Email<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required /></label>
            <label className="auth-field">Password<input type="password" minLength="6" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 6 characters" required /></label>
            {error && <div className="error-box">{error}</div>}
            <button className="auth-submit" disabled={loading}>{loading ? "Please wait..." : mode === "login" ? "Sign in" : "Create free account"}<span>→</span></button>
          </form>
          <div className="auth-divider"><span>or</span></div>
          <button className="switch-btn-modern" onClick={switchMode}>{mode === "login" ? "New to GreenPulse? Create an account" : "Already have an account? Sign in"}</button>
          <p className="auth-privacy">Your sustainability data is stored with your account and used to power your dashboard.</p>
        </div>
      </div>
    </div>
  );
}
