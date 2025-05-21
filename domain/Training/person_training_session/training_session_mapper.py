from domain.Training.person_training_session.training_session_dto import TrainingSessionDTO
from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity
from domain.Training.person_training_session.training_session_model import TrainingSessionModel


class TrainingSessionMapper:
    @staticmethod
    def dto_to_entity(dto):
        return TrainingSessionEntity(
            id = dto.id,
            start_time = dto.start_time,
            end_time = dto.end_time,
            location = dto.location,
            name = dto.name,
            sduration = dto.duration,
            metrics_id = dto.metrics_id,
            person_id = dto.person_id,
            team_training_id = dto.team_training_id
        )

    @staticmethod
    def entity_to_dto(entity):
        return TrainingSessionDTO(
            id = entity.id,
            start_time = entity.start_time,
            end_time = entity.end_time,
            location = entity.location,
            name = entity.name,
            duration = entity.duration,
            metrics_id = entity.metrics_id,
            person_id = entity.person_id,
            team_training_id = entity.team_training_id
        )