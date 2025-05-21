from domain.Person.person_entity import PersonEntity
from domain.Person.person_service import PersonService
from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity
from domain.Training.person_training_session.training_session_service import TrainingSessionService
from domain.Training.team_training_session.team_training_session_entity import TeamTrainingSessionEntity
from domain.Training.team_training_session.team_training_session_repository import TeamTrainingSessionRepository
from domain.base.base_service import BaseService
from configuration.symbols import SYMBOL_ERROR


class TeamTrainingSessionService(BaseService[TeamTrainingSessionEntity]):
    def __init__(self, repository: TeamTrainingSessionRepository, training_session_service:TrainingSessionService, person_service:PersonService):
        super().__init__(repository)
        self.training_session_service=training_session_service
        self.person_service = person_service

    def create(self, place, date, name) -> TeamTrainingSessionEntity:
        new_team_training = TeamTrainingSessionEntity(place=place, date=date, name=name)
        return self.repository.create(new_team_training)

    def init_team_training(self, team_training_id: int, person_ids: list[int]) -> TeamTrainingSessionEntity:

        team_training = self.repository.get_by_id(team_training_id)

        if not team_training:
            raise ValueError(f"{SYMBOL_ERROR} Team training not found")

        persons = {p.id: p for p in self.person_service.get_by_ids(PersonEntity, person_ids)}

        training_sessions = [
            self.training_session_service.create(
                name=f"{team_training.name} - {persons[pid].name}",
                location=team_training.place,
                person_id=pid,
                team_training_id=team_training.id
            )
            for pid in person_ids
        ]

        for training_session in training_sessions:
            self.training_session_service.set_current_session(training_session.id, training_session.person_id)

        self.repository.update(team_training)

        return team_training

    def start_team_training(self, team_training_id):

        if not team_training_id:
            raise ValueError(f"{SYMBOL_ERROR} Team training id is None")

        training_sessions = self.training_session_service.get_all_connected_to_team_training_id(team_training_id)
        if len(training_sessions) == 0 or training_sessions is None:
            raise ValueError(f"{SYMBOL_ERROR} No sessoin connected to team training {team_training_id}")
        for training_id in training_sessions:
            self.training_session_service.start_training_session(session_id=training_id)


