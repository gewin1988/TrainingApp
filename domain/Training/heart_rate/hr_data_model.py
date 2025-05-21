from domain.Training.heart_rate.hr_data_dto import HrDataDTO


class HrDataModel:
    def __init__(self, dto):
        self.id = dto.id
        self.timestamp = dto.timestamp
        self.value = dto.value
        self.training_metrics_id = dto.training_metrics_id

    def __str__(self):
        return f"{self.timestamp}: {self.value}"

    def to_dto(self):
        return HrDataDTO(id = self.id, timestamp = self.timestamp, value = self.value, training_metrics_id=self.training_metrics_id)