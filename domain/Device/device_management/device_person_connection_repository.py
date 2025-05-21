from sqlalchemy.orm import Session

from domain.Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity
from domain.base.base_repository import BaseRepository


class DevicePersonConnectionRepository(BaseRepository[DevicePersonConnectionEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, DevicePersonConnectionEntity)


