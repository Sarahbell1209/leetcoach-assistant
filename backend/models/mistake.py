from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database.db import Base

MISTAKE_CATEGORIES = [
    "Algorithm misunderstanding",
    "Didn't understand problem",
    "Boundary condition",
    "Wrong data structure",
    "Wrong implementation",
    "Complexity too high",
    "Syntax error",
    "Off-by-one",
    "Overflow",
    "Other",
]


class Mistake(Base):
    __tablename__ = "mistakes"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=True)
    category = Column(String(64), nullable=False, default="Other")
    reflection = Column(Text, default="")  # max 500 words, enforced in API
    created_at = Column(DateTime, default=datetime.utcnow)

    problem = relationship("Problem", back_populates="mistakes")
    submission = relationship("Submission", back_populates="mistake")
