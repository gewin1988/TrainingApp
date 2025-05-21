from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db_management.database import Base


class TrainingImpulseEntity(Base):
    __tablename__ = "training_impulses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simplified_banister_trimp = Column(Float, nullable=False, default=0.0)
    advanced_banister_trimp = Column(Float, nullable=False, default=0.0)
    edwards_trimp = Column(Float, nullable=False, default=0.0)
    recovery_factor = Column(Float, nullable=False, default=1.1)

    metrics_id = Column(Integer, ForeignKey('training_metrics.id'), unique=True, nullable=True)
    training_metrics = relationship("TrainingMetricsEntity", back_populates="training_impulse")

