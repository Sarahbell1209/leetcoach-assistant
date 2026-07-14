from collections import Counter
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import get_db
from models.mistake import Mistake
from models.problem import Problem
from models.session import StudySession
from models.submission import Submission
from schemas import DashboardStats

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    start_today = datetime(now.year, now.month, now.day)

    today_subs = db.query(Submission).filter(Submission.submitted_at >= start_today).all()
    solved_today = sum(1 for s in today_subs if s.status.lower() in {"accepted", "ac", "success"})
    failed_today = len(today_subs) - solved_today

    total_solved = db.query(Problem).filter(Problem.is_solved.is_(True)).count()
    total_subs = db.query(Submission).count()
    accepted_subs = (
        db.query(Submission)
        .filter(func.lower(Submission.status).in_(["accepted", "ac", "success"]))
        .count()
    )
    acceptance_rate = (accepted_subs / total_subs * 100) if total_subs else 0.0

    difficulty = {"Easy": 0, "Medium": 0, "Hard": 0}
    for p in db.query(Problem).filter(Problem.is_solved.is_(True)).all():
        difficulty[p.difficulty] = difficulty.get(p.difficulty, 0) + 1

    tag_counter: Counter[str] = Counter()
    for p in db.query(Problem).all():
        for t in p.tags:
            tag_counter[t.name] += 1

    common = (
        db.query(Mistake.category, func.count(Mistake.id))
        .group_by(Mistake.category)
        .order_by(func.count(Mistake.id).desc())
        .first()
    )

    study_seconds = db.query(func.coalesce(func.sum(StudySession.duration), 0)).scalar() or 0

    daily = []
    for i in range(13, -1, -1):
        day = start_today - timedelta(days=i)
        nxt = day + timedelta(days=1)
        count = (
            db.query(Submission)
            .filter(Submission.submitted_at >= day, Submission.submitted_at < nxt)
            .count()
        )
        daily.append({"date": day.strftime("%Y-%m-%d"), "count": count})

    return DashboardStats(
        solved_today=solved_today,
        failed_today=failed_today,
        total_solved=total_solved,
        current_streak=_streak(db),
        total_study_seconds=int(study_seconds),
        acceptance_rate=round(acceptance_rate, 1),
        difficulty=difficulty,
        tag_distribution=dict(tag_counter.most_common(12)),
        common_mistake=common[0] if common else None,
        daily_submissions=daily,
    )


def _streak(db: Session) -> int:
    solved_dates = {
        p.first_solved_at.date()
        for p in db.query(Problem).filter(Problem.first_solved_at.isnot(None)).all()
    }
    if not solved_dates:
        return 0
    streak = 0
    day = datetime.utcnow().date()
    # allow yesterday if nothing today yet
    if day not in solved_dates:
        day = day - timedelta(days=1)
    while day in solved_dates:
        streak += 1
        day -= timedelta(days=1)
    return streak
