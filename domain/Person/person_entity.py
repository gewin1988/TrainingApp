from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from domain.Person.person_config import *
from configuration.symbols import SYMBOL_ERROR
from infrastructure.database.db_management.db_manager import Base
from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity

class PersonEntity(Base):
    __tablename__ = 'persons'
    __table_args__ = (
        UniqueConstraint("name", "age", name="uq_name_age"),  # Composite unique constraint
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    fitness_level = Column(String(100), default="not_trained")
    resting_hr = Column(Integer, default=60)
    max_hr_calculation_algorythm = Column(String(100), default="simple")
    hr_max = Column(Integer)
    vo2_max = Column(Float)
    heart_rate_reserve = Column(Integer)
    bmi = Column(Float)

    training_sessions = relationship("TrainingSessionEntity", back_populates="person", cascade="all, delete-orphan")


