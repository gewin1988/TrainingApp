from domain.Device.device_management.device_person_connection_dto import DevicePersonConnectionDTO


class DevicePersonConnectionModel:
    def __init__(self, dto):
        self.id = dto.id
        self.device_mac = dto.device_mac
        self.owner_id = dto.owner_id

    def to_dto(self):
        return DevicePersonConnectionDTO(id = self.id, device_mac=self.device_mac, owner_id=self.owner_id)