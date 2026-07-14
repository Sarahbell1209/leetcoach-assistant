import os
from functools import lru_cache

from openai import OpenAI

HINT_PROMPTS = {
    1: "Explain the problem differently in plain language. Do NOT mention algorithms or solutions.",
    2: "Provide intuition only — how a human might think about approaching it. No code, no algorithm names.",
    3: "Suggest 2-3 possible data structures that might help. Do not explain the full algorithm.",
    4: "Suggest the algorithm family (e.g. two pointers, DFS) and why it fits. No code.",
    5: "Provide short pseudo-code only. No complete implementation in a real language.",
    6: "Provide a clean reference implementation. Explain WHY each key step exists.",
}

SYSTEM_PROMPT = """You are an interview coach for LeetCode practice.
Do NOT immediately reveal the answer unless the user is at hint level 6.
Always encourage independent thinking.
Only provide ONE level of hint at a time.
When reviewing code: point out issues first; do not rewrite unless explicitly asked.
Always explain WHY.
Keep responses concise and actionable."""


@lru_cache
def _client() -> OpenAI | None:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key.startswith("sk-your"):
        return None
    return OpenAI(api_key=key)


def get_hint(
    *,
    problem_title: str,
    problem_description: str,
    language: str,
    code: str,
    hint_level: int,
) -> str:
    level = max(1, min(6, hint_level))
    instruction = HINT_PROMPTS[level]
    user_msg = f"""Problem: {problem_title}

Description:
{problem_description or '(not provided)'}

User language: {language}
User code so far:
```
{code or '(empty)'}
```

Hint level requested: {level}
Instruction: {instruction}
"""
    client = _client()
    if client is None:
        return _offline_hint(level, problem_title)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
    )
    return resp.choices[0].message.content or ""


def review_code(*, problem_title: str, language: str, code: str, status: str) -> str:
    client = _client()
    prompt = f"""Review this submission for "{problem_title}" ({status}).

Language: {language}
Code:
```
{code}
```

Analyze:
1. Time complexity
2. Space complexity
3. Edge cases
4. Readability & naming
5. Optimization opportunities
6. Potential bugs

Do NOT rewrite the entire solution. Point out issues and suggest focused improvements."""

    if client is None:
        return (
            "OpenAI API key not configured. Manual checklist:\n"
            "- State time/space complexity\n"
            "- List edge cases you considered\n"
            "- Check off-by-one and empty inputs\n"
            "- Look for unused variables / unclear names"
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""


def _offline_hint(level: int, title: str) -> str:
    tips = {
        1: f"Rephrase \"{title}\" in your own words. What is the input? What is the exact output? Any constraints that matter?",
        2: f"For \"{title}\", ask: can I solve a smaller version first? What changes as input grows?",
        3: "Candidates often help: hash map, array (two pointers), stack, heap, set, tree/graph adjacency.",
        4: "Match pattern: sorted → binary search / two pointers; pairs/lookup → hash map; paths → BFS/DFS; optima → DP/greedy.",
        5: "Write steps as: init → loop invariant → update → return. Keep each line one idea.",
        6: "Configure OPENAI_API_KEY in backend/.env to unlock full reference implementations.",
    }
    return tips.get(level, tips[1])
