from sqlalchemy.orm import Session

from domain.Training.team_training_session.team_training_session_entity import TeamTrainingSessionEntity
from domain.base.base_repository import BaseRepository


class TeamTrainingSessionRepository(BaseRepository[TeamTrainingSessionEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TeamTrainingSessionEntity)
