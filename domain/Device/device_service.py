from domain.Device.device_entity import BLEHrDeviceEntity
from domain.Device.device_repository import DeviceRepository
from domain.Device.device_utils import is_valid_mac
from domain.base.base_service import BaseService
from configuration.symbols import SYMBOL_ERROR, SYMBOL_EVENT
from domain.events.hr_data_event import HrDataEvent
from shared.event_handler import EventHandler


class DeviceService(BaseService[BLEHrDeviceEntity]):
    # def __init__(self, repository: DeviceRepository, event_handler: EventHandler):
    def __init__(self, repository: DeviceRepository):
        super().__init__(repository)
        # event_handler.add_listener(self.on_hr_data_event)


    def create(self, mac_address, brand:str, type:str) -> BLEHrDeviceEntity:
        if not is_valid_mac(mac_address):
            print(f"{SYMBOL_ERROR} The given address({mac_address}) is not a valid mac address!")
        new_device = BLEHrDeviceEntity(mac_address=mac_address, brand=brand, type=type)
        return self.repository.create(new_device)

    # def on_hr_data_event(self, event: HrDataEvent):
    #     # Domain logika az HR adattal
    #     print(f"{SYMBOL_EVENT} HR data - {event.data}, from user: {event.sender_id}")