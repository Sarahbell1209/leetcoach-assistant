# LeetCoach AI — Product Requirements

Version: 1.0 · Phase 1 personal use

## Goal
AI-powered LeetCode learning assistant that works *alongside* LeetCode.
Record submissions, analyze mistakes, schedule reviews, progressive hints — never spoil first.

**Philosophy:** Learning > Statistics > AI

## Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI + SQLAlchemy + SQLite
- Extension: Chrome Manifest V3
- AI: OpenAI API (optional; offline hint fallback)

## Phase 1 modules
1. Automatic submission recorder (extension)
2. Problem library
3. Learning dashboard
4. Mistake book
5. Spaced review scheduler (1→3→7→14→30 days)
6. Progressive AI hints (levels 1–6)
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
