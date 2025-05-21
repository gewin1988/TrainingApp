from domain.Training.team_training_session.team_training_session_dto import TeamTrainingSessionDTO
from domain.Training.team_training_session.team_training_session_entity import TeamTrainingSessionEntity
from domain.Training.team_training_session.team_training_session_model import TeamTrainingSessionModel



class TeamTrainingSessionMapper:
    @staticmethod
    def dto_to_entity(dto):
        return TeamTrainingSessionEntity(
            name=dto.name,
            place=dto.place,
            date=dto.date
        )

    @staticmethod
    def entity_to_dto(entity):
        return TeamTrainingSessionDTO(
            name=entity.name,
            place=entity.place,
            date=entity.date
        )