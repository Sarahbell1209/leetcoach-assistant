from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), unique=True, nullable=False)
    next_review = Column(DateTime, nullable=False)
    review_count = Column(Integer, default=0)
    mastery_level = Column(Integer, default=0)  # 0..4 maps to intervals
    status = Column(String(32), default="New")  # New / Learning / Reviewing / Mastered
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    problem = relationship("Problem", back_populates="review_schedule")
