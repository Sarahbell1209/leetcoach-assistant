import { api } from "@/lib/api";
import { HintPanel } from "@/components/HintPanel";

export const dynamic = "force-dynamic";

function formatDuration(seconds: number) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export default async function HomePage() {
  let stats = null;
  let problems: Awaited<ReturnType<typeof api.problems>> = [];
  let reviews: Awaited<ReturnType<typeof api.reviewsDue>> = [];
  let mistakes: Awaited<ReturnType<typeof api.mistakes>> = [];
  let templates: Awaited<ReturnType<typeof api.templates>> = [];
  let plan = null;
  let error: string | null = null;

  try {
    [stats, problems, reviews, mistakes, templates, plan] = await Promise.all([
      api.dashboard(),
      api.problems(),
      api.reviewsDue(),
      api.mistakes(),
      api.templates(),
      api.todayPlan(),
    ]);
  } catch {
    error =
      "Backend unreachable. Start it with: cd backend && uvicorn main:app --reload --port 8000";
  }

  const planItems = plan
    ? (JSON.parse(plan.content) as { items: { label: string }[]; notes?: string }).items
    : [];
  const maxBar = Math.max(1, ...(stats?.daily_submissions.map((d) => d.count) ?? [1]));

  return (
    <main>
      <p className="pill">Personal interview lab</p>
      <h1 className="brand">LeetCoach 助手</h1>
      <p className="tagline">
        Stay on LeetCode. We record attempts, schedule reviews, and give progressive hints —
        never spoilers first.
      </p>

      <nav className="nav">
        <a href="#today">Today</a>
        <a href="#reviews">Reviews</a>
        <a href="#mistakes">Mistakes</a>
        <a href="#templates">Templates</a>
        <a href="#hints">Hints</a>
        <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
          API docs
        </a>
      </nav>

      {error && <div className="error-banner">{error}</div>}

      {stats && (
        <section className="grid" aria-label="Key stats">
          <div className="stat">
            <div className="label">Solved today</div>
            <div className="value">{stats.solved_today}</div>
          </div>
          <div className="stat">
            <div className="label">Streak</div>
            <div className="value">{stats.current_streak}d</div>
          </div>
          <div className="stat">
            <div className="label">Total solved</div>
            <div className="value">{stats.total_solved}</div>
          </div>
          <div className="stat">
            <div className="label">Acceptance</div>
            <div className="value">{stats.acceptance_rate}%</div>
          </div>
        </section>
      )}

      {stats && (
        <section className="section" id="today">
          <h2>14-day activity</h2>
          <p className="sub">
            Failed today: {stats.failed_today} · Study time:{" "}
            {formatDuration(stats.total_study_seconds)}
            {stats.common_mistake ? ` · Common miss: ${stats.common_mistake}` : ""}
          </p>
          <div className="bars" title="Daily submissions">
            {stats.daily_submissions.map((d) => (
              <div
                key={d.date}
                className="bar"
                style={{ height: `${Math.max(8, (d.count / maxBar) * 100)}%` }}
                title={`${d.date}: ${d.count}`}
              />
            ))}
          </div>
        </section>
      )}

      <div className="two-col">
        <section className="section">
          <h2>Today&apos;s plan</h2>
          <p className="sub">{plan ? `${plan.mode} · ~${plan.target_minutes} min` : "—"}</p>
          <div className="list">
            {planItems.length === 0 && <div className="empty">No plan yet.</div>}
            {planItems.map((item) => (
              <div className="row" key={item.label}>
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="section" id="reviews">
          <h2>Due for review</h2>
          <p className="sub">Spaced repetition — fail → tomorrow → 3 → 7 → 14 → 30 days</p>
          <div className="list">
            {reviews.length === 0 && <div className="empty">Nothing due. Keep solving.</div>}
            {reviews.map((r) => (
              <div className="row" key={r.id}>
                <a href={r.problem_url || "#"} target="_blank" rel="noreferrer">
                  {r.problem_title || `Problem #${r.problem_id}`}
                </a>
                <span className="meta">
                  {r.status} · L{r.mastery_level}
                </span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="two-col">
        <section className="section">
          <h2>Problems</h2>
          <p className="sub">Synced from Chrome extension submissions</p>
          <div className="list">
            {problems.length === 0 && (
              <div className="empty">No problems yet. Submit on LeetCode with the extension.</div>
            )}
            {problems.slice(0, 12).map((p) => (
              <div className="row" key={p.id}>
                <div>
                  <a href={p.url} target="_blank" rel="noreferrer">
                    {p.leetcode_id}. {p.title}
                  </a>
                  <div className="meta">
                    {p.tags.slice(0, 3).join(" · ") || "untagged"} · {p.total_attempts} attempts
                  </div>
                </div>
                <span className={`meta diff-${p.difficulty}`}>
                  {p.is_solved ? "✓ " : ""}
                  {p.difficulty}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className="section" id="mistakes">
          <h2>Mistake book</h2>
          <p className="sub">Auto-created on failed submits — add your reflection later</p>
          <div className="list">
            {mistakes.length === 0 && <div className="empty">No mistakes logged yet.</div>}
            {mistakes.slice(0, 12).map((m) => (
              <div className="row" key={m.id}>
                <div>
                  <strong>{m.category}</strong>
                  <div className="meta">{m.reflection || "Add reflection via API / upcoming UI"}</div>
                </div>
                <span className="meta">#{m.problem_id}</span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="section" id="templates">
        <h2>Algorithm templates</h2>
        <p className="sub">
          Recognition signals · when to use · common pitfalls
          {templates.length === 0 && " — POST /api/templates/seed to load defaults"}
        </p>
        <div className="list">
          {templates.map((t) => (
            <details key={t.id} className="row" style={{ display: "block" }}>
              <summary style={{ cursor: "pointer" }}>
                {t.name} <span className="meta">{t.complexity}</span>
              </summary>
              <p className="sub" style={{ marginTop: 10 }}>
                {t.when_to_use}
              </p>
              <p className="meta">Signals: {t.recognition_signals}</p>
              <p className="meta">Watch out: {t.common_mistakes}</p>
              {t.code_python && <pre>{t.code_python}</pre>}
            </details>
          ))}
        </div>
      </section>

      <section className="section" id="hints">
        <h2>Progressive hints</h2>
        <p className="sub">Levels 1→6: rephrase → intuition → structures → algorithm → pseudo → code</p>
        <HintPanel />
      </section>
    </main>
  );
}
