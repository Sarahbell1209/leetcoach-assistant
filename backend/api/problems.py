from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.problem import Problem
from schemas import ProblemOut, SubmissionCreate, SubmissionOut
from services.submissions import record_submission, upsert_problem

router = APIRouter(prefix="/api", tags=["core"])


def _problem_out(p: Problem) -> ProblemOut:
    return ProblemOut(
        id=p.id,
        leetcode_id=p.leetcode_id,
        title=p.title,
        slug=p.slug,
        difficulty=p.difficulty,
        url=p.url,
        is_solved=p.is_solved,
        first_solved_at=p.first_solved_at,
        last_attempt=p.last_attempt,
        total_attempts=p.total_attempts,
        favorite=p.favorite,
        notes=p.notes or "",
        tags=[t.name for t in p.tags],
    )


@router.post("/submissions", response_model=SubmissionOut)
def create_submission(payload: SubmissionCreate, db: Session = Depends(get_db)):
    return record_submission(db, payload)


@router.get("/submissions", response_model=list[SubmissionOut])
def list_submissions(limit: int = 50, db: Session = Depends(get_db)):
    from models.submission import Submission

    return (
        db.query(Submission)
        .order_by(Submission.submitted_at.desc())
        .limit(min(limit, 200))
        .all()
    )


@router.get("/problems", response_model=list[ProblemOut])
def list_problems(db: Session = Depends(get_db)):
    problems = db.query(Problem).order_by(Problem.updated_at.desc()).all()
    return [_problem_out(p) for p in problems]


@router.get("/problems/{problem_id}", response_model=ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(404, "Problem not found")
    return _problem_out(p)


@router.patch("/problems/{problem_id}/favorite")
def toggle_favorite(problem_id: int, db: Session = Depends(get_db)):
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(404, "Problem not found")
    p.favorite = not p.favorite
    db.commit()
    return {"favorite": p.favorite}


@router.patch("/problems/{problem_id}/notes")
def update_notes(problem_id: int, notes: str, db: Session = Depends(get_db)):
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(404, "Problem not found")
    p.notes = notes
    db.commit()
    return {"ok": True}
