from domain.Training.heart_rate.hr_data_entity import HrDataEntity
from domain.Training.training_data.metrics.metrics_config import *
from domain.Training.training_data.impulse.training_impulse_entity import TrainingImpulseEntity
from domain.Training.training_data.metrics.training_metrics_entity import TrainingMetricsEntity
from domain.Training.zone.zone_entity import ZoneEntity
from domain.Training.training_data.metrics.training_metrics_repository import TrainingMetricsRepository
from domain.Training.training_data.impulse.training_impulse_repository import TrainingImpulseRepository
from domain.Training.zone.zone_repository import ZoneRepository
from domain.base.base_service import BaseService


class TrainingMetricsService(BaseService[TrainingMetricsEntity]):
    def __init__(self, repository: TrainingMetricsRepository, training_impulse_repository: TrainingImpulseRepository, zone_repository: ZoneRepository):
        super().__init__(repository)
        self.training_impulse_repository= training_impulse_repository
        self.zones_repository = zone_repository

    def create(self, tss=0, epoc=0, calories=0, resting_calories=0, max_hr=0, min_hr=0, avg_hr=0,
               zoladz_calories = 0, mifflin_st_jeor_calories=0,
               avg_hr_to_hr_max_ratio = 0, intensity_zones = None, training_impulse=None) -> TrainingMetricsEntity:

        if isinstance(training_impulse, TrainingImpulseEntity):
            new_impulse = training_impulse
        else:
            new_impulse = TrainingImpulseEntity()

        if isinstance(intensity_zones, list):  # Csak listát fogadunk el
            if all(isinstance(zone, ZoneEntity) for zone in intensity_zones):
                new_zones_list = intensity_zones
            else:
                raise TypeError("Az intensity_zones nem csak ZoneEntity objektumokat tartalmaz.")
        else:
            # create with default values
            new_zones_list  = [
            ZoneEntity(name=INTENSITY_ZONE0_NAME, description=INTENSITY_ZONE0_DESCRIPTION, lower_bound=0, upper_bound=94, weight_factor=INTENSITY_ZONE0_WEIGHT_FACTOR),
            ZoneEntity(name=INTENSITY_ZONE1_NAME, description=INTENSITY_ZONE1_DESCRIPTION, lower_bound=95, upper_bound=114, weight_factor = INTENSITY_ZONE1_WEIGHT_FACTOR),
            ZoneEntity(name=INTENSITY_ZONE2_NAME, description=INTENSITY_ZONE2_DESCRIPTION, lower_bound=115, upper_bound=133, weight_factor=INTENSITY_ZONE2_WEIGHT_FACTOR),
            ZoneEntity(name=INTENSITY_ZONE3_NAME, description=INTENSITY_ZONE3_DESCRIPTION, lower_bound=134, upper_bound=152, weight_factor=INTENSITY_ZONE3_WEIGHT_FACTOR),
            ZoneEntity(name=INTENSITY_ZONE4_NAME, description=INTENSITY_ZONE4_DESCRIPTION, lower_bound=153, upper_bound=171, weight_factor=INTENSITY_ZONE4_WEIGHT_FACTOR),
            ZoneEntity(name=INTENSITY_ZONE5_NAME, description=INTENSITY_ZONE5_DESCRIPTION, lower_bound=172, upper_bound=190, weight_factor=INTENSITY_ZONE5_WEIGHT_FACTOR),
        ]

        new_metrics = TrainingMetricsEntity(training_stress_score=tss, epoc=epoc, caloric_expenditure=calories, resting_calories_by_training=resting_calories,
                                            zoladz_calories=zoladz_calories, mifflin_st_jeor_calories=mifflin_st_jeor_calories,
                                            avg_hr_to_hr_max_ratio = avg_hr_to_hr_max_ratio, max_hr=max_hr, min_hr=min_hr, avg_hr=avg_hr )

        # new_metrics.zones = new_zones
        self.zones_repository.create_bulk(new_zones_list)
        self.training_impulse_repository.create(new_impulse)
        new_metrics.training_impulse=new_impulse
        new_metrics.zones = new_zones_list
        return self.repository.create(new_metrics)

    # def create_intensity_zones(self):
    #
    #     zones = [
    #         ZoneEntity("Zóna 1", "Nagyon könnyű", 0, 100),
    #         ZoneEntity("Zóna 2", "Könnyű", 101, 120),
    #         ZoneEntity("Zóna 3", "Közepes", 121, 140),
    #         ZoneEntity("Zóna 4", "Nehéz", 141, 160),
    #         ZoneEntity("Zóna 5", "Nagyon nehéz", 161, 180),
    #     ]
    #
    #     return zones

    def add_zones(self, metrics_id, zones):
        metrics = self.repository.get_by_id(metrics_id)
        if metrics:
            metrics.zones = zones
            self.repository.save(metrics)

    def add_trimp_data(self, metrics_id: int, trimp_data:TrainingImpulseEntity):
        metrics = self.repository.get_by_id(metrics_id)
        if metrics:
            metrics.training_impulse = trimp_data
            self.repository.save(metrics)

    def add_hr_data(self, metrics_id: int, hr_data_list: list[HrDataEntity]):
        """Add HR data entities to a specific TrainingMetricsEntity."""
        metrics = self.repository.get_by_id(metrics_id)
        if metrics:
            for hr_data in hr_data_list:
                metrics.hr_data.append(hr_data)  # Add HR data to the relationship
            self.repository.save(metrics)  # Save the changes to the database

    def get_hr_data(self, metrics_id: int) -> list[HrDataEntity]:
        """Fetch all HR data entities associated with a specific TrainingMetricsEntity."""
        return self.repository.get_hr_data_for_metrics(metrics_id)