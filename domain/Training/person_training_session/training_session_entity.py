from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class TrainingSessionEntity(Base):
    __tablename__ = 'training_session'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    duration = Column(Integer, nullable=True)

    # One-to-one relationship with TrainingMetricsEntity
    metrics_id = Column(Integer, ForeignKey('training_metrics.id'), unique=True, nullable=True)
    metrics = relationship("TrainingMetricsEntity", back_populates="session")

    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)  # 🔥 ForeignKey -> Many-to-One kapcsolat
    person = relationship("PersonEntity", back_populates="training_sessions")  # 🔥 Kapcsolat vissza a személyhez

    team_training_id = Column(Integer, ForeignKey("team_trainings.id"), nullable=True)  # Foreign key to team_trainings
    team_training = relationship("TeamTrainingSessionEntity", back_populates="training_sessions")

