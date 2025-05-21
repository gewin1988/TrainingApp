from domain.Training.zone.zone_dto import ZoneDTO
from domain.Training.zone.zone_entity import ZoneEntity
from domain.Training.zone.zone_model import ZoneModel


class ZoneMapper:
    @staticmethod
    def dto_to_entity(dto):
        return ZoneEntity(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            lower_bound=dto.lower_bound,
            upper_bound=dto.upper_bound,
            weight_factor=dto.weight_factor,
            time_spent=dto.time_spent,
            time_percentage=dto.time_percentage
        )

    @staticmethod
    def entity_to_dto(entity):
        return ZoneDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            lower_bound=entity.lower_bound,
            upper_bound=entity.upper_bound,
            weight_factor=entity.weight_factor,
            time_spent = entity.time_spent,
            time_percentage = entity.time_percentage
        )

    @classmethod
    def entity_list_to_dto_list(cls, zone_entity_list):
        return [ZoneMapper.entity_to_dto(zone) for zone in zone_entity_list]