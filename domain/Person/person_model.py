from flask import Flask

from configuration.symbols import SYMBOL_ERROR
from domain.Person.person_config import MAX_HR_CALCULATION_DEFAULT, UNDER_TRAINED_COEFFICIENT, \
    AVERAGELY_TRAINED_COEFFICIENT, MODERATELY_TRAINED_COEFFICIENT, HIGHLY_TRAINED_COEFFICIENT, MAX_HR_OPTIMIZATION
from domain.Person.person_dto import PersonDTO
from domain.Training.person_training_session.training_session_model import TrainingSessionModel

app = Flask(__name__)

class PersonModel:
    def __init__(self, dto):
        self.id = dto.id
        self.name = dto.name
        self.gender = dto.gender
        self.age = dto.age
        self.weight = dto.weight
        self.height = dto.height
        self.fitness_level = dto.fitness_level
        self.resting_hr = dto.resting_hr
        self.max_hr_calculation_algorythm = dto.max_hr_calculation_algorythm
        self.max_hr_optimization = MAX_HR_OPTIMIZATION
        self.hr_max = self.calculate_max_hr(dto.max_hr_calculation_algorythm)
        self.vo2_max = self.calculate_vo2_max(self.hr_max, self.resting_hr)
        self.heart_rate_reserve = self.calculate_hrr(self.hr_max, self.resting_hr)
        self.bmi = self.calculate_bmi()
        self.current_training_session = None

    def __hash__(self):
        # A hash érték a name, age, weight és height alapján számolódik
        return hash((self.name, self.age, self.weight, self.height))

    def __eq__(self, other):
        # Két Person objektum egyenlő, ha a name, age, weight és height mezőik megegyeznek
        return (
                isinstance(other, PersonModel)
                and self.name == other.name
                and self.age == other.age
                and self.weight == other.weight
                and self.height == other.height
        )

    def __str__(self):
        return (f"Id: {self.id} Name: {self.name}, Gender:{self.gender}, Age: {self.age}, "
                f"Weight: {self.weight}, Height: {self.height},"
                f" Fitness level: {self.fitness_level}, Max HR: {self.hr_max}, VO2 max: {self.vo2_max}"
                f"bmi: {self.bmi}")

    def to_dto(self):
        return PersonDTO(id=self.id, name=self.name, age = self.age, gender = self.gender, weight = self.weight, height = self.height,
                         fitness_level=self.fitness_level, hr_max=self.hr_max, resting_hr=self.resting_hr, max_hr_calculation_algorythm=self.max_hr_calculation_algorythm,
                         vo2_max=self.vo2_max, heart_rate_reserve=self.heart_rate_reserve, bmi=self.bmi)

    def assign_session(self, session:TrainingSessionModel):
        self.current_training_session = session

    def calculate_bmi(self):
        height_in_m = self.height / 100
        return self.weight / (height_in_m * height_in_m)

    def calculate_hrr(self, hr_max, resting_hr):
        return hr_max - resting_hr

    def calculate_vo2_max(self, hr_max, resting_hr):
        vo2_max = 15.3 * (hr_max / resting_hr)
        return vo2_max

    def calculate_max_hr(self, mode):
        if mode.lower() == "simple":
            base_hr_max = 220 - self.age
        elif mode.lower() == "Tanaka_Gulati":
            if self.gender.lower() == "male":  # Tanaka
                base_hr_max = 208 - (self.age * 0.7)
            elif self.gender.lower() == "female":  # Gulati
                base_hr_max = 206 - (self.age * 0.88)
            else:
                raise ValueError(f"{SYMBOL_ERROR} Gender must be 'male' or 'female'")
        else:
            raise ValueError(
                f"{SYMBOL_ERROR} Expected: Max HR calculation should be simple or Tanaka_Gulati. Received: {mode} ")

        if self.max_hr_optimization:
            if self.fitness_level == "not_trained":
                return round(base_hr_max)
            elif self.fitness_level == "under_trained":
                return round(base_hr_max * UNDER_TRAINED_COEFFICIENT)
            elif self.fitness_level == "averagely_trained":
                return round(base_hr_max * AVERAGELY_TRAINED_COEFFICIENT)
            elif self.fitness_level == "moderately_trained":
                return round(base_hr_max * MODERATELY_TRAINED_COEFFICIENT)  # Slightly lower for moderately trained
            elif self.fitness_level == "highly_trained":
                return round(base_hr_max * HIGHLY_TRAINED_COEFFICIENT)  # Further lower for highly trained
            else:
                raise ValueError(f"{SYMBOL_ERROR} Unknown fitness level")
        else:
            return round(base_hr_max)
