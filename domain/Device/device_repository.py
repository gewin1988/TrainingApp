from sqlalchemy.orm import Session

from domain.Device.device_entity import BLEHrDeviceEntity
from domain.base.base_repository import BaseRepository


class DeviceRepository(BaseRepository[BLEHrDeviceEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, BLEHrDeviceEntity)