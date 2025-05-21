class CaloriesModel:
    def __init__(self, calories_burnt, resting_calories, zoladz_calories, mifflin_st_jeor_calories):
        self.caloric_expenditure = calories_burnt
        self.resting_calories = resting_calories  # Basal Metabolic Rate (BMR) per day Mifflin-St Jeor formula
        self.zoladz_calories = zoladz_calories
        self.mifflin_st_jeor_calories = mifflin_st_jeor_calories