from datetime import datetime

from sqlalchemy.orm import Session

from models.mistake import Mistake
from models.problem import Problem, Tag
from models.submission import Submission
from scheduler.spaced_repetition import schedule_after_failure, schedule_after_success


def upsert_problem(
    db: Session,
    *,
    leetcode_id: int,
    title: str,
    slug: str,
    difficulty: str,
    url: str,
    tags: list[str] | None = None,
) -> Problem:
    problem = db.query(Problem).filter(Problem.leetcode_id == leetcode_id).first()
    if problem is None:
        problem = Problem(
            leetcode_id=leetcode_id,
            title=title,
            slug=slug,
            difficulty=difficulty,
            url=url,
        )
        db.add(problem)
        db.flush()
    else:
        problem.title = title
        problem.slug = slug
        problem.difficulty = difficulty
        problem.url = url
        problem.updated_at = datetime.utcnow()

    if tags:
        for name in tags:
            tag = db.query(Tag).filter(Tag.name == name).first()
            if tag is None:
                tag = Tag(name=name)
                db.add(tag)
                db.flush()
            if tag not in problem.tags:
                problem.tags.append(tag)
    return problem


def record_submission(db: Session, payload) -> Submission:
    problem = upsert_problem(
        db,
        leetcode_id=payload.leetcode_id,
        title=payload.title,
        slug=payload.slug,
        difficulty=payload.difficulty,
        url=payload.url,
        tags=payload.tags,
    )

    attempt = problem.total_attempts + 1
    problem.total_attempts = attempt
    problem.last_attempt = datetime.utcnow()

    accepted = payload.status.lower() in {"accepted", "ac", "success"}
    if accepted:
        if not problem.is_solved:
            problem.is_solved = True
            problem.first_solved_at = datetime.utcnow()
        schedule_after_success(db, problem.id)
    else:
        schedule_after_failure(db, problem.id)
        mistake = Mistake(
            problem_id=problem.id,
            category="Other",
            reflection="",
        )
        db.add(mistake)

    submission = Submission(
        problem_id=problem.id,
        language=payload.language,
        code=payload.code,
        status=payload.status,
        runtime=payload.runtime,
        memory=payload.memory,
        attempt_number=attempt,
        time_spent=payload.time_spent,
        used_hint_level=payload.used_hint_level,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    if not accepted:
        pending = (
            db.query(Mistake)
            .filter(Mistake.problem_id == problem.id, Mistake.submission_id.is_(None))
            .order_by(Mistake.id.desc())
            .first()
        )
        if pending:
            pending.submission_id = submission.id
            db.commit()

    return submission
