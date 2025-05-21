from domain.Person.person_dto import PersonDTO
from domain.Person.person_entity import PersonEntity
from domain.Person.person_model import PersonModel


class PersonMapper:
    @staticmethod
    def entity_to_dto(entity):
        return PersonDTO(id = entity.id, age = entity.age, name=entity.name, gender=entity.gender, weight=entity.weight, height=entity.weight, fitness_level = entity.fitness_level,
                         resting_hr = entity.resting_hr, max_hr_calculation_algorythm = entity.max_hr_calculation_algorythm, bmi=entity.bmi,
                         vo2_max=entity.vo2_max, heart_rate_reserve=entity.heart_rate_reserve, hr_max=entity.hr_max)

    @staticmethod
    def dto_to_entity(dto):
        return PersonEntity(id = dto.id, name=dto.name, age = dto.age, gender=dto.gender, weight=dto.weight, height=dto.weight, fitness_level = dto.fitness_level,
                            resting_hr = dto.resting_hr, max_hr_calculation_algorythm = dto.max_hr_calculation_algorythm, hr_max = dto.hr_max,
                            vo2_max=dto.vo2_max,  heart_rate_reserve = dto.heart_rate_reserve,  bmi = dto.bmi)



    # @staticmethod
    # def to_entity(person_model):
    #     return PersonEntity(
    #         name=person_model.name,
    #         gender=person_model.gender,
    #         age=person_model.age,
    #         weight=person_model.weight,
    #         height=person_model.height,
    #         fitness_level=person_model.fitness_level,
    #         resting_hr=person_model.resting_hr,
    #         max_hr_calculation_algorythm=person_model.hr_max_calc_algo,
    #         max_hr_optimization=person_model.max_hr_optimization,
    #         hr_max = person_model.hr_max,
    #         vo2_max = person_model.vo2_max,
    #         heart_rate_reserve = person_model.heart_rate_reserve,
    #         bmi = person_model.bmi
    #     )
    #
    # @staticmethod
    # def to_model(person_entity):
    #     person_model = PersonModel(
    #         name = person_entity.name,
    #         gender = person_entity.gender,
    #         age = person_entity.age,
    #         weight = person_entity.weight,
    #         height = person_entity.height,
    #         fitness_level = person_entity.fitness_level,
    #         resting_hr = person_entity.resting_hr,
    #         max_hr_calculation_algorythm = person_entity.hr_max_calc_algo
    #     )
    #     person_model.id = person_entity.id
    #     return person_model