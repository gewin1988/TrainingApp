from contextlib import contextmanager

from configuration.symbols import SYMBOL_INFO, SYMBOL_OK
from infrastructure.database.db_management.database import SessionLocal, Base, engine


# Globális session-kezelés
class DBSessionManager:
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is None or not cls._session.is_active:
            cls._session = SessionLocal()
        return cls._session

    @classmethod
    def close_session(cls):
        if cls._session:
            cls._session.close()
            cls._session = None


def create_tables(drop_before=False):
    # from Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity
    # from Device.device_entity import BLEHrDeviceEntity
    # from Person.person_entity import PersonEntity
    # from Training.heart_rate.hr_data_entity import HrDataEntity
    # from Training.metrics_data.training_metrics_entity import TrainingMetricsEntity
    # from Training.metrics_data.training_impulse_entity import TrainingImpulseEntity
    # from Training.person_training_session.training_session_entity import TrainingSessionEntity
    # from Training.team_training_session.team_training_session_entity import TeamTrainingSessionEntity
    # from Training.zone.zone_entity import ZoneEntity

    from domain.Device.device_entity import BLEHrDeviceEntity
    from domain.Person.person_entity import PersonEntity
    from domain.Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity


    from domain.Training.heart_rate.hr_data_entity import HrDataEntity
    from domain.Training.zone.zone_entity import ZoneEntity
    from domain.Training.training_data.metrics.training_metrics_entity import TrainingMetricsEntity
    from domain.Training.training_data.impulse.training_impulse_entity import TrainingImpulseEntity
    from domain.Training.person_training_session.training_session_entity import TrainingSessionEntity
    from domain.Training.team_training_session.team_training_session_entity import TeamTrainingSessionEntity


    assert DevicePersonConnectionEntity
    assert BLEHrDeviceEntity
    assert PersonEntity
    assert HrDataEntity
    assert TrainingSessionEntity
    assert TeamTrainingSessionEntity
    assert TrainingMetricsEntity
    assert TrainingImpulseEntity

    assert ZoneEntity

    if drop_before is True:
        print(f"{SYMBOL_INFO} Tables before drop: ")
        print(f"{SYMBOL_INFO} Tables to delete:", Base.metadata.tables.keys())
        print(f"{SYMBOL_INFO} Drop tables...")
        Base.metadata.drop_all(engine)
        print(f"✅ Drop tables done!")

    print(f"{SYMBOL_INFO} Tables before creation:", Base.metadata.tables.keys())
    print(f"{SYMBOL_INFO} Create tables...")
    Base.metadata.create_all(engine)
    print(f"{SYMBOL_OK} Tables created!")
    print(f"{SYMBOL_INFO} Tables after creation:", Base.metadata.tables.keys())


@contextmanager
def get_db():
    db = DBSessionManager.get_session()
    try:
        yield db
        db.commit()  # Ha nincs hiba, commitálunk
    except Exception as e:
        db.rollback()
        raise e
    finally:
        pass  # Nem zárjuk le a session-t azonnal, csak ha szükséges

