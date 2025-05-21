from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class ZoneEntity(Base):
    __tablename__ = "training_zones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    lower_bound = Column(Float,nullable=False)
    upper_bound = Column(Float,nullable=False)
    weight_factor = Column(Float,nullable=True)
    time_spent = Column(Float,nullable=True)
    time_percentage = Column(Float,nullable=True)

    metrics_id = Column(Integer, ForeignKey("training_metrics.id"), nullable=True)
    training_metrics = relationship("TrainingMetricsEntity", back_populates="zones")

