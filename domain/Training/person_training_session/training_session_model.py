from datetime import datetime

from domain.Training.person_training_session.training_session_dto import TrainingSessionDTO
from domain.Training.training_data.metrics.training_metrics_model import TrainingMetricsModel
from shared.event_handler import EventHandler


class TrainingSessionModel:

    # def __init__(self,start_time, end_time, location, name, duration, metrics, person_id,team_training_id ):
        # self.id = dto.id
    def __init__(self, name, location, metrics):
        self.start_time = None
        self.end_time = None
        self.location = location
        self.name = name
        self.duration = None  # Total session time in seconds
        self.metrics = metrics

    def __str__(self):
        return f"Name: {self.name}, location: {self.location}, start: {self.start_time}, end: {self.end_time}, duration(seconds): {self.duration}"

    def to_dto(self):
        return TrainingSessionDTO(name = self.name, location=self.location,start_time=self.start_time,end_time=self.end_time,
                                  duration=self.duration, metrics_id=self.metrics.id)

    def start_session(self):
        self.start_time = datetime.now()
        self.metrics.set_start_time(self.start_time)

    def stop_session(self, user_name, age, gender, weight, height, hr_max, resting_hr, heart_rate_reserve):
        self.end_time = datetime.now()
        self.duration = self.end_time-self.start_time
        self.metrics.calculate_post_training_data(user_name=user_name, duration=self.duration, age=age, gender=gender, weight=weight,
                                                  height=height, hr_max=hr_max, resting_hr=resting_hr, heart_rate_reserve = heart_rate_reserve)

    def end_session(self):
        self.end_time = datetime.now()
        self.duration = self.end_time-self.start_time

    # def init_session_metrics(self, person_hr_max):
    #     self.metrics = TrainingMetricsModel(TrainingMetricsMapper.entity_to_dto())