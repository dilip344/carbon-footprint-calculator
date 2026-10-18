const fields = [
  ["electricity_kwh", "Electricity / month", "kWh"],
  ["lpg_kg", "LPG / month", "kg"],
  ["water_liters", "Water / month", "L"],
  ["waste_kg", "Waste / month", "kg"],
  ["paper_kg", "Paper / month", "kg"],
  ["trees", "Trees planted", "trees"],
];

export default function CommunityCalculator({ form, setForm, onSubmit, loading }) {
  const change = (event) => {
    const { name, value } = event.target;
    setForm((old) => ({
      ...old,
      [name]: ["entity_name", "travel_mode", "food_type"].includes(name)
        ? value
        : Number(value),
    }));
  };

  return (
    <form className="card calculator" onSubmit={onSubmit}>
      <div className="section-head">
        <div>
          <span className="eyebrow">COMMUNITY CALCULATOR</span>
          <h2>Measure a shared footprint</h2>
          <p>For campuses, NGOs, schools, villages, offices and community groups.</p>
        </div>
        <span className="secure-pill community-pill">● Community mode</span>
      </div>

      <div className="form-section">
        <h3>Community profile</h3>
        <div className="form-grid two">
          <label>
            Community / campus name
            <input name="entity_name" value={form.entity_name} onChange={change} placeholder="e.g. Green Valley Campus" required />
          </label>
          <label>
            People / members
            <div className="input-unit">
              <input name="population" type="number" min="1" value={form.population} onChange={change} required />
              <span>people</span>
            </div>
          </label>
        </div>
      </div>

      <div className="form-section">
        <h3>Transportation</h3>
        <div className="form-grid two">
          <label>
            Main travel mode
            <select name="travel_mode" value={form.travel_mode} onChange={change}>
              <option value="bus">Bus</option>
              <option value="car">Car</option>
              <option value="bike">Motorbike</option>
              <option value="train">Train</option>
              <option value="walk">Walk</option>
              <option value="other">Other</option>
            </select>
          </label>
          <label>
            Total travel / month
            <div className="input-unit">
              <input name="travel_km" type="number" min="0" value={form.travel_km} onChange={change} />
              <span>km</span>
            </div>
          </label>
          <label>
            Petrol / diesel / month
            <div className="input-unit">
              <input name="fuel_liters" type="number" min="0" value={form.fuel_liters} onChange={change} />
              <span>L</span>
            </div>
          </label>
          <label>
            Flights / month
            <input name="flights" type="number" min="0" step="0.1" value={form.flights} onChange={change} />
          </label>
        </div>
        <div className="form-note">Enter aggregate community totals, not one person's values.</div>
      </div>

      <div className="form-section">
        <h3>Energy & resources</h3>
        <div className="form-grid two">
          {fields.map(([name, label, unit]) => (
            <label key={name}>
              {label}
              <div className="input-unit">
                <input name={name} type="number" min="0" step={name === "trees" ? "1" : "0.1"} value={form[name]} onChange={change} />
                <span>{unit}</span>
              </div>
            </label>
          ))}
        </div>
      </div>

      <div className="form-section">
        <h3>Shared lifestyle</h3>
        <label>
          Typical food pattern
          <select name="food_type" value={form.food_type} onChange={change}>
            <option value="vegetarian">Vegetarian</option>
            <option value="mixed">Mixed</option>
            <option value="non_vegetarian">Non-vegetarian</option>
          </select>
        </label>
      </div>

      <button className="primary-btn community-primary" disabled={loading}>
        {loading ? "Analysing community footprint..." : "Calculate community footprint"} <span>→</span>
      </button>
    </form>
  );
}
