from sqlalchemy.orm import Session

from domain.Training.zone.zone_entity import ZoneEntity
from domain.base.base_repository import BaseRepository


class ZoneRepository(BaseRepository[ZoneEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, ZoneEntity)