from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.mistake import MISTAKE_CATEGORIES, Mistake
from models.review import ReviewSchedule
from schemas import MistakeCreate, MistakeOut, ReviewOut

router = APIRouter(prefix="/api", tags=["learning"])


@router.get("/mistakes", response_model=list[MistakeOut])
def list_mistakes(db: Session = Depends(get_db)):
    return db.query(Mistake).order_by(Mistake.created_at.desc()).all()


@router.get("/mistakes/categories")
def categories():
    return MISTAKE_CATEGORIES


@router.post("/mistakes", response_model=MistakeOut)
def create_mistake(payload: MistakeCreate, db: Session = Depends(get_db)):
    words = len(payload.reflection.split()) if payload.reflection else 0
    if words > 500:
        raise HTTPException(400, "Reflection must be ≤ 500 words")
    m = Mistake(
        problem_id=payload.problem_id,
        submission_id=payload.submission_id,
        category=payload.category,
        reflection=payload.reflection,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.patch("/mistakes/{mistake_id}", response_model=MistakeOut)
def update_mistake(mistake_id: int, payload: MistakeCreate, db: Session = Depends(get_db)):
    m = db.query(Mistake).filter(Mistake.id == mistake_id).first()
    if not m:
        raise HTTPException(404, "Mistake not found")
    words = len(payload.reflection.split()) if payload.reflection else 0
    if words > 500:
        raise HTTPException(400, "Reflection must be ≤ 500 words")
    m.category = payload.category
    m.reflection = payload.reflection
    db.commit()
    db.refresh(m)
    return m


@router.get("/reviews/due", response_model=list[ReviewOut])
def reviews_due(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    rows = (
        db.query(ReviewSchedule)
        .filter(ReviewSchedule.next_review <= now)
        .order_by(ReviewSchedule.next_review.asc())
        .all()
    )
    out = []
    for r in rows:
        out.append(
            ReviewOut(
                id=r.id,
                problem_id=r.problem_id,
                next_review=r.next_review,
                review_count=r.review_count,
                mastery_level=r.mastery_level,
                status=r.status,
                problem_title=r.problem.title if r.problem else None,
                problem_url=r.problem.url if r.problem else None,
            )
        )
    return out


@router.get("/reviews", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    rows = db.query(ReviewSchedule).order_by(ReviewSchedule.next_review.asc()).all()
    return [
        ReviewOut(
            id=r.id,
            problem_id=r.problem_id,
            next_review=r.next_review,
            review_count=r.review_count,
            mastery_level=r.mastery_level,
            status=r.status,
            problem_title=r.problem.title if r.problem else None,
            problem_url=r.problem.url if r.problem else None,
        )
        for r in rows
    ]
