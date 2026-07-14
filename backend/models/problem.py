from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from database.db import Base

problem_tags = Table(
    "problem_tags",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problems.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)

    problems = relationship("Problem", secondary=problem_tags, back_populates="tags")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    leetcode_id = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String(256), nullable=False)
    slug = Column(String(256), unique=True, nullable=False)
    difficulty = Column(String(16), nullable=False)  # Easy / Medium / Hard
    url = Column(String(512), nullable=False)
    is_solved = Column(Boolean, default=False)
    first_solved_at = Column(DateTime, nullable=True)
    last_attempt = Column(DateTime, nullable=True)
    total_attempts = Column(Integer, default=0)
    favorite = Column(Boolean, default=False)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = relationship("Tag", secondary=problem_tags, back_populates="problems")
    submissions = relationship("Submission", back_populates="problem")
    mistakes = relationship("Mistake", back_populates="problem")
    review_schedule = relationship("ReviewSchedule", back_populates="problem", uselist=False)
