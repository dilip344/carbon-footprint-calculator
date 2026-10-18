const API = "http://127.0.0.1:8000";

async function req(path, opt = {}) {
  const r = await fetch(API + path, {
    headers: { "Content-Type": "application/json", ...(opt.headers || {}) },
    ...opt,
  });
  if (!r.ok) {
    let m = "Request failed";
    try { m = (await r.json()).detail || m; } catch {}
    throw Error(m);
  }
  return r;
}

export async function registerUser(d) {
  return (await req("/api/auth/register", { method: "POST", body: JSON.stringify(d) })).json();
}
export async function loginUser(d) {
  return (await req("/api/auth/login", { method: "POST", body: JSON.stringify(d) })).json();
}
export async function calculateCarbon(id, d) {
  return (await req(`/api/carbon/calculate/${id}`, { method: "POST", body: JSON.stringify(d) })).json();
}
export async function calculateCommunity(id, d) {
  return (await req(`/api/community/calculate/${id}`, { method: "POST", body: JSON.stringify(d) })).json();
}
export async function getLatest(id, mode = "individual") {
  return (await req(`/api/carbon/latest/${id}?mode=${mode}`)).json();
}
export async function getHistory(id, mode = "individual") {
  return (await req(`/api/carbon/history/${id}?mode=${mode}`)).json();
}
export async function downloadReport(id) {
  const r = await fetch(`${API}/api/carbon/report/${id}`);
  if (!r.ok) throw Error("Report download failed");
  const b = await r.blob(), u = URL.createObjectURL(b), a = document.createElement("a");
  a.href = u;
  a.download = `greenpulse-report-${id}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(u);
}
