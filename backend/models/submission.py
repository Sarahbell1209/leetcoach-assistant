from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database.db import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    language = Column(String(64), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(64), nullable=False)  # Accepted / Wrong Answer / etc.
    runtime = Column(String(64), nullable=True)
    memory = Column(String(64), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    attempt_number = Column(Integer, default=1)
    time_spent = Column(Integer, nullable=True)  # seconds
    used_hint_level = Column(Integer, default=0)

    problem = relationship("Problem", back_populates="submissions")
    mistake = relationship("Mistake", back_populates="submission", uselist=False)
