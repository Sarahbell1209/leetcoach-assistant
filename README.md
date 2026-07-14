# LeetCoach AI

AI-powered LeetCode learning assistant that works **alongside** LeetCode — not instead of it.

Records every submission, builds a mistake book, schedules spaced reviews, and gives **progressive hints** (never spoilers first).

> Learning > Statistics > AI

## Architecture

```
Chrome Extension  →  FastAPI Backend  →  SQLite
                         ↓
                  Next.js Dashboard
                         ↓
                    OpenAI API (optional)
```

## Quick start

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional: add OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

- Health: http://localhost:8000/api/health  
- Swagger: http://localhost:8000/docs  

Seed algorithm templates:

```bash
curl -X POST http://localhost:8000/api/templates/seed
```

### 2. Dashboard

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000

### 3. Chrome extension

1. Chrome → `chrome://extensions` → enable Developer mode  
2. **Load unpacked** → select the `extension/` folder  
3. Open any LeetCode problem, click **Submit** — results auto-sync to the backend  

## Features (Phase 1 MVP)

| Module | Status |
|--------|--------|
| Submission recorder (extension) | ✅ |
| Problem library + attempts | ✅ |
| Dashboard / streak / charts | ✅ |
| Mistake book (auto on fail) | ✅ |
| Spaced repetition reviews | ✅ |
| Progressive AI hints (L1–L6) | ✅ |
| Code review endpoint | ✅ |
| Daily plan | ✅ |
| Algorithm templates | ✅ |

## API snapshot

- `POST /api/submissions` — record a submit  
- `GET /api/stats/dashboard` — learning stats  
- `GET /api/reviews/due` — due reviews  
- `POST /api/ai/hint` — one hint level at a time  
- `POST /api/ai/review` — post-submit code review  
- `GET /api/plans/today` — daily plan  

## Project layout

```
leetcode-ai/
├── backend/          # FastAPI + SQLAlchemy
├── frontend/         # Next.js dashboard
├── extension/        # Chrome MV3
└── docs/PRD.md
```

## Roadmap

- **Phase 2:** auth, PostgreSQL, cloud sync, mock interview  
- **Phase 3:** team workspace, company question engine, learning path  

## License

MIT — personal interview prep & portfolio use.
