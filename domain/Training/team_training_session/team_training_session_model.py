from domain.Person.person_model import PersonModel
from domain.Training.person_training_session.training_session_model import TrainingSessionModel


class TeamTrainingSessionModel:
    
    def __init__(self, name, place, date):
        self.name = name
        self.place = place
        self.date = date
        # self.participant_sessions: list[TrainingSessionModel] = []
        self.participants: list[PersonModel] = []

    # def add_participant_session(self, training_session):
    #     self.participant_sessions.append(training_session)

    def add_participant(self, participant):
        self.participants.append(participant)

    def init_team_training(self):
        for participant in self.participants:
            session = TrainingSessionModel(name="Session1_"+participant.name, location=self.place)
            session.init_session_metrics(participant.hr_max)
            participant.assign_session(session)

    def start_team_training(self):
        for participant in self.participants:
            participant.current_training_session.start_session()

    def stop_team_training(self):
        for participant in self.participants:
            participant.current_training_session.stop_session(user_name=participant.name, age=participant.age,
                                                              gender=participant.gender, weight=participant.weight,
                                                              height=participant.height, hr_max=participant.hr_max,
                                                              resting_hr=participant.resting_hr,
                                                              heart_rate_reserve=participant.heart_rate_reserve)