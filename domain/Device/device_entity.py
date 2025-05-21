from sqlalchemy import Column, String, Integer

from infrastructure.database.db_management.database import Base


class BLEHrDeviceEntity(Base):
    __tablename__ = "devices"

    # id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_address = Column(String(50), primary_key=True, nullable=False) # as id
    brand = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)

    # person = relationship("PersonEntity", back_populates="device")




