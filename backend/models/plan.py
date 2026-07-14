from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from database.db import Base


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_date = Column(Date, default=date.today, unique=True, index=True)
    mode = Column(String(64), default="Interview Sprint")
    content = Column(Text, default="")  # JSON payload
    target_minutes = Column(Integer, default=90)
    created_at = Column(DateTime, default=datetime.utcnow)
