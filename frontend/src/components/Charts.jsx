import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const COLORS = ["#3b9b68", "#65b979", "#e7a52b", "#d85b4f", "#8d6cc7", "#55a7a2", "#7396c9", "#c66d9a"];

export function EmissionChart({ breakdown }) {
  const data = Object.entries(breakdown || {})
    .filter(([key, value]) => key !== "Total" && key !== "Tree offset" && Number(value) > 0)
    .map(([name, value]) => ({ name, value: Number(value) }));

  return (
    <div className="card chart-card">
      <div className="card-heading">
        <div>
          <h3>Emission Sources</h3>
          <p>Monthly contribution by category</p>
        </div>
        <span className="chart-dot">●</span>
      </div>

      {data.length ? (
        <div className="donut-wrap">
          <ResponsiveContainer width="54%" height={285}>
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                innerRadius={67}
                outerRadius={101}
                paddingAngle={2}
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${Number(value).toFixed(1)} kg`, "Emission"]} />
            </PieChart>
          </ResponsiveContainer>

          <div className="chart-legend">
            {data.slice(0, 7).map((item, index) => {
              const total = data.reduce((sum, x) => sum + x.value, 0);
              const pct = total ? (item.value / total) * 100 : 0;
              return (
                <div className="legend-row" key={item.name}>
                  <span className="legend-name">
                    <i style={{ background: COLORS[index % COLORS.length] }} />
                    {item.name}
                  </span>
                  <strong>{item.value.toFixed(1)} kg ({pct.toFixed(1)}%)</strong>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="chart-empty">No emission data available.</div>
      )}
    </div>
  );
}

export function ForecastChart({ forecast }) {
  const data = (forecast || []).map((item) => ({
    month: `M${item.month}`,
    emissions: Number(item.estimated_emissions),
  }));

  return (
    <div className="card chart-card">
      <div className="card-heading">
        <div>
          <h3>6-Month Outlook</h3>
          <p>Estimated future monthly emissions</p>
        </div>
        <span className="forecast-badge">OUTLOOK</span>
      </div>

      <ResponsiveContainer width="100%" height={285}>
        <LineChart data={data} margin={{ top: 12, right: 14, left: -14, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 4" stroke="#e6eee8" vertical={false} />
          <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: "#7b8d84", fontSize: 11 }} />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: "#7b8d84", fontSize: 11 }} />
          <Tooltip formatter={(value) => [`${Number(value).toFixed(1)} kg`, "Forecast"]} />
          <Line
            type="monotone"
            dataKey="emissions"
            stroke="#3b9b68"
            strokeWidth={3}
            dot={{ r: 5, fill: "#3b9b68", stroke: "#ffffff", strokeWidth: 2 }}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
