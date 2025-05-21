from domain.Training.training_data.impulse.impulse_config import RECOVERY_FACTOR_AVG
from domain.Training.training_data.impulse.training_impulse_dto import TrainingImpulseDTO


class TrainingImpulseModel:
    def __init__(self,dto):
        self.id = dto.id
        self.simplified_banister_trimp = dto.simplified_banister_trimp
        self.advanced_banister_trimp = dto.advanced_banister_trimp
        self.edwards_trimp = dto.edwards_trimp
        self.metrics_id = dto.metrics_id
        self.recovery_factor = dto.recovery_factor

    def __str__(self):
        return f"Simplified Banister: {self.simplified_banister_trimp}, Advanced Banister: {self.advanced_banister_trimp}, Edwards: {self.edwards_trimp}"

    def to_dto(self):
        return TrainingImpulseDTO(id=self.id, simplified_banister_trimp=self.simplified_banister_trimp, advanced_banister_trimp=self.advanced_banister_trimp,
                                  edwards_trimp=self.edwards_trimp, metrics_id=self.metrics_id, recovery_factor = self.recovery_factor)