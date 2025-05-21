from sqlalchemy.orm import Session

from domain.Training.training_data.metrics.training_metrics_entity import TrainingMetricsEntity
from domain.base.base_repository import BaseRepository


class TrainingMetricsRepository(BaseRepository[TrainingMetricsEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TrainingMetricsEntity)

    def get_hr_data_for_metrics(self, metrics_id: int) -> list:
        """Fetch all HR data entities associated with a specific TrainingMetricsEntity."""
        metrics = self.db.query(TrainingMetricsEntity).filter(TrainingMetricsEntity.id == metrics_id).first()
        if metrics:
            return metrics.hr_data  # Access the hr_data relationship
        return []