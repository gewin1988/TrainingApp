from domain.Person.person_model import PersonModel
from domain.Training.person_training_session.training_session_model import TrainingSessionModel


class StopSessionEvent:
    def __init__(self, person:PersonModel):
        self.person = person