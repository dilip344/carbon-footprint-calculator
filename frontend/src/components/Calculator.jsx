const fields = [
  ["electricity_kwh", "Electricity / month", "kWh"],
  ["lpg_kg", "LPG / month", "kg"],
  ["water_liters", "Water / day", "litres"],
  ["waste_kg", "Waste / month", "kg"],
  ["paper_kg", "Paper / month", "kg"],
  ["trees", "Trees planted", "trees"],
];

export default function Calculator({ form, setForm, onSubmit, loading }) {
  const change = (event) => {
    const { name, value } = event.target;
    setForm((old) => ({
      ...old,
      [name]: ["travel_mode", "food_type"].includes(name) ? value : Number(value),
    }));
  };

  return (
    <form className="card calculator" onSubmit={onSubmit}>
      <div className="section-head">
        <div>
          <span className="eyebrow">CARBON CALCULATOR</span>
          <h2>Tell us about your lifestyle</h2>
          <p>Use your normal activity levels for the most useful estimate.</p>
        </div>
        <span className="secure-pill">● AI analysis</span>
      </div>

      <div className="form-section">
        <h3>Transportation</h3>
        <div className="form-grid two">
          <label>
            Primary travel mode
            <select name="travel_mode" value={form.travel_mode} onChange={change}>
              <option value="car">Car</option>
              <option value="bike">Motorbike</option>
              <option value="bus">Bus</option>
              <option value="train">Train</option>
              <option value="walk">Walk</option>
              <option value="other">Other</option>
            </select>
          </label>

          <label>
            Travel distance / day
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

        <div className="form-note">
          For cars, fuel is used as the primary car-emission input when provided, preventing double-counting.
        </div>
      </div>

      <div className="form-section">
        <h3>Energy & Resources</h3>
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
        <h3>Lifestyle</h3>
        <label>
          Food habit
          <select name="food_type" value={form.food_type} onChange={change}>
            <option value="vegetarian">Vegetarian</option>
            <option value="mixed">Mixed</option>
            <option value="non_vegetarian">Non-vegetarian</option>
          </select>
        </label>
      </div>

      <button className="primary-btn" disabled={loading}>
        {loading ? "Analysing your footprint..." : "Calculate my carbon footprint"}
        <span>→</span>
      </button>
    </form>
  );
}
