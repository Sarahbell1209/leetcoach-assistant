from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{DATA_DIR / 'leetcoach.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models import (  # noqa: F401
        problem,
        submission,
        mistake,
        review,
        template,
        session as study_session,
        plan,
    )

    Base.metadata.create_all(bind=engine)
