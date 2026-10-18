const Arrow = () => <span aria-hidden="true">↗</span>;

function LeafMark() {
  return <div className="landing-logo-mark"><span>G</span></div>;
}

function MiniChart() {
  return (
    <div className="mini-chart" aria-hidden="true">
      <svg viewBox="0 0 420 150" preserveAspectRatio="none">
        <defs>
          <linearGradient id="area" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#9ce7b6" stopOpacity=".32" />
            <stop offset="100%" stopColor="#9ce7b6" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d="M0 112 C35 106 45 92 76 98 S121 83 150 88 S191 58 220 72 S270 52 299 61 S346 38 372 47 S401 29 420 34 V150 H0 Z" fill="url(#area)" />
        <path d="M0 112 C35 106 45 92 76 98 S121 83 150 88 S191 58 220 72 S270 52 299 61 S346 38 372 47 S401 29 420 34" fill="none" stroke="#9ce7b6" strokeWidth="4" strokeLinecap="round" />
      </svg>
    </div>
  );
}

function DashboardPreview() {
  return (
    <div className="preview-window">
      <div className="preview-sidebar">
        <div className="preview-side-logo"><LeafMark /></div>
        <div className="preview-side-item active"><span>⌂</span> Overview</div>
        <div className="preview-side-item"><span>◌</span> Calculator</div>
        <div className="preview-side-item"><span>↗</span> Insights</div>
        <div className="preview-side-item"><span>◷</span> History</div>
        <div className="preview-side-item"><span>▤</span> Reports</div>
        <div className="preview-side-bottom"><span className="preview-avatar">G</span></div>
      </div>
      <div className="preview-main">
        <div className="preview-topline">
          <div><small>PERSONAL MODE</small><h3>Your sustainability overview</h3></div>
          <span className="preview-mode">Individual</span>
        </div>
        <div className="preview-metrics">
          <div><small>MONTHLY FOOTPRINT</small><strong>214.8 <em>kg CO₂e</em></strong><span className="positive">↓ 8.4% this month</span></div>
          <div><small>SUSTAINABILITY SCORE</small><strong>82<span>/100</span></strong><span>Excellent progress</span></div>
          <div><small>TOP CONTRIBUTOR</small><strong>Travel</strong><span>46% of footprint</span></div>
        </div>
        <div className="preview-grid">
          <div className="preview-card preview-chart-card"><div className="preview-card-title"><span>Emissions trend</span><b>6 months</b></div><MiniChart /><div className="preview-chart-axis"><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span></div></div>
          <div className="preview-card preview-score-card"><div className="preview-card-title"><span>Impact mix</span><b>Monthly</b></div><div className="preview-ring"><div><strong>214</strong><span>kg CO₂e</span></div></div><div className="preview-legend"><span><i className="dot travel" />Travel <b>46%</b></span><span><i className="dot energy" />Energy <b>29%</b></span><span><i className="dot home" />Home <b>25%</b></span></div></div>
        </div>
      </div>
    </div>
  );
}

export default function Landing({ onGetStarted, onLogin }) {
  const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });

  return (
    <div className="landing-page">
      <header className="landing-nav">
        <button className="landing-brand" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
          <LeafMark />
          <span>GreenPulse</span>
        </button>
        <nav className="landing-links" aria-label="Primary navigation">
          <button onClick={() => scrollTo("about")}>About</button>
          <button onClick={() => scrollTo("features")}>Features</button>
          <button onClick={() => scrollTo("community")}>Community</button>
          <button onClick={() => scrollTo("how-it-works")}>How it works</button>
          <button onClick={() => scrollTo("contact")}>Contact</button>
        </nav>
        <div className="landing-actions">
          <button className="nav-login" onClick={onLogin}>Login</button>
          <button className="nav-cta" onClick={onGetStarted}>Get started <Arrow /></button>
        </div>
      </header>

      <main>
        <section className="hero-section">
          <div className="hero-glow hero-glow-one" />
          <div className="hero-glow hero-glow-two" />
          <div className="hero-content">
            <div className="hero-badge"><span className="pulse-dot" /> Free carbon intelligence for people & communities</div>
            <h1>Make your impact<br /><span>visible.</span> Make it better.</h1>
            <p>Measure everyday emissions, understand what drives them, and turn the numbers into practical climate action — for one person or an entire community.</p>
            <div className="hero-buttons">
              <button className="hero-primary" onClick={onGetStarted}>Start measuring free <Arrow /></button>
              <button className="hero-secondary" onClick={() => scrollTo("features")}>Explore features <span>↓</span></button>
            </div>
            <div className="hero-trust"><span>✓ No paid plans</span><span>✓ Personal & community modes</span><span>✓ Your data stays in your account</span></div>
          </div>
          <div className="hero-preview"><DashboardPreview /></div>
        </section>

        <section className="stats-strip">
          <div><strong>01</strong><span>Measure</span><p>Track travel, energy, water, waste, food and more.</p></div>
          <div><strong>02</strong><span>Understand</span><p>See the categories creating the biggest impact.</p></div>
          <div><strong>03</strong><span>Improve</span><p>Get focused actions and follow your progress.</p></div>
          <div><strong>04</strong><span>Share</span><p>Turn individual progress into community action.</p></div>
        </section>

        <section id="about" className="story-section section-light">
          <div className="section-kicker">ONE PLATFORM · TWO WAYS TO ACT</div>
          <div className="story-grid">
            <div><h2>Small choices become meaningful when you can see them.</h2></div>
            <div><p>GreenPulse is designed for real life. A person can understand their own footprint, while a college, NGO, school, village or workplace can measure collective impact using the same platform.</p><p>The goal is simple: replace vague sustainability goals with measurable progress.</p></div>
          </div>
        </section>

        <section id="features" className="features-section section-dark">
          <div className="section-heading centered"><div className="section-kicker light">BUILT FOR ACTION</div><h2>Everything you need to move<br /><span>from numbers to action.</span></h2><p>Clear dashboards, meaningful comparisons and practical recommendations — without making sustainability complicated.</p></div>
          <div className="feature-grid">
            <article className="feature-card feature-large"><div className="feature-number">01</div><div className="feature-icon">◒</div><h3>Personal footprint</h3><p>Understand your monthly and annual emissions across transport, electricity, LPG, water, waste, food, flights and paper.</p><div className="feature-tags"><span>Individual</span><span>History</span><span>Score</span></div></article>
            <article className="feature-card"><div className="feature-number">02</div><div className="feature-icon">◎</div><h3>Community impact</h3><p>Measure a shared footprint for campuses, NGOs, schools, villages and teams — including per-person impact.</p><div className="feature-tags"><span>Campus</span><span>NGO</span><span>Village</span></div></article>
            <article className="feature-card"><div className="feature-number">03</div><div className="feature-icon">↗</div><h3>Smart insights</h3><p>Identify your biggest emission sources and receive focused recommendations based on the data you provide.</p><div className="feature-tags"><span>Insights</span><span>Recommendations</span></div></article>
            <article className="feature-card"><div className="feature-number">04</div><div className="feature-icon">⌁</div><h3>Future forecast</h3><p>Use historical calculations to see how emissions may change over the next six months.</p><div className="feature-tags"><span>Forecast</span><span>Trends</span></div></article>
            <article className="feature-card feature-wide"><div><div className="feature-number">05</div><div className="feature-icon">▤</div></div><div><h3>Reports you can use</h3><p>Keep your calculation history organized and generate a clean PDF report for personal records, project reviews or community presentations.</p></div><button onClick={onGetStarted}>See the dashboard <Arrow /></button></article>
          </div>
        </section>

        <section id="community" className="community-section">
          <div className="community-copy"><div className="section-kicker">COMMUNITY MODE</div><h2>One person can start it.<br /><span>A community can scale it.</span></h2><p>Switch from Individual to Community mode whenever you need to measure a larger group. The same account, the same platform, a wider impact.</p><button className="outline-dark" onClick={onGetStarted}>Explore community mode <Arrow /></button></div>
          <div className="community-visual"><div className="community-orbit orbit-one" /><div className="community-orbit orbit-two" /><div className="community-center"><span>GREEN</span><strong>Impact</strong><small>together</small></div><div className="community-node node-one">Campus</div><div className="community-node node-two">NGO</div><div className="community-node node-three">School</div><div className="community-node node-four">Village</div></div>
        </section>

        <section id="how-it-works" className="steps-section section-light">
          <div className="section-heading centered"><div className="section-kicker">HOW IT WORKS</div><h2>A simple loop for lasting progress.</h2></div>
          <div className="steps-grid"><div><span>01</span><h3>Create your account</h3><p>Start with a free account and choose the mode that matches your goal.</p></div><div><span>02</span><h3>Enter your activity</h3><p>Add your normal monthly or daily activity data in a guided calculator.</p></div><div><span>03</span><h3>Understand your impact</h3><p>See totals, major contributors, score, trends and personalized actions.</p></div><div><span>04</span><h3>Measure again</h3><p>Return to your dashboard and watch your progress over time.</p></div></div>
        </section>

        <section className="cta-section"><div className="cta-inner"><div className="section-kicker light">START TODAY</div><h2>Know your footprint.<br /><span>Change what comes next.</span></h2><p>GreenPulse is free to use — because better climate decisions should be accessible to everyone.</p><button onClick={onGetStarted}>Create your free account <Arrow /></button></div></section>

        <section id="contact" className="contact-section"><div><div className="landing-brand footer-brand"><LeafMark /><span>GreenPulse</span></div><p>Carbon intelligence for sustainable people and communities.</p></div><div className="contact-links"><button onClick={() => scrollTo("about")}>About</button><button onClick={() => scrollTo("features")}>Features</button><button onClick={() => scrollTo("community")}>Community</button><button onClick={onLogin}>Login</button></div><div className="contact-free">Free for everyone<br /><span>Built for measurable climate action.</span></div></section>
      </main>
      <footer className="landing-footer"><span>© {new Date().getFullYear()} GreenPulse</span><span>Measure · Understand · Improve</span></footer>
    </div>
  );
}
