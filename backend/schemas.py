from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProblemCreate(BaseModel):
    leetcode_id: int
    title: str
    slug: str
    difficulty: str
    url: str
    tags: list[str] = []


class ProblemOut(BaseModel):
    id: int
    leetcode_id: int
    title: str
    slug: str
    difficulty: str
    url: str
    is_solved: bool
    first_solved_at: Optional[datetime] = None
    last_attempt: Optional[datetime] = None
    total_attempts: int
    favorite: bool
    notes: str
    tags: list[str] = []

    class Config:
        from_attributes = True


class SubmissionCreate(BaseModel):
    leetcode_id: int
    title: str
    slug: str
    difficulty: str = "Medium"
    url: str
    language: str
    code: str
    status: str
    runtime: Optional[str] = None
    memory: Optional[str] = None
    time_spent: Optional[int] = None
    used_hint_level: int = 0
    tags: list[str] = []


class SubmissionOut(BaseModel):
    id: int
    problem_id: int
    language: str
    code: str
    status: str
    runtime: Optional[str] = None
    memory: Optional[str] = None
    submitted_at: datetime
    attempt_number: int
    time_spent: Optional[int] = None
    used_hint_level: int

    class Config:
        from_attributes = True


class MistakeCreate(BaseModel):
    problem_id: int
    submission_id: Optional[int] = None
    category: str = "Other"
    reflection: str = Field(default="", max_length=3000)


class MistakeOut(BaseModel):
    id: int
    problem_id: int
    submission_id: Optional[int] = None
    category: str
    reflection: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    problem_id: int
    next_review: datetime
    review_count: int
    mastery_level: int
    status: str
    problem_title: Optional[str] = None
    problem_url: Optional[str] = None

    class Config:
        from_attributes = True


class HintRequest(BaseModel):
    problem_title: str
    problem_description: str = ""
    language: str = "python"
    code: str = ""
    hint_level: int = Field(ge=1, le=6)


class HintResponse(BaseModel):
    hint_level: int
    hint: str


class CodeReviewRequest(BaseModel):
    problem_title: str
    language: str
    code: str
    status: str = "Accepted"


class CodeReviewResponse(BaseModel):
    review: str


class DashboardStats(BaseModel):
    solved_today: int
    failed_today: int
    total_solved: int
    current_streak: int
    total_study_seconds: int
    acceptance_rate: float
    difficulty: dict[str, int]
    tag_distribution: dict[str, int]
    common_mistake: Optional[str] = None
    daily_submissions: list[dict]


class TemplateOut(BaseModel):
    id: int
    name: str
    when_to_use: str
    recognition_signals: str
    complexity: str
    common_mistakes: str
    representative_problems: str
    code_python: str

    class Config:
        from_attributes = True


class DailyPlanOut(BaseModel):
    id: int
    plan_date: date
    mode: str
    content: str
    target_minutes: int

    class Config:
        from_attributes = True
