"""
    Max hr calculation modes:
    simple: simpliest
    Tanaka_Gulati: Tanaka and Gulati formula
"""
MAX_HR_CALCULATION_DEFAULT = "simple"
MAX_HR_CALCULATION_MODE = "simple"

MAX_HR_OPTIMIZATION = False
"""
    Fitness training levels:
    not_trained
    under_trained
    averagely_trained
    moderately_trained
    highly_trained
"""
FITNESS_LEVEL_DEFAULT = "not_trained"
"""
    Use this coefficient to fine-tune the max hr
"""
UNDER_TRAINED_COEFFICIENT = 0.65
AVERAGELY_TRAINED_COEFFICIENT = 0.75
MODERATELY_TRAINED_COEFFICIENT = 0.9
HIGHLY_TRAINED_COEFFICIENT = 0.95

NAME_MIN_LEN = 2

AGE_LOWER_BOUND = 10
AGE_UPPER_BOUND = 100

HEIGHT_LOWER_BOUND = 50
HEIGHT_UPPER_BOUND = 220

WEIGHT_LOWER_BOUND = 20
WEIGHT_UPPER_BOUND = 250

VALID_GENDERS = ["male", "female"]

