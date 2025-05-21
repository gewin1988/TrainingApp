from domain.Device.device_dto import BLEHrDeviceDTO


class BLEHrDeviceModel:
    def __init__(self, dto):
        self.id = dto.id
        self.mac_address = dto.mac_address
        self.brand = dto.brand
        self.type = dto.type

    def __str__(self):
        return f"Address: {self.mac_address}, Brand: {self.brand}, Type: {self.type}"

    def to_dto(self):
        return BLEHrDeviceDTO(id=self.id, mac_address=self.mac_address, brand=self.brand, type=self.type)