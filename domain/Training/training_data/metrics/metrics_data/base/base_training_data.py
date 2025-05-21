from domain.Data.hr_data import HrData
from domain.Training.training_data.calories.calories_model import CaloriesModel
from domain.Training.training_data.impulse.training_impulse_model import TrainingImpulseModel
from domain.Training.training_data.metrics.metrics_config import *
from domain.Training.zone.zone_model import ZoneModel


class BaseTrainingData:
    def __init__(self, zones):

        self.hr_data: list[HrData] = []  # Üres lista inicializálása
        # Caloric relevant
        self.caloric_usage = CaloriesModel(calories_burnt=0, resting_calories=0,
                                           zoladz_calories=0,
                                           mifflin_st_jeor_calories=0)
        self.training_stress_score = 0
        self.intensity_factor = 0
        self.max_hr = 0
        self.min_hr = 0
        self.avg_hr = 0

        self.zones = zones

        self.training_impulse = TrainingImpulseModel(simplified_banister_trimp=0, advanced_banister_trimp=0,
                                             edwards_trimp=0)
