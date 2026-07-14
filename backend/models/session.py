from datetime import datetime

from sqlalchemy import Column, DateTime, Integer

from database.db import Base


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, default=0)  # seconds
    problems_attempted = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
