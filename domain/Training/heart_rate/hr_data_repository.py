from sqlalchemy.orm import Session
from domain.Training.heart_rate.hr_data_entity import HrDataEntity

from domain.base.base_repository import BaseRepository


class HrDataRepository(BaseRepository[HrDataEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, HrDataEntity)


