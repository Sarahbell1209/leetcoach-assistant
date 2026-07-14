from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database.db import Base


class AlgorithmTemplate(Base):
    __tablename__ = "algorithm_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    when_to_use = Column(Text, default="")
    recognition_signals = Column(Text, default="")
    complexity = Column(String(128), default="")
    common_mistakes = Column(Text, default="")
    representative_problems = Column(Text, default="")  # JSON list as text
    code_python = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
