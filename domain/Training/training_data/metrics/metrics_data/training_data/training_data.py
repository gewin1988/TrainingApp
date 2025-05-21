from domain.Training.training_data.metrics.metrics_data.real_time_training_data.real_time_training_data import \
    RealTimeTrainingData


class TrainingData:
    def __init__(self, zone_dto_list):
        self.current_data = RealTimeTrainingData(zone_dto_list)
        self.post_training_data = None #ez lesz a post session