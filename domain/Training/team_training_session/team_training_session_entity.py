from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class TeamTrainingSessionEntity(Base):
    __tablename__ = "team_trainings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    place = Column(String(255), nullable=False)
    date = Column(DATETIME, nullable=False)

    training_sessions = relationship("TrainingSessionEntity", back_populates="team_training")



