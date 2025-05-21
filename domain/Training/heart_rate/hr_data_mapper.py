from domain.Training.heart_rate.hr_data_dto import HrDataDTO
from domain.Training.heart_rate.hr_data_entity import HrDataEntity
from domain.Training.heart_rate.hr_data_model import HrDataModel


class HrDataMapper:
    @staticmethod
    def dto_to_entity(dto):
        return HrDataEntity(
            id = dto.id,
            timestamp=dto.timestamp,
            value=dto.value,
            training_metrics_id = dto.training_metrics_id
        )

    @staticmethod
    def entity_to_dto(entity):
        return HrDataDTO(
            id = entity.id,
            timestamp=entity.timestamp,
            value=entity.value,
            training_metrics_id = entity.training_metrics_id
        )