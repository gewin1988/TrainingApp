from domain.Person.person_config import *
from configuration.symbols import SYMBOL_ERROR

def check_name(name:str) -> bool:
    if not name or len(name) < NAME_MIN_LEN:
        print(f"{SYMBOL_ERROR} Name must be at least {NAME_MIN_LEN} characters long.")
        return False
    return True

def check_gender(gender:str)->bool:
    if gender.lower() not in VALID_GENDERS:
        print(f"{SYMBOL_ERROR} Invalid gender: use one of: {VALID_GENDERS}.")
        return False
    return True

def check_age(age: int) -> bool:
    if not (AGE_LOWER_BOUND < age < AGE_UPPER_BOUND):
        print (f"{SYMBOL_ERROR} Age must be between {AGE_LOWER_BOUND} and {AGE_UPPER_BOUND}.")
        return False
    return True

def check_weight(weight:int)->bool:
    if not (WEIGHT_LOWER_BOUND <= weight <= WEIGHT_UPPER_BOUND):
        print(f"{SYMBOL_ERROR} Weight must be between {WEIGHT_LOWER_BOUND}kg and {WEIGHT_UPPER_BOUND}kg.")
        return False
    return True

def check_height(height:int)->bool:
    if not (HEIGHT_LOWER_BOUND <= height <= HEIGHT_UPPER_BOUND):
        print(f"{SYMBOL_ERROR} Height must be between {HEIGHT_LOWER_BOUND}cm and {HEIGHT_UPPER_BOUND}cm.")
        return  False
    return True
