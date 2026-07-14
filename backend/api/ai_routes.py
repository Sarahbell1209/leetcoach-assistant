from fastapi import APIRouter

from ai.coach import get_hint, review_code
from schemas import CodeReviewRequest, CodeReviewResponse, HintRequest, HintResponse

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/hint", response_model=HintResponse)
def hint(payload: HintRequest):
    text = get_hint(
        problem_title=payload.problem_title,
        problem_description=payload.problem_description,
        language=payload.language,
        code=payload.code,
        hint_level=payload.hint_level,
    )
    return HintResponse(hint_level=payload.hint_level, hint=text)


@router.post("/review", response_model=CodeReviewResponse)
def code_review(payload: CodeReviewRequest):
    text = review_code(
        problem_title=payload.problem_title,
        language=payload.language,
        code=payload.code,
        status=payload.status,
    )
    return CodeReviewResponse(review=text)
