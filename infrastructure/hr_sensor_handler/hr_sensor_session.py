import asyncio
import random
import time
from datetime import datetime, timedelta

from bleak import BleakClient, BleakError

from configuration.symbols import SYMBOL_ERROR, SYMBOL_INFO
from infrastructure.hr_sensor_handler.hr_sensor_config import HEART_RATE_CHARACTERISTIC_UUID
from infrastructure.hr_sensor_handler.interfaces.interface_hr_sensor_session import IHrSensorSession

# Constants
WARM_UP_DURATION = 600  # 10 minutes in seconds
HARD_WORK_DURATION = 4200  # 70 minutes in seconds
RAMP_DOWN_DURATION = 600  # 10 minutes in seconds
WARM_UP_HR_MIN = 60
WARM_UP_HR_MAX = 100
HARD_WORK_HR_MIN = 120
HARD_WORK_HR_MAX = 170
RAMP_DOWN_HR_MIN = 80

class DeviceTest:
    def __init__(self):
        self.INTERVALS = [
            (1, 60, 70),   # 1 minute, range 60-70
            (1, 70, 80),   # 1 minute, range 70-80
            (1, 80, 90),   # 1 minute, range 80-90
            (1, 90, 120),  # 1 minute, range 90-120
            (1, 120, 150), # 1 minute, range 120-150
            (1, 90, 120),  # 1 minute, range 90-120
            (1, 60, 90),   # 1 minute, range 60-90
        ]
    def get_intervals(self):
        return self.INTERVALS

    def generate_heart_rate(self,interval_index, previous_rate):
        """Generate a heart rate value based on the current interval and previous rate."""
        _, lower, upper = self.INTERVALS[interval_index]
        # Ensure the new rate is the same or slightly higher than the previous rate
        new_rate = random.randint(lower, upper)
        return max(previous_rate, new_rate)

class HrDeviceSession(IHrSensorSession):
    """Manages a single BLE heart rate sensor connection."""

    def __init__(self, address: str, callback):
        self.address = address
        self.callback = callback
        self.client = BleakClient(address)
        self.connected = False
        self._disconnect_event = asyncio.Event()
        self.counter = 0
        self.__tester = DeviceTest()
        self.connected_lock = asyncio.Lock()

    def assign_callback(self, callback):
        if callback:
            self.callback=callback

    async def  on_hr_data_arrived(self, sender, data, timestamp = None):
        """Handles incoming HR data and forwards it to the correct function."""
        if self.callback:
            if timestamp is None:
                self.callback(sender, data, datetime.now())
            else:
                self.callback(sender, data, timestamp)
        # else:
            # print(f"{SYMBOL_ERROR} Callback not set!")

        # Register a disconnection callback
    def handle_disconnect(self, client:BleakClient):
        print(f"{SYMBOL_INFO} Device {self.address} disconnected.")
        self.connected = False
        self._disconnect_event.set()  # <-- TRIGGER DISCONNECT

    async def connect(self):
        """Connect to the BLE device and start listening for HR data, with auto-reconnect."""
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                print(f"{SYMBOL_INFO} Attempting to connect to {self.address}...")
                await self.client.connect()

                async with self.client:
                    print(f"{SYMBOL_INFO} Connected to {self.address}")
                    self.connected = True
                    retry_count = 0  # Reset retry counter on success
                    self.client.set_disconnected_callback(self.handle_disconnect)

                    # Start notifications
                    await self.client.start_notify(
                        HEART_RATE_CHARACTERISTIC_UUID,
                        self.on_hr_data_arrived
                    )

                    # Wait for disconnect event
                    await self._disconnect_event.wait()

            except BleakError as e:
                retry_count += 1
                print(f"{SYMBOL_ERROR} Connection failed ({retry_count}/{max_retries}) for {self.address}: {e}")

            self.connected = False
            self._disconnect_event.clear()  # Reset event for next retry
            await asyncio.sleep(5)  # Wait before retrying

        print(f"{SYMBOL_ERROR} Max retries reached. Giving up on {self.address}")

    async def disconnect(self):
        """Disconnect from the BLE device."""
        if self.client.is_connected:
            await self.client.disconnect()
            print(f"{SYMBOL_INFO} Disconnected from {self.address}")

    async def simulated_connect(self):
        """Establish BLE connection"""
        self.connected = True
        print(f"Simulation Connected to {self.address}")


    async def ensure_connected(self):
        """
       Ensure the device is connected. If not, connect it.
       """
        if not self.connected:
            await self.simulated_connect()

    async def ensure_disconnected(self):
        """
       Ensure the device is connected. If not, connect it.
       """
        if self.connected:
            await self.simulated_disconnect()

    async def simulated_disconnect(self):
        """Establish BLE connection"""
        self.connected = False
        print(f"Disconnected from {self.address}")

    async def simulate_hr_data(self):
        """
        Simulate heart rate metrics_data by calling the __callback with random values every second.
        """
        while True and self.counter<5:
            self.counter+=1
            hr = random.randint(60, 190)  # Random heart rate between 60 and 120
            # print(f"simulate hr for:{self.address} : {hr}")
            # if self.__callback is None:
            #     print("__callback lost")
            # if self.__is_connected is False:
            #     print("connection lost")
            if self.connected:
                # print(f"{SYMBOL_INFO} simualte hr data: {hr} for {self.address}")
                await self.on_hr_data_arrived(data=hr, sender=self.address)  # Call the __callback with the simulated metrics_data
            # else:
                # print(f"{SYMBOL_ERROR} client not connected")
            await asyncio.sleep(1)  # Wait for 1 second

    def generate_hr_data(self, start_time):
        """
        Simulate HR data for a 1.5-hour training session.
        :param start_time: The start time of the training session (datetime object).
        """
        current_time = start_time

        # Warm-up phase (0–10 minutes)
        for second in range(WARM_UP_DURATION):
            hr_value = WARM_UP_HR_MIN + (WARM_UP_HR_MAX - WARM_UP_HR_MIN) * (second / WARM_UP_DURATION)
            yield current_time, hr_value
            current_time += timedelta(seconds=1)

        # Hard work phase (10–80 minutes)
        for second in range(HARD_WORK_DURATION):
            hr_value = random.randint(HARD_WORK_HR_MIN, HARD_WORK_HR_MAX)
            yield current_time, hr_value
            current_time += timedelta(seconds=1)

        # Ramp-down phase (80–90 minutes)
        for second in range(RAMP_DOWN_DURATION):
            hr_value = HARD_WORK_HR_MAX - (HARD_WORK_HR_MAX - RAMP_DOWN_HR_MIN) * (second / RAMP_DOWN_DURATION)
            yield current_time, hr_value
            current_time += timedelta(seconds=1)

    async def simulate_training(self):
        """
        Simulate a 1.5-hour training session and process HR data as fast as possible.
        """
        await asyncio.sleep(5)
        print("Simulate training started")
        for timestamp, hr_value in self.generate_hr_data(datetime.now()):
            async with self.connected_lock:  # Biztonságos hozzáférés a self.connected változóhoz
                if self.connected:
                    # Az on_hr_data_arrived függvényt aszinkron módon indítjuk, de nem várjuk meg
                    await asyncio.create_task(self.on_hr_data_arrived(self.address, hr_value, timestamp))
            # No delay between iterations (run as fast as possible)