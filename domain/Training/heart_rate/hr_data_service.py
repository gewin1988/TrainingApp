from domain.Training.heart_rate.hr_data_entity import HrDataEntity

from domain.Training.heart_rate.hr_data_repository import HrDataRepository
from domain.base.base_service import BaseService


class HrDataService(BaseService[HrDataEntity]):
    def __init__(self, repository: HrDataRepository):
        super().__init__(repository)


    def create(self, value, timestamp):
        hr_data = HrDataEntity(value=value, timestamp=timestamp)
        return self.repository.create(hr_data)