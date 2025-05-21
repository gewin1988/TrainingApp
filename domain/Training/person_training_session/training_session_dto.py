class TrainingSessionDTO:
    def __init__(self, id, start_time, end_time, location, name, duration, metrics_id, person_id, team_training_id):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.name = name
        self.duration = duration
        self.metrics_id = metrics_id
        self.person_id = person_id
        self.team_training_id = team_training_id