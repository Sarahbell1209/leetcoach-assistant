import json
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.plan import DailyPlan
from models.template import AlgorithmTemplate
from schemas import DailyPlanOut, TemplateOut

router = APIRouter(prefix="/api", tags=["plan-templates"])

DEFAULT_TEMPLATES = [
    {
        "name": "Two Pointers",
        "when_to_use": "Sorted arrays, pairs with target sum, palindrome checks, in-place partition.",
        "recognition_signals": "sorted input · find pair/triplet · remove duplicates in-place · opposite ends",
        "complexity": "O(n) time, O(1) space typical",
        "common_mistakes": "Off-by-one when moving pointers; forgetting early termination; unsorted input.",
        "representative_problems": '["Two Sum II", "3Sum", "Container With Most Water", "Trapping Rain Water"]',
        "code_python": "def two_sum(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        s = nums[lo] + nums[hi]\n        if s == target:\n            return [lo, hi]\n        if s < target:\n            lo += 1\n        else:\n            hi -= 1\n    return []\n",
    },
    {
        "name": "Sliding Window",
        "when_to_use": "Contiguous subarray/substring with constraint (max/min/length/sum).",
        "recognition_signals": "longest/shortest subarray · at most K distinct · fixed window size",
        "complexity": "O(n) time with hash map, O(k) space",
        "common_mistakes": "Not shrinking window correctly; counting frequency updates twice.",
        "representative_problems": '["Longest Substring Without Repeating", "Minimum Window Substring", "Max Consecutive Ones III"]',
        "code_python": "from collections import defaultdict\n\ndef longest_unique(s):\n    seen = defaultdict(int)\n    left = best = 0\n    for right, ch in enumerate(s):\n        seen[ch] += 1\n        while seen[ch] > 1:\n            seen[s[left]] -= 1\n            left += 1\n        best = max(best, right - left + 1)\n    return best\n",
    },
    {
        "name": "Binary Search",
        "when_to_use": "Sorted search space, or monotonic answer space (search on answer).",
        "recognition_signals": "sorted · find boundary · minimize/maximize under constraint",
        "complexity": "O(log n) time",
        "common_mistakes": "Infinite loops (lo/hi updates); mid overflow in other languages; wrong invariant.",
        "representative_problems": '["Binary Search", "Search Insert Position", "Koko Eating Bananas", "Median of Two Sorted Arrays"]',
        "code_python": "def lower_bound(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo\n",
    },
    {
        "name": "BFS",
        "when_to_use": "Shortest path in unweighted graph, level-order traversal.",
        "recognition_signals": "shortest · minimum steps · levels · grid flooded fill",
        "complexity": "O(V+E)",
        "common_mistakes": "Not marking visited when enqueueing; mixing DFS recursion depth.",
        "representative_problems": '["Binary Tree Level Order", "Word Ladder", "Rotting Oranges", "Shortest Path in Binary Matrix"]',
        "code_python": "from collections import deque\n\ndef bfs(start, graph):\n    q = deque([start])\n    seen = {start}\n    while q:\n        node = q.popleft()\n        for nei in graph[node]:\n            if nei not in seen:\n                seen.add(nei)\n                q.append(nei)\n    return seen\n",
    },
    {
        "name": "DFS / Backtracking",
        "when_to_use": "Explore all paths, permutations, combinations, tree/graph search.",
        "recognition_signals": "all solutions · paths · subsets · prune early",
        "complexity": "Often exponential; prune aggressively",
        "common_mistakes": "Forgetting undo after recurse; mutating shared path list.",
        "representative_problems": '["Subsets", "Combination Sum", "Permutations", "N-Queens", "Word Search"]',
        "code_python": "def subsets(nums):\n    res, path = [], []\n    def dfs(i):\n        if i == len(nums):\n            res.append(path[:])\n            return\n        path.append(nums[i])\n        dfs(i + 1)\n        path.pop()\n        dfs(i + 1)\n    dfs(0)\n    return res\n",
    },
    {
        "name": "Dynamic Programming",
        "when_to_use": "Optimal substructure + overlapping subproblems.",
        "recognition_signals": "max/min · count ways · can/cannot · subsequence",
        "complexity": "Depends on state; often O(n) or O(n*m)",
        "common_mistakes": "Wrong state definition; wrong transition; off-by-one on indices.",
        "representative_problems": '["Climbing Stairs", "House Robber", "Coin Change", "LIS", "Edit Distance"]',
        "code_python": "def coin_change(coins, amount):\n    dp = [0] + [float('inf')] * amount\n    for x in range(1, amount + 1):\n        for c in coins:\n            if x >= c:\n                dp[x] = min(dp[x], dp[x - c] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1\n",
    },
]


@router.get("/templates", response_model=list[TemplateOut])
def list_templates(db: Session = Depends(get_db)):
    return db.query(AlgorithmTemplate).order_by(AlgorithmTemplate.name.asc()).all()


@router.post("/templates/seed")
def seed_templates(db: Session = Depends(get_db)):
    created = 0
    for item in DEFAULT_TEMPLATES:
        exists = db.query(AlgorithmTemplate).filter(AlgorithmTemplate.name == item["name"]).first()
        if exists:
            continue
        db.add(AlgorithmTemplate(**item))
        created += 1
    db.commit()
    return {"created": created}


@router.get("/plans/today", response_model=DailyPlanOut)
def today_plan(mode: str = "Interview Sprint", db: Session = Depends(get_db)):
    today = date.today()
    plan = db.query(DailyPlan).filter(DailyPlan.plan_date == today).first()
    if plan is None:
        content = {
            "mode": mode,
            "items": [
                {"type": "warmup", "label": "1 Easy warm-up", "count": 1},
                {"type": "new", "label": "2 New problems", "count": 2},
                {"type": "review", "label": "2 Review problems", "count": 2},
            ],
            "target_minutes": 90,
            "notes": "Hints only when stuck > 15 min. Log reflections after each fail.",
        }
        plan = DailyPlan(
            plan_date=today,
            mode=mode,
            content=json.dumps(content),
            target_minutes=90,
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
    return plan
