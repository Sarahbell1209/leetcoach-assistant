"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function HintPanel() {
  const [title, setTitle] = useState("Two Sum");
  const [level, setLevel] = useState(1);
  const [code, setCode] = useState("");
  const [hint, setHint] = useState("");
  const [loading, setLoading] = useState(false);

  async function requestHint(nextLevel = level) {
    setLoading(true);
    try {
      const res = await api.hint({
        problem_title: title,
        hint_level: nextLevel,
        code,
        language: "python3",
      });
      setHint(res.hint);
      setLevel(nextLevel);
    } catch {
      setHint("Could not reach AI endpoint. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="controls">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Problem title"
          style={{ minWidth: 200 }}
        />
        <select value={level} onChange={(e) => setLevel(Number(e.target.value))}>
          {[1, 2, 3, 4, 5, 6].map((n) => (
            <option key={n} value={n}>
              Level {n}
            </option>
          ))}
        </select>
        <button disabled={loading} onClick={() => requestHint(level)}>
          {loading ? "Thinking…" : "Get hint"}
        </button>
        <button
          className="secondary"
          disabled={loading || level >= 6}
          onClick={() => requestHint(Math.min(6, level + 1))}
        >
          Next level
        </button>
      </div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Optional: paste your current code for better hints"
        rows={5}
        style={{ width: "100%", marginTop: 12 }}
      />
      {hint && <div className="hint-box">{hint}</div>}
    </div>
  );
}
