from domain.Training.training_data.impulse.training_impulse_dto import TrainingImpulseDTO
from domain.Training.training_data.impulse.training_impulse_entity import TrainingImpulseEntity
from domain.Training.training_data.impulse.training_impulse_model import TrainingImpulseModel


class TrainingImpulseMapper:
    @staticmethod
    def dto_to_entity(dto):
        return TrainingImpulseEntity(
            id=dto.id,
            simplified_banister_trimp=dto.training_metrics_modeltraining_session_model,
            advanced_banister_trimp=dto.advanced_banister_trimp,
            edwards_trimp=dto.edwards_trimp,
            recovery_factor=dto.recovery_factor,
            metrics_id = dto.metrics_id
        )

    @staticmethod
    def entity_to_dto(entity):
        return TrainingImpulseDTO(
            id=entity.id,
            simplified_banister_trimp=entity.simplified_banister_trimp,
            advanced_banister_trimp=entity.advanced_banister_trimp,
            edwards_trimp=entity.edwards_trimp,
            recovery_factor=entity.recovery_factor,
            metrics_id=entity.metrics_id
        )