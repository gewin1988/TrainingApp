from tkinter.font import names


class TeamTrainingSessionDTO:
    def __init__(self, id, name, date, place):
        self.id = id
        self.name = name
        self.place = place
        self.date = date
