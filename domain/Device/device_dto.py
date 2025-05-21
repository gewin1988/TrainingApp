class BLEHrDeviceDTO:
    def __init__(self, id, mac_address, brand, type:str):
        self.id = id
        self.mac_address = mac_address
        self.brand = brand
        self.type = type