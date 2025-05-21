import asyncio
import json
import threading
import time
from datetime import datetime

import keyboard
from sqlalchemy.orm import configure_mappers

from configuration.symbols import SYMBOL_TIME, SYMBOL_EVENT
from domain.Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity
from domain.Device.device_management.device_person_connection_mapper import DevicePersonConnectionMapper
from domain.Device.device_management.device_person_connection_model import DevicePersonConnectionModel
from domain.Device.device_management.device_person_connection_repository import DevicePersonConnectionRepository
from domain.Device.device_management.device_person_connection_service import InMemoryDevicePersonConnectionService, \
    DevicePersonConnectionService
from domain.Device.device_mapper import DeviceMapper
from domain.Device.device_model import BLEHrDeviceModel
from domain.Device.device_repository import DeviceRepository
from domain.Device.device_service import DeviceService
from domain.Person.person_mapper import PersonMapper
from domain.Person.person_model import PersonModel
from domain.Person.person_repository import PersonRepository
from domain.Person.person_service import PersonService
from domain.Training.person_training_session.training_session_model import TrainingSessionModel
from domain.Training.team_training_session.team_training_session_model import TeamTrainingSessionModel
from domain.Training.training_data.impulse.training_impulse_repository import TrainingImpulseRepository
from domain.Training.training_data.metrics.training_metrics_mapper import TrainingMetricsMapper
from domain.Training.training_data.metrics.training_metrics_model import TrainingMetricsModel
from domain.Training.training_data.metrics.training_metrics_repository import TrainingMetricsRepository
from domain.Training.training_data.metrics.training_metrics_service import TrainingMetricsService
from domain.Training.zone.zone_mapper import ZoneMapper
from domain.Training.zone.zone_repository import ZoneRepository
from domain.Training.zone.zone_service import ZoneService
# from domain.in_memory_rt_data.in_memory_data_service import InMemoryRealTimeDataService
from domain.real_time_session_manager.real_time_session_manager import RealTimeSessionManager
from infrastructure.database.db_management.db_manager import create_tables, get_db
from infrastructure.hr_sensor_handler.hr_sensor_service import HrSensorService

from shared.event_handler import EventHandler

from pynput import keyboard

def on_press(key, event_obj):
    """
    Billentyű lenyomás esemény kezelése.
    """
    try:
        if key.char == 's':  # Ha az 's' betűt nyomták le
            print("Az 's' betűt lenyomták! Meghívom a callback függvényt.")
            my_callback(event_obj)
    except AttributeError:
        pass  # Nem alfanumerikus billentyű (pl. shift, ctrl)

def my_callback(event_obj):
    """
    Példa callback függvény.
    """
    print("Callback függvény meghívva!")

def start_keyboard_listener(my_class_instance):
    """
    Billentyűzet figyelő indítása egy külön szálon.
    """
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()  # Ez blokkolja a szálat, de nem a főprogramot



async def start_team_training_session(personlist :list[PersonModel], location:str):
    hr_event_handler = EventHandler()

    with(get_db()) as db:
        met_repo = TrainingMetricsRepository(db)
        zone_repo = ZoneRepository(db)
        impulse_repo = TrainingImpulseRepository(db)
        met_serv = TrainingMetricsService(met_repo, zone_repository=zone_repo,training_impulse_repository=impulse_repo)
        zone_serv = ZoneService(zone_repo)
        team_training1 = TeamTrainingSessionModel(name="FC", place=location, date=datetime.today())

        for person in personlist:
            zone_entity_list = zone_serv.create_5_zones(person.hr_max)
            zone_dto_list = ZoneMapper.entity_list_to_dto_list(zone_entity_list)
            metric_entity  = met_serv.create(intensity_zones=zone_entity_list)
            metric_model = TrainingMetricsModel(TrainingMetricsMapper.entity_to_dto(metric_entity), zone_dto_list)
            person.assign_session(TrainingSessionModel(name="Session"+person.name+"_1", location=location, metrics = metric_model))
            team_training1.add_participant(person)

        # team_training1.init_team_training()
        #  team_training1.start_team_training()
        rt_session_manager = RealTimeSessionManager(team_training1, hr_event_handler=hr_event_handler)
        # print(json.dumps(rt_session_manager, default=custom_serializer, indent=4))

        hr_sensor_service = HrSensorService(hr_event_handler=hr_event_handler)
        for device in device_connection_service.cache:
            hr_sensor_service.register_device(device, hr_sensor_service.process_hr_data)

        # print(json.dumps(hr_sensor_service, default=custom_serializer, indent=4))
        # team_training1.start_team_training()

        # team_training1.start_team_training()
        # await hr_sensor_service.start_all_simulations()
        rt_session_manager.start_trainings()
        print(f"{SYMBOL_TIME} Start trainings at: {datetime.now()}")
        await hr_sensor_service.start_all_simulations()
        print(f"{SYMBOL_TIME} Training session ended at: {datetime.now()}!")
        await hr_sensor_service.stop_all_simulations()
        team_training1.stop_team_training()

device_connection_service = InMemoryDevicePersonConnectionService()

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)

async def main():
    # configure_mappers()
    create_tables(True)
    with (get_db() as db):
        device_repository = DeviceRepository(db)
        device_service = DeviceService(device_repository)
        # ---------------------
        device_gw = device_service.create(mac_address="A4:5E:60:3B:7F:C2", brand="Garmin", type="watch")
        device_pw = device_service.create(mac_address="00:1D:92:8A:4F:11", brand="Polar", type="watch")
        device_ds = device_service.create(mac_address="3C:52:82:9D:E0:5B", brand="Dechatlon", type="chest strap")
        # ---------------------
        person_repository = PersonRepository(db)
        person_service = PersonService(person_repository)
        #---------------------
        person1 = person_service.create(name="Adam Forgo", gender="male", age=36, weight=104, height=200,
                                       fitness_level="moderately_trained", resting_hr=60, max_hr_calculation_algorythm="simple")
        person2 = person_service.create(name="Teszt Elek", gender="male", age=26, weight=66, height=172,
                fitness_level="moderately_trained", resting_hr=60, max_hr_calculation_algorythm="simple")
        person3 = person_service.create(name="Juli Anna", gender="female", age=31, weight=44, height=160,
                fitness_level="moderately_trained", resting_hr=60, max_hr_calculation_algorythm="simple")
        # ---------------------

        device_gw = BLEHrDeviceModel(DeviceMapper.entity_to_dto(device_service.get_by_id(1)))
        device_pw = BLEHrDeviceModel(DeviceMapper.entity_to_dto(device_service.get_by_id(2)))
        device_ds = BLEHrDeviceModel(DeviceMapper.entity_to_dto(device_service.get_by_id(3)))

        device_ds.type="modified type"
        device_ds.brand="modified brand"
        device_service.update(DeviceMapper.dto_to_entity(device_ds.to_dto()))
        device_ds = BLEHrDeviceModel(DeviceMapper.entity_to_dto(device_service.get_by_id(3)))
        print(f"------------------- after mod: {device_ds}")

        person1 = PersonModel(PersonMapper.entity_to_dto(person_service.get_by_id(1)))
        person2 = PersonModel(PersonMapper.entity_to_dto(person_service.get_by_id(2)))
        person3 = PersonModel(PersonMapper.entity_to_dto(person_service.get_by_id(3)))

        device_person_connection_repository = DevicePersonConnectionRepository(db)
        device_person_connection_service = DevicePersonConnectionService(device_person_connection_repository, person_repository)
        device_person_connection_service.assign_owner(device_gw.mac_address, person1.id)
        device_person_connection_service.assign_owner(device_pw.mac_address, person2.id)
        device_person_connection_service.assign_owner(device_ds.mac_address, person3.id)

        device_person_conn = device_person_connection_service.get_all_connection_from_cache()

        connections = []

        for device_mac, owner_id in device_person_conn.items():
            device_person_conn_entity = DevicePersonConnectionEntity(device_mac=device_mac, owner_id=owner_id)

            # Átalakítjuk modellé
            dev_pers_conn_model = DevicePersonConnectionModel(DevicePersonConnectionMapper.entity_to_dto(device_person_conn_entity))
            connections.append(dev_pers_conn_model)
            print(f"model address = {dev_pers_conn_model.device_mac} and owner id = {dev_pers_conn_model.owner_id}")

    for connection in connections:
        device_connection_service.assign_owner(connection.device_mac,owner_id=connection.owner_id)

    participants = []

    for participant_entity in person_service.get_all():
        participant_model = PersonModel(PersonMapper.entity_to_dto(participant_entity))
        print(participant_model)



    await start_team_training_session([person1, person2, person3], "Szabadtér")

    return

    new_device_gw = BLEHrDeviceModel(mac_address="A4:5E:60:3B:7F:C2", brand="Garmin", type="watch")
    new_device_pw = BLEHrDeviceModel(mac_address="00:1D:92:8A:4F:11", brand="Polar", type="watch")
    new_device_ds = BLEHrDeviceModel(mac_address="3C:52:82:9D:E0:5B", brand="Dechatlon", type="chest strap")

    new_person = PersonModel(name="Adam Forgo", gender="male", age=36, weight=104, height=200,
                                       fitness_level="moderately_trained", resting_hr=60, max_hr_optimization=True,
                             max_hr_calculation_algorythm="simple")
    new_person2 = PersonModel(name="Teszt Elek", gender="male", age=26, weight=66, height=172,
                             fitness_level="moderately_trained", resting_hr=60, max_hr_optimization=True,
                             max_hr_calculation_algorythm="simple")
    new_person3 = PersonModel(name="Juli Anna", gender="female", age=31, weight=44, height=160,
                             fitness_level="moderately_trained", resting_hr=60, max_hr_optimization=True,
                             max_hr_calculation_algorythm="simple")






    device_person_connection1 = DevicePersonConnectionModel(device_mac=new_device_gw.mac_address, owner=new_person)
    device_person_connection2 = DevicePersonConnectionModel(device_mac=new_device_pw.mac_address, owner=new_person2)
    device_person_connection3 = DevicePersonConnectionModel(device_mac=new_device_ds.mac_address, owner=new_person3)
    device_person_connections = [
        device_person_connection1,
        device_person_connection2,
        device_person_connection3
    ]

    for connection in device_person_connections:
        device_connection_service.assign_owner(connection.device_mac,owner=connection.owner)

    await start_team_training_session([new_person,new_person2,new_person3], "Szabadtér")




# Run the event loop
asyncio.run(main())