from domain.Person.person_model import PersonModel


class HrDataEvent:
    def __init__(self, data, sender:PersonModel, timestamp):
        self.data = data
        self.timestamp = timestamp
        self.sender = sender