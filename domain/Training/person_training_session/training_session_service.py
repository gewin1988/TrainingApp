from datetime import datetime
from typing import Optional, List

from sqlalchemy import TIMESTAMP

from domain.Training.heart_rate.hr_data_entity import HrDataEntity
from domain.Training.training_data.metrics.training_metrics_entity import TrainingMetricsEntity
from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity

from domain.Training.person_training_session.training_session_repository import TrainingSessionRepository
# from domain.TrainingSessionManager.training_session_manager import TrainingSessionManager
from domain.base.base_service import BaseService
from domain.Training.training_data.metrics.training_metrics_service import TrainingMetricsService
from configuration.symbols import SYMBOL_ERROR


class TrainingSessionService(BaseService[TrainingSessionEntity]):
    def __init__(self, repository: TrainingSessionRepository, metrics_service:TrainingMetricsService):
        super().__init__(repository)
        self.metrics_service = metrics_service
        # self.training_session_manager = training_session_manager

    def create(self, name: str, location: str, person_id:int, team_training_id:int = None, start_time = None, metrics_data: dict = None) -> TrainingSessionEntity:
        """
        Create a new training session with optional metrics_data.
        """

        # Create the TrainingSessionEntity
        new_training_session = TrainingSessionEntity(
            name=name,
            location=location,
            start_time=start_time,
            team_training_id=team_training_id
        )

        if isinstance(metrics_data, TrainingMetricsEntity):
            new_metrics = metrics_data
        # Ha egy dict-et kaptunk, akkor konvertáljuk TrainingMetricsEntity példánnyá
        elif isinstance(metrics_data, dict):
            new_metrics = TrainingMetricsEntity(**metrics_data)
        # Ha semmi nincs megadva, akkor új példányt hozunk létre
        else:
            new_metrics = self.metrics_service.create()


        new_training_session.metrics = new_metrics
        new_training_session.person_id = person_id
        # add the session to training session manager cache
        # self.training_session_manager.set_active_session(person_id=person_id,session_id=new_training_session.id)

        # Save the training session to the database
        return self.repository.create(new_training_session)

    def get_start_time_by_id(self, session_id)->Optional[datetime]:
        session = self.repository.get_by_id(session_id)
        if session:
            return session.start_time
        else:
            return None

    def start_training_session(self, session_id):
        self.update_start_time(session_id, datetime.now())


    def update_start_time(self, session_id: int, new_value:datetime) -> TrainingSessionEntity:
        return self.update_entity_field(entity_id=session_id, field_name="start_time", new_value=new_value)

    def update_end_time(self, session_id: int, new_value: TIMESTAMP):
        self.update_entity_field(entity_id=session_id, field_name="end_time", new_value=new_value)

    def update_duration(self, session_id: int, new_value: TIMESTAMP):
        self.update_entity_field(entity_id=session_id, field_name="duration", new_value=new_value)

    def update_metrics(self, session_id: int, new_value: TrainingMetricsEntity):
        self.update_entity_field(entity_id=session_id, field_name="metrics_data", new_value=new_value)

    def update_person_id(self, session_id: int, new_value: int):
        self.update_entity_field(entity_id=session_id, field_name="person_id", new_value=new_value)

    def update_team_training_id(self, session_id: int, new_value: int):
        self.update_entity_field(entity_id=session_id, field_name="team_training_id", new_value=new_value)

    def add_hr_data_to_session(self, session_id: int, hr_data_list: list):
        """HR adatok hozzáadása egy training session-höz"""
        training_session = self.repository.get_by_id(session_id)

        if not training_session:
            raise ValueError(f"{SYMBOL_ERROR} Nincs ilyen edzés: {session_id}")

        if not training_session.metrics:
            raise ValueError(f"{SYMBOL_ERROR} A session ({session_id}) nem rendelkezik metrics_data entitással.")

        # HR adatok hozzáadása a training metrics_data-hez
        self.metrics_service.add_hr_data(training_session.metrics.id, hr_data_list)

    def get_session_with_metrics(self, session_id: int) -> Optional[TrainingSessionEntity]:
        """
        Fetch a training session with its associated metrics_data.

        :param session_id: ID of the training session.
        :return: The TrainingSessionEntity with metrics_data, or None if not found.
        """
        return self.repository.get_by_id(session_id)

    def get_hr_data(self, session_id:int)->List[HrDataEntity]:
        training_session = self.repository.get_by_id(session_id)
        if training_session and training_session.metrics:
            return training_session.metrics.hr_data  # Visszaadja az összes kapcsolódó HR adatot
        return []  # Ha nincs session vagy nincs hozzá metrika, üres listát ad vissza

    def set_current_session(self, session_id, person_id):
        self.training_session_manager.set_active_session(session_id=session_id, person_id=person_id)

    def get_all_connected_to_team_training_id(self, team_training_id):
        trainings = self.repository.get_all()
        return [training.id for training in trainings if training.team_training_id == team_training_id]
