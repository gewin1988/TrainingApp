from domain.Device.device_management.device_person_connection_dto import DevicePersonConnectionDTO
from domain.Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity
from domain.Device.device_management.device_person_connection_model import DevicePersonConnectionModel


class DevicePersonConnectionMapper:
    @staticmethod
    def dto_to_entity(dto):
        return DevicePersonConnectionEntity(
            id = dto.id,
            device_mac=dto.device_mac,
            owner_id=dto.owner_id,

        )

    @staticmethod
    def entity_to_dto(entity):
        return DevicePersonConnectionDTO(
            id = entity.id,
            device_mac=entity.device_mac,
            owner_id=entity.owner_id,

        )