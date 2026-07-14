(function () {
  const difficultyMap = {
    easy: "Easy",
    medium: "Medium",
    hard: "Hard",
  };

  function parseSlug() {
    const m = location.pathname.match(/\/problems\/([^/]+)/);
    return m ? m[1] : null;
  }

  function getTitle() {
    const el =
      document.querySelector('[data-cy="question-title"]') ||
      document.querySelector("div[class*='text-title']") ||
      document.querySelector("h1");
    return el ? el.textContent.trim() : document.title.replace(" - LeetCode", "").trim();
  }

  function getDifficulty() {
    const text = document.body.innerText;
    if (/\bHard\b/.test(text)) return "Hard";
    if (/\bMedium\b/.test(text)) return "Medium";
    if (/\bEasy\b/.test(text)) return "Easy";
    return "Medium";
  }

  function getLeetCodeId() {
    const title = getTitle();
    const m = title.match(/^(\d+)\./);
    return m ? Number(m[1]) : Number(Date.now() % 100000);
  }

  function getEditorCode() {
    // Monaco / CodeMirror fallbacks used by LeetCode
    const lines = document.querySelectorAll(".view-line");
    if (lines.length) {
      return Array.from(lines)
        .map((l) => l.textContent)
        .join("\n");
    }
    const ta = document.querySelector("textarea");
    return ta ? ta.value : "";
  }

  function getLanguage() {
    const btn =
      document.querySelector('[id*="lang"]') ||
      document.querySelector("button[class*='lang']") ||
      document.querySelector('[data-cy="lang-select"]');
    if (btn && btn.textContent) return btn.textContent.trim();
    return "python3";
  }

  function detectResultStatus() {
    const body = document.body.innerText;
    if (/Accepted/i.test(body) && /Runtime/i.test(body)) return "Accepted";
    if (/Wrong Answer/i.test(body)) return "Wrong Answer";
    if (/Time Limit Exceeded/i.test(body)) return "Time Limit Exceeded";
    if (/Runtime Error/i.test(body)) return "Runtime Error";
    if (/Compile Error/i.test(body)) return "Compile Error";
    if (/Memory Limit Exceeded/i.test(body)) return "Memory Limit Exceeded";
    return null;
  }

  function extractRuntimeMemory() {
    const text = document.body.innerText;
    const runtime = (text.match(/Runtime[:\s]+([\d.]+\s*ms)/i) || [])[1] || null;
    const memory = (text.match(/Memory[:\s]+([\d.]+\s*MB)/i) || [])[1] || null;
    return { runtime, memory };
  }

  let lastRecordedKey = null;

  function tryRecord() {
    const status = detectResultStatus();
    if (!status) return;

    const slug = parseSlug();
    if (!slug) return;

    const { runtime, memory } = extractRuntimeMemory();
    const code = getEditorCode();
    const key = `${slug}:${status}:${code.slice(0, 80)}:${runtime}`;
    if (key === lastRecordedKey) return;
    lastRecordedKey = key;

    const payload = {
      leetcode_id: getLeetCodeId(),
      title: getTitle().replace(/^\d+\.\s*/, ""),
      slug,
      difficulty: getDifficulty(),
      url: `https://leetcode.com/problems/${slug}/`,
      language: getLanguage(),
      code: code || "// code not captured",
      status,
      runtime,
      memory,
      time_spent: null,
      used_hint_level: 0,
      tags: [],
    };

    chrome.runtime.sendMessage({ type: "RECORD_SUBMISSION", payload }, (res) => {
      if (chrome.runtime.lastError) {
        console.warn("[LeetCoach]", chrome.runtime.lastError.message);
        return;
      }
      console.log("[LeetCoach] recorded", res);
      showToast(res?.ok ? `Recorded: ${status}` : `Record failed`);
    });
  }

  function showToast(msg) {
    const el = document.createElement("div");
    el.textContent = `LeetCoach · ${msg}`;
    Object.assign(el.style, {
      position: "fixed",
      bottom: "24px",
      right: "24px",
      zIndex: 999999,
      background: "#0f172a",
      color: "#e2e8f0",
      padding: "10px 14px",
      borderRadius: "8px",
      fontSize: "13px",
      fontFamily: "ui-sans-serif, system-ui, sans-serif",
      boxShadow: "0 8px 24px rgba(0,0,0,.35)",
    });
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2800);
  }

  // Observe DOM for submission result panels
  const observer = new MutationObserver(() => tryRecord());
  observer.observe(document.body, { childList: true, subtree: true });

  // Also hook Submit button clicks for a delayed poll
  document.addEventListener(
    "click",
    (e) => {
      const t = e.target;
      if (!(t instanceof HTMLElement)) return;
      const label = (t.textContent || "").trim().toLowerCase();
      if (label === "submit" || t.closest('button[data-e2e-locator="console-submit-button"]')) {
        setTimeout(tryRecord, 2500);
        setTimeout(tryRecord, 5000);
        setTimeout(tryRecord, 8000);
      }
    },
    true
  );

  console.log("[LeetCoach] content script ready on", parseSlug());
})();
