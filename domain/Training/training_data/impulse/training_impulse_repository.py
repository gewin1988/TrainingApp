from sqlalchemy.orm import Session

from domain.Training.training_data.impulse.training_impulse_entity import TrainingImpulseEntity
from domain.base.base_repository import BaseRepository


class TrainingImpulseRepository(BaseRepository[TrainingImpulseEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TrainingImpulseEntity)