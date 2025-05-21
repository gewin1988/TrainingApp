from domain.Training.training_data.metrics.metrics_config import *
from domain.Training.zone.zone_entity import ZoneEntity
from domain.Training.zone.zone_repository import ZoneRepository
from domain.base.base_service import BaseService


class ZoneService(BaseService[ZoneEntity]):
    def __init__(self, repository: ZoneRepository):
        super().__init__(repository)

    def create(self, name, description, lower_bound, upper_bound, weight_factor):
        new_zone = ZoneEntity(name=name, description=description, lower_bound=lower_bound, upper_bound=upper_bound, weight_factor=weight_factor)
        return self.repository.create(new_zone)

    def create_5_zones(self, person_hr_max):
        ze0 = ZoneEntity(name=INTENSITY_ZONE0_NAME, description=INTENSITY_ZONE0_DESCRIPTION, lower_bound=0.0,
                  upper_bound=0.5 * person_hr_max, weight_factor=INTENSITY_ZONE0_WEIGHT_FACTOR)
        ze1 = ZoneEntity(name=INTENSITY_ZONE1_NAME, description=INTENSITY_ZONE1_DESCRIPTION, lower_bound=0.5 * person_hr_max,
                  upper_bound=0.6 * person_hr_max, weight_factor=INTENSITY_ZONE1_WEIGHT_FACTOR)
        ze2 = ZoneEntity(name=INTENSITY_ZONE2_NAME, description=INTENSITY_ZONE2_DESCRIPTION, lower_bound=0.6 * person_hr_max,
                  upper_bound=0.7 * person_hr_max, weight_factor=INTENSITY_ZONE2_WEIGHT_FACTOR)
        ze3 = ZoneEntity(name=INTENSITY_ZONE3_NAME, description=INTENSITY_ZONE3_DESCRIPTION, lower_bound=0.7 * person_hr_max,
                  upper_bound=0.8 * person_hr_max, weight_factor=INTENSITY_ZONE3_WEIGHT_FACTOR)
        ze4 = ZoneEntity(name=INTENSITY_ZONE4_NAME, description=INTENSITY_ZONE4_DESCRIPTION, lower_bound=0.8 * person_hr_max,
                  upper_bound=0.9 * person_hr_max, weight_factor=INTENSITY_ZONE4_WEIGHT_FACTOR)
        ze5 = ZoneEntity(name=INTENSITY_ZONE5_NAME, description=INTENSITY_ZONE5_DESCRIPTION, lower_bound=0.9 * person_hr_max,
                  upper_bound=1.0 * person_hr_max, weight_factor=INTENSITY_ZONE5_WEIGHT_FACTOR)

        return self.repository.create_bulk([ze0,ze1,ze2,ze3,ze4,ze5])