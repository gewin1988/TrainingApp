from domain.Device.device_dto import BLEHrDeviceDTO
from domain.Device.device_entity import BLEHrDeviceEntity
from domain.Device.device_model import  BLEHrDeviceModel


class DeviceMapper:
    @staticmethod
    def dto_to_entity(dto):
        return BLEHrDeviceEntity(
            id=dto.id,
            mac_address=dto.mac_address,
            brand=dto.brand,
            type=dto.type,

        )

    @staticmethod
    def entity_to_dto(entity):
        return BLEHrDeviceDTO(
            id=entity.id,
            mac_address=entity.mac_address,
            brand=entity.brand,
            type=entity.type,

        )