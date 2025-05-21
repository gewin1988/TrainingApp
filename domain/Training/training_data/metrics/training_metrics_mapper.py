from domain.Training.training_data.metrics.training_metrics_dto import TrainingMetricsDTO
from domain.Training.training_data.metrics.training_metrics_entity import TrainingMetricsEntity
from domain.Training.training_data.metrics.training_metrics_model import TrainingMetricsModel


class TrainingMetricsMapper:
    @staticmethod
    def dto_to_entity(dto):
        return TrainingMetricsEntity(
            id = dto.id,
            intensity_factor = dto.intensity_factor,
            training_stress_score = dto.training_stress_score,
            epoc = dto.epoc  ,
            caloric_expenditure = dto.calories,
            resting_calories_by_training = dto.resting_calories,
            zoladz_calories=dto.zoladz_calories,
            mifflin_st_jeor_calories = dto.mifflin_st_jeor_calories,
            max_hr = dto.max_hr,
            min_hr = dto.min_hr,
            avg_hr = dto.avg_hr,
            avg_hr_to_hr_max_ratio = dto.avg_hr_to_hr_max_ratio
        )

    @staticmethod
    def entity_to_dto(entity):
        return TrainingMetricsDTO(
            id=entity.id,
            intensity_factor=entity.intensity_factor,
            training_stress_score=entity.training_stress_score,
            epoc=entity.epoc,
            caloric_expenditure=entity.caloric_expenditure,
            resting_calories_by_training=entity.resting_calories_by_training,
            zoladz_calories=entity.zoladz_calories,
            mifflin_st_jeor_calories=entity.mifflin_st_jeor_calories,
            max_hr=entity.max_hr,
            min_hr=entity.min_hr,
            avg_hr=entity.avg_hr,
            avg_hr_to_hr_max_ratio=entity.avg_hr_to_hr_max_ratio
        )