from abc import ABC, abstractmethod

from shared.event_handler import EventHandler


class IHRSensorService(ABC):


    @abstractmethod
    def register_device(self, ble_address: str, callback):
        """Register a new BLE device and its callback function."""
        pass

    @abstractmethod
    async def start_all_connections(self):
        """Start BLE connections for all registered devices."""
        pass

    @abstractmethod
    async def disconnect_device(self, ble_address: str):
        """Disconnect a specific device."""
        pass

    @abstractmethod
    async def disconnect_all(self):
        """Disconnect all devices."""
        pass

    @abstractmethod
    def process_hr_data(self, sender, data, timestamp):
        """Process received heart rate data."""
        pass
