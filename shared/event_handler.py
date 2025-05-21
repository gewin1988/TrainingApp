# shared/event_handler.py
import asyncio


from typing import TypeVar, Generic, Callable, Optional
import asyncio

# Típusváltozók a különböző eseményadatokhoz
T = TypeVar('T')
U = TypeVar('U')

class EventHandler(Generic[T]):
    def __init__(self):
        self.listeners = []

    def add_listener(self, callback: Callable[[T], None]):
        self.listeners.append(callback)

    async def raise_event(self, event_data: T):
        tasks = []
        for listener in self.listeners:
            if asyncio.iscoroutinefunction(listener):
                tasks.append(listener(event_data))
            else:
                listener(event_data)
        if tasks:
            await asyncio.gather(*tasks)

# # Példa használatra
# hr_event_handler = EventHandler[HrEventData]()  # HrEventData típusú eseményekhez
# simple_event_handler = EventHandler[None]()    # Paraméter nélküli eseményekhez
# my3d_event_handler = EventHandler[My3DClass]() # My3DClass típusú eseményekhez
#
# # Feliratkozók hozzáadása
# hr_event_handler.add_listener(lambda data: print(f"HR Event: {data.employee_name}"))
# simple_event_handler.add_listener(lambda: print("Simple Event triggered!"))
# my3d_event_handler.add_listener(lambda data: print(f"3D Event: {data}"))
#
# # Események kiváltása
# hr_event = HrEventData(event_type='employee_added', employee_id=1, employee_name='John Doe')
# my3d_event = My3DClass()  # Tegyük fel, hogy ez a My3DClass egy példány
#
# asyncio.run(hr_event_handler.raise_event(hr_event))
# asyncio.run(simple_event_handler.raise_event(None))
# asyncio.run(my3d_event_handler.raise_event(my3d_event))