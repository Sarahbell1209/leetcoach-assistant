# LeetCoach 助手 — Product Requirements

Version: 1.0 · Phase 1 personal use

## Goal
LeetCode 刷题学习助手，配合力扣使用。
Record submissions, analyze mistakes, schedule reviews, progressive hints — never spoil first.

**Philosophy:** 学习 > 统计 > 助手

## Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI + SQLAlchemy + SQLite
- Extension: Chrome Manifest V3
- 助手提示: OpenAI API (optional; offline hint fallback)

## Phase 1 modules
1. Automatic submission recorder (extension)
2. Problem library
3. Learning dashboard
4. Mistake book
5. Spaced review scheduler (1→3→7→14→30 days)
6. Progressive hints (levels 1–6)
7. Code review
8. Statistics
9. Daily plan
10. Algorithm templates

## Hint levels
1. Rephrase problem  
2. Intuition  
3. Data structures  
4. Algorithm family  
5. Pseudo-code  
6. Reference implementation  

## Success criteria
Open LeetCode → solve → Submit → auto-record → mistake analysis → review schedule → dashboard updates. No manual data entry.
