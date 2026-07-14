const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export type DashboardStats = {
  solved_today: number;
  failed_today: number;
  total_solved: number;
  current_streak: number;
  total_study_seconds: number;
  acceptance_rate: number;
  difficulty: Record<string, number>;
  tag_distribution: Record<string, number>;
  common_mistake: string | null;
  daily_submissions: { date: string; count: number }[];
};

export type Problem = {
  id: number;
  leetcode_id: number;
  title: string;
  slug: string;
  difficulty: string;
  url: string;
  is_solved: boolean;
  total_attempts: number;
  favorite: boolean;
  tags: string[];
};

export type Review = {
  id: number;
  problem_id: number;
  next_review: string;
  review_count: number;
  mastery_level: number;
  status: string;
  problem_title: string | null;
  problem_url: string | null;
};

export type Mistake = {
  id: number;
  problem_id: number;
  category: string;
  reflection: string;
  created_at: string;
};

export type Template = {
  id: number;
  name: string;
  when_to_use: string;
  recognition_signals: string;
  complexity: string;
  common_mistakes: string;
  code_python: string;
};

export type DailyPlan = {
  id: number;
  plan_date: string;
  mode: string;
  content: string;
  target_minutes: number;
};

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}

export const api = {
  health: () => get<{ status: string }>("/api/health"),
  dashboard: () => get<DashboardStats>("/api/stats/dashboard"),
  problems: () => get<Problem[]>("/api/problems"),
  reviewsDue: () => get<Review[]>("/api/reviews/due"),
  mistakes: () => get<Mistake[]>("/api/mistakes"),
  templates: () => get<Template[]>("/api/templates"),
  todayPlan: () => get<DailyPlan>("/api/plans/today"),
  seedTemplates: async () => {
    const res = await fetch(`${API_BASE}/api/templates/seed`, { method: "POST" });
    return res.json();
  },
  hint: async (body: {
    problem_title: string;
    hint_level: number;
    code?: string;
    language?: string;
  }) => {
    const res = await fetch(`${API_BASE}/api/ai/hint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return res.json() as Promise<{ hint_level: number; hint: string }>;
  },
};
