from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.ai_routes import router as ai_router
from api.learning import router as learning_router
from api.plan import router as plan_router
from api.problems import router as problems_router
from api.stats import router as stats_router
from database.db import init_db

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(
    title="LeetCoach AI",
    description="AI-powered LeetCode learning assistant — learn to solve, don't copy solutions.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems_router)
app.include_router(learning_router)
app.include_router(stats_router)
app.include_router(ai_router)
app.include_router(plan_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "leetcoach-ai"}
