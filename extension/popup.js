const apiInput = document.getElementById("api");
const status = document.getElementById("status");

chrome.storage.sync.get({ apiBase: "http://localhost:8000" }, ({ apiBase }) => {
  apiInput.value = apiBase;
});

document.getElementById("save").addEventListener("click", () => {
  const apiBase = apiInput.value.trim().replace(/\/$/, "");
  chrome.storage.sync.set({ apiBase }, async () => {
    try {
      const res = await fetch(`${apiBase}/api/health`);
      const data = await res.json();
      status.textContent = res.ok ? `Connected · ${data.service}` : "Unreachable";
    } catch {
      status.textContent = "Cannot reach backend. Is uvicorn running?";
    }
  });
});
