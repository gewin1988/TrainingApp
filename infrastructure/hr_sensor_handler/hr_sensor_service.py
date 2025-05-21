import asyncio
import random

from configuration.symbols import SYMBOL_ERROR
from domain.Device.device_management.device_person_connection_service import DevicePersonConnectionService, \
    InMemoryDevicePersonConnectionService
from domain.Device.device_service import DeviceService
from domain.Person.person_service import PersonService
# from domain.TrainingSessionManager.training_session_manager import TrainingSessionManager
from domain.events.hr_data_event import HrDataEvent
from infrastructure.hr_sensor_handler.hr_sensor_session import HrDeviceSession
from infrastructure.hr_sensor_handler.interfaces.interface_hr_sensor_service import  IHRSensorService
from shared.event_handler import EventHandler


class HrSensorService(IHRSensorService):

    def __init__(self, hr_event_handler: EventHandler):

        self.__sessions = {}  # {ble_address: BLEDeviceSession}
        self.session_tasks = None
        self.event_handler = hr_event_handler
        # self.training_session_manager = training_session_manager

    def register_device(self, ble_address: str, callback):
        """Register a new BLE device and its callback function."""
        if ble_address in self.__sessions:
            print(f"Device {ble_address} is already registered.")
            return

        session = HrDeviceSession(ble_address, callback)
        self.__sessions[ble_address] = session

    async def start_all_connections(self):
        """Start BLE connections for all registered devices."""
        # tasks = [session.connect() for session in self.__sessions.values()]
        tasks = [session.ensure_connected() for session in self.__sessions.values()]
        await asyncio.gather(*tasks)

    async def stop_all_connections(self):
        """Start BLE connections for all registered devices."""
        # tasks = [session.connect() for session in self.__sessions.values()]
        tasks = [session.ensure_disconnected() for session in self.__sessions.values()]
        await asyncio.gather(*tasks)

    async def start_all_simulations(self):
        await self.start_all_connections()
        # self.session_tasks = [session.simulate_hr_data() for session in self.__sessions.values()]
        self.session_tasks = [session.simulate_training() for session in self.__sessions.values()]
        await asyncio.gather(*self.session_tasks)

    async def stop_all_simulations(self):
        #todo: stop tasks

        await self.stop_all_connections()


    async def disconnect_device(self, ble_address: str):
        """Disconnect a specific device."""
        session = self.__sessions.pop(ble_address, None)
        if session:
            await session.disconnect()

    async def disconnect_all(self):
        """Disconnect all devices."""
        tasks = [session.ensure_disconnected() for session in self.__sessions.values()]
        await asyncio.gather(*tasks)
        self.__sessions.clear()

    def process_hr_data(self, sender, data, timestamp):

        in_memory_device_person_connection_service = InMemoryDevicePersonConnectionService()
        device_owner = in_memory_device_person_connection_service.get_owner_by_device_id_from_cache(sender)
        event = HrDataEvent(data, device_owner, timestamp)
        # print(f"new hr data: {data} at {timestamp} from: {sender} - {device_owner.name}")
        asyncio.create_task(self.event_handler.raise_event(event))

        # device_owner_id = self.device_person_connection_manager_service.get_owner_by_device_id_from_cache(sender)
        # session_id = self.training_session_manager.get_active_session(device_owner_id)
        #
        # if device_owner_id:
        #     if device_owner_id == 1:
        #         data = random.randint(1, 30)
        #     elif device_owner_id == 2:
        #         data = random.randint(30, 60)
        #     else:
        #         data = random.randint(60, 90)
        #
        #     # raise event
        #     event = HrDataEvent(data, session_id, timestamp)
        #     # print(f"event raised with: {data} - {device_owner_id}")
        #     # self.event_handler.raise_event(event)
        #     # todo: send hr data to redis
        # asyncio.create_task(self.event_handler.raise_event(event))

