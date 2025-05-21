from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class HrDataEntity(Base):
    __tablename__ = 'hr_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    value = Column(Integer, nullable=False)

    training_metrics_id = Column(Integer, ForeignKey('training_metrics.id'), nullable=False)
    training_metrics = relationship("TrainingMetricsEntity", back_populates="hr_data")

