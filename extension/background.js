const DEFAULT_API = "http://localhost:8000";

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({ apiBase: DEFAULT_API, hintLevel: 0 });
});

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "RECORD_SUBMISSION") {
    chrome.storage.sync.get({ apiBase: DEFAULT_API }, async ({ apiBase }) => {
      try {
        const res = await fetch(`${apiBase}/api/submissions`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(message.payload),
        });
        const data = await res.json();
        sendResponse({ ok: res.ok, data });
      } catch (err) {
        sendResponse({ ok: false, error: String(err) });
      }
    });
    return true; // async
  }
});
