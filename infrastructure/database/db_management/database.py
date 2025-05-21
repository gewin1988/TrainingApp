from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from infrastructure.database.db_management.db_config import DATABASE_URL

# SQLAlchemy engine létrehozása
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory létrehozása
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Alap osztály az ORM modellekhez
Base = declarative_base()
