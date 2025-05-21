import asyncio
import json
from datetime import datetime, timedelta
from threading import Event

from configuration.symbols import SYMBOL_ERROR, SYMBOL_EVENT
from domain.Data.hr_data import HrData
from domain.Person.person_model import PersonModel
from domain.Training.person_training_session.training_session_model import TrainingSessionModel
from domain.Training.team_training_session.team_training_session_model import TeamTrainingSessionModel
from domain.events.hr_data_event import HrDataEvent
from domain.events.stop_session_event import StopSessionEvent
from shared import event_handler
from shared.event_handler import EventHandler

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)


class RealTimeSessionManager:
    _instance = None  # Az egyetlen példányt tároljuk itt

    def __new__(cls, *args, **kwargs):
        # Ha még nincs példány, létrehozzuk
        if not cls._instance:
            cls._instance = super(RealTimeSessionManager, cls).__new__(cls)  # Nincs *args és **kwargs
            cls._instance._initialized = False  # Jelző, hogy az __init__ még nem futott le
        return cls._instance

    def __init__(self, data, hr_event_handler: EventHandler):
        if getattr(self, '_initialized', False):
            return  # Ha már inicializálva van, ne fusson újra az __init__

        if isinstance(data, TeamTrainingSessionModel):
            self.active_users = data.participants  # Itt inicializáljuk az összes résztvevőt
        elif isinstance(data, PersonModel):
            self.active_users = [data]
        else:
            raise TypeError(f"{SYMBOL_ERROR} data must be a TeamTrainingSessionModel or a list of TrainingSessionModel")



        hr_event_handler.add_listener(self.on_hr_data_event)
        self.counter = 0
        self.running = True
        self.lock = asyncio.Lock()
        self.current_duration = timedelta()
        asyncio.create_task(self.periodic_update_mid_frequency(100))
        asyncio.create_task(self.periodic_update_high_frequency(50))
        asyncio.create_task(self.periodic_update_low_frequency(6))
        duration_task = asyncio.create_task(self.update_duration(self.active_users[0].current_training_session.start_time))
        self._initialized = True  # Jelöljük, hogy az __init__ lefutott

    def on_hr_data_event(self, event: HrDataEvent):
        # Domain logika az HR adattal
        # print(f"{SYMBOL_EVENT} HR data - {event.data}, from user: {event.sender}")
        self.counter = self.counter+1
        current_participant = event.sender
        if event:
            # current_participant.current_training_session.metrics.hr_data.append(HrData(value=event.data,timestamp=event.timestamp))
            current_participant.current_training_session.metrics.handle_new_hr_data(HrData(value=event.data, timestamp=event.timestamp), current_participant.current_training_session.start_time, current_participant.name)
            # if self.counter==22:
                # self.counter = 0
                # print(json.dumps(current_participant.current_training_session.metrics, default=custom_serializer, indent=4))

#todo: send data to visualisation queue

    # def on_stop_event(self, event:StopSessionEvent):
    #     event.person.current_training_session.metrics.calculate_post_training_data(user_name=event.person.name)
    async def periodic_update_low_frequency(self, interval: int):
            while self.running:
                await asyncio.sleep(interval)  # Várakozás az adott időtartamig
                async with self.lock:  # SZÁLBIZTOS ZÁROLÁS ITT
                    for user in self.active_users:
                        user.current_training_session.metrics.calculate_low_frequency_data(user_name=user.name,  duration=self.current_duration,
                                                                                           age=user.age, gender=user.gender, hr_max=user.hr_max, hr_rest=user.resting_hr,
                                                                                           height=user.height, weight=user.weight)

    async def periodic_update_mid_frequency(self, interval: int):
            while self.running:
                await asyncio.sleep(interval)  # Várakozás az adott időtartamig
                async with self.lock:  # SZÁLBIZTOS ZÁROLÁS ITT
                    for user in self.active_users:
                        user.current_training_session.metrics.calculate_mid_frequency_data(user_name=user.name, gender=user.gender, resting_hr=user.resting_hr,
                                                                                           heart_rate_reserve=user.heart_rate_reserve,
                                                                                           duration=self.current_duration,
                                                                                           hr_max=user.hr_max)

    async def periodic_update_high_frequency(self, interval: int):
            while self.running:
                await asyncio.sleep(interval)  # Várakozás az adott időtartamig
                async with self.lock:  # SZÁLBIZTOS ZÁROLÁS ITT
                    for user in self.active_users:
                        user.current_training_session.metrics.calculate_high_frequency_data(user_name = user.name, hr_max=user.hr_max)

    async def update_duration(self, start_time):
        while self.running:
            now = datetime.now()
            self.current_duration = now - start_time  # Kiszámoljuk az eltelt időt
            # print(f"Current duration: {self.current_duration}")  # Kiíratás (opcionális)
            await asyncio.sleep(1)  # Várunk 1 másodpercet

    def start_trainings(self):
        for active_user in self.active_users:
            active_user.current_training_session.start_session()