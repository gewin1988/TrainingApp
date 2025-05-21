class TrainingMetricsDTO:
    def __init__(self, id, training_stress_score, epoc, caloric_expenditure, resting_calories_by_training, zoladz_calories,
                 mifflin_st_jeor_calories, max_hr, min_hr, avg_hr, avg_hr_to_hr_max_ratio, intensity_factor):
        self.id = id
        self.training_stress_score = training_stress_score
        self.epoc = epoc
        self.caloric_expenditure = caloric_expenditure
        self.resting_calories_by_training = resting_calories_by_training
        self.zoladz_calories = zoladz_calories
        self.mifflin_st_jeor_calories =mifflin_st_jeor_calories
        self.max_hr = max_hr
        self.min_hr = min_hr
        self.avg_hr = avg_hr
        self.avg_hr_to_hr_max_ratio =avg_hr_to_hr_max_ratio
        self.intensity_factor = intensity_factor

