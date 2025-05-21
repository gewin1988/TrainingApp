from domain.Training.training_data.impulse.training_impulse_entity import TrainingImpulseEntity
from domain.Training.training_data.impulse.training_impulse_repository import TrainingImpulseRepository
from domain.base.base_service import BaseService


class TrainingImpulseService(BaseService[TrainingImpulseEntity]):
    def __init__(self, repository: TrainingImpulseRepository):
        super().__init__(repository)

    def create(self, simple_banister, advanced_banister, ed) -> TrainingImpulseEntity:
        new_impulse = TrainingImpulseEntity(simple_banister=simple_banister, advanced_banister=advanced_banister, edwards=edwards)
        return self.repository.create(new_impulse)