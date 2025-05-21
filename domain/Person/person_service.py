# /services/person_service.py
from domain.Person.person_repository import PersonRepository
from domain.Person.person_entity import PersonEntity
from domain.Person.person_utils import *
from domain.base.base_service import BaseService
from configuration.symbols import SYMBOL_ERROR


class PersonService(BaseService[PersonEntity]):

    def __init__(self, repository: PersonRepository):
        super().__init__(repository)

    def create(self, name, gender, age, weight, height, fitness_level=FITNESS_LEVEL_DEFAULT, resting_hr=60,
               max_hr_calculation_algorythm=MAX_HR_CALCULATION_DEFAULT) -> PersonEntity:
        if not check_name(name):
            raise ValueError(f"{SYMBOL_ERROR} invalid name length")

        if not check_gender(gender):
            raise ValueError(f"{SYMBOL_ERROR} Invalid gender")

        if not check_age(age):
            raise ValueError(f"{SYMBOL_ERROR} Invalid age")

        if not check_weight(weight):
            raise ValueError(f"{SYMBOL_ERROR} Invalid weight")

        if not check_height(height):
            raise ValueError(f"{SYMBOL_ERROR} Invalid height")

        new_person = PersonEntity(name = name, gender = gender, age = age, weight = weight, height=height,
                                  fitness_level=fitness_level, resting_hr=resting_hr,
                                  max_hr_calculation_algorythm=max_hr_calculation_algorythm)
        return self.repository.create(new_person)
