from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.review import ReviewSchedule

# Spaced repetition intervals (days) by mastery_level after success
INTERVALS = [1, 3, 7, 14, 30]


def schedule_after_failure(db: Session, problem_id: int) -> ReviewSchedule:
    """First failure → review tomorrow."""
    schedule = db.query(ReviewSchedule).filter(ReviewSchedule.problem_id == problem_id).first()
    tomorrow = datetime.utcnow() + timedelta(days=1)
    if schedule is None:
        schedule = ReviewSchedule(
            problem_id=problem_id,
            next_review=tomorrow,
            review_count=0,
            mastery_level=0,
            status="Learning",
        )
        db.add(schedule)
    else:
        schedule.next_review = tomorrow
        schedule.status = "Learning"
        schedule.mastery_level = max(0, schedule.mastery_level - 1)
    db.flush()
    return schedule


def schedule_after_success(db: Session, problem_id: int) -> ReviewSchedule:
    """Advance spaced-repetition interval on success."""
    schedule = db.query(ReviewSchedule).filter(ReviewSchedule.problem_id == problem_id).first()
    if schedule is None:
        level = 0
        next_days = INTERVALS[0]
        schedule = ReviewSchedule(
            problem_id=problem_id,
            next_review=datetime.utcnow() + timedelta(days=next_days),
            review_count=1,
            mastery_level=level,
            status="Reviewing",
        )
        db.add(schedule)
    else:
        schedule.review_count += 1
        schedule.mastery_level = min(len(INTERVALS) - 1, schedule.mastery_level + 1)
        days = INTERVALS[schedule.mastery_level]
        schedule.next_review = datetime.utcnow() + timedelta(days=days)
        schedule.status = "Mastered" if schedule.mastery_level >= len(INTERVALS) - 1 else "Reviewing"
    db.flush()
    return schedule
