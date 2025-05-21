class PersonDTO:
    def __init__(self, id, name, age, gender, weight, height, fitness_level, resting_hr, max_hr_calculation_algorythm,
                 hr_max, vo2_max, heart_rate_reserve, bmi):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.fitness_level = fitness_level
        self.resting_hr = resting_hr
        self.max_hr_calculation_algorythm = max_hr_calculation_algorythm
        self.hr_max = hr_max
        self.vo2_max = vo2_max
        self.heart_rate_reserve = heart_rate_reserve
        self.bmi = bmi