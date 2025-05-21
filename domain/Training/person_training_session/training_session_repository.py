from sqlalchemy.orm import Session

from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity
from domain.base.base_repository import BaseRepository


class TrainingSessionRepository(BaseRepository[TrainingSessionEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TrainingSessionEntity)