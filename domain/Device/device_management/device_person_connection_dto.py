class DevicePersonConnectionDTO:
    def __init__(self, id, device_mac, owner_id):
        self.id = id
        self.device_mac = device_mac
        self.owner_id = owner_id