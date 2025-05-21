from abc import ABC, abstractmethod
from typing import Protocol


class IHrSensorSession(ABC):
    @abstractmethod
    async def connect(self):
        """Establish a connection to the BLE device."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect from the BLE device."""
        pass

    @abstractmethod
    async def ensure_connected(self):
        """Ensure the device is connected, reconnect if needed."""
        pass

    @abstractmethod
    async def ensure_disconnected(self):
        """Ensure the device is disconnected."""
        pass

    @abstractmethod
    def on_hr_data_arrived(self, sender, data):
        """Handle received heart rate data from the BLE device."""
        pass