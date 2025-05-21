from domain.Training.training_data.metrics.metrics_data.base.base_training_data import BaseTrainingData


class PostSessionTrainingData(BaseTrainingData):
    def __init__(self, person_hr_max):
        super().__init__(person_hr_max=person_hr_max)
        self.epoc = 0
        self.avg_hr_to_hr_max_ratio = None