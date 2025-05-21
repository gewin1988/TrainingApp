from sqlalchemy import Integer, Column, Float
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class TrainingMetricsEntity(Base):
    __tablename__ = 'training_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    training_stress_score = Column(Float, nullable=True)
    epoc = Column(Float, nullable=True)
    caloric_expenditure = Column(Float, nullable=True)
    resting_calories_by_training = Column(Float, nullable=True)
    zoladz_calories = Column(Float, nullable=True)
    mifflin_st_jeor_calories = Column(Float, nullable=True)
    max_hr = Column(Integer, nullable=True)
    min_hr = Column(Integer, nullable=True)
    avg_hr = Column(Integer, nullable=True)
    avg_hr_to_hr_max_ratio = Column(Integer, nullable=True)
    intensity_factor = Column(Float, nullable=True) #ez lehet kikerül majd vagy jön hozzá valami együttható a jobb számoláshoz

    # One-to-one relationship with TrainingSessionEntity
    session = relationship("TrainingSessionEntity", back_populates="metrics", uselist=False)

    # One-to-many relationship with HrDataEntity
    hr_data = relationship("HrDataEntity", back_populates="training_metrics")

    # One-to-one relationship with TrainingImpulseEntity
    training_impulse = relationship("TrainingImpulseEntity", back_populates="training_metrics", uselist=False)

    # One-to-one relationship with ZoneEntity
    zones = relationship("ZoneEntity", back_populates="training_metrics", cascade="all, delete-orphan")

