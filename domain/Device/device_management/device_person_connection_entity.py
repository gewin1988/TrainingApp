from sqlalchemy import Column, String, Integer

from infrastructure.database.db_management.database import Base


class DevicePersonConnectionEntity(Base):
    __tablename__ = 'device_ownership'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_mac = Column(String(17), primary_key=True)
    owner_id = Column(Integer, nullable=True)

