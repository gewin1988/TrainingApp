from typing import Optional, Dict, Any

from sqlalchemy import Column

from domain.Device.device_management.device_person_connection_entity import DevicePersonConnectionEntity
from domain.Device.device_management.device_person_connection_repository import DevicePersonConnectionRepository
from domain.Person.person_model import PersonModel
from domain.Person.person_repository import PersonRepository
from domain.base.base_service import BaseService
from configuration.symbols import SYMBOL_WARNING, SYMBOL_ERROR

class InMemoryDevicePersonConnectionService:
    _instance = None  # Az egyetlen példányt tároljuk itt

    def __new__(cls, *args, **kwargs):
        # Ha még nincs példány, létrehozzuk
        if not cls._instance:
            cls._instance = super(InMemoryDevicePersonConnectionService, cls).__new__(cls, *args, **kwargs)
            cls._instance.cache = {}  # Inicializáljuk a cache-t
        return cls._instance

    # def __init__(self):
    #     self.cache = {}

    def assign_owner(self, device_mac, owner_id):
        # if not self._is_valid_mac(device_mac):
        #     raise ValueError("Invalid MAC address.")
        if owner_id is None or device_mac is None:
            raise ValueError(f"{SYMBOL_ERROR} Person or mac is None.")
        self.cache[device_mac] = owner_id
        print(f"cache updated with pair: {device_mac} - {owner_id}")

    def deassign_owner(self, device_mac):
        """Eltávolítja az eszköz és személy kapcsolatát az adatbázisból és a cache-ből."""
        if device_mac not in self.cache:
            raise ValueError(f"{SYMBOL_WARNING} Couldn't remove from cache. Device is not assigned to any person. ")

        del self.cache[device_mac]

    def get_owner_by_device_id_from_cache(self, device_mac:str)->Optional[PersonModel]:
        if device_mac not in self.cache:
            print(f"{SYMBOL_WARNING} Couldn't get from cache. Device ({device_mac}) is not assigned to any person. ")
            return None
        return self.cache[device_mac]



class DevicePersonConnectionService(BaseService[DevicePersonConnectionEntity]):
    def __init__(self, repository: DevicePersonConnectionRepository, person_repository:PersonRepository):
        super().__init__(repository)
        self.person_repository=person_repository
        self.cache=self.load_cache()


    def load_cache(self):
        current_connections = self.repository.get_all()
        current_cache = {connection.device_mac: connection.owner_id for connection in current_connections}
        return current_cache


    def assign_owner(self, device_mac, owner_id):
        # if not self._is_valid_mac(device_mac):
        #     raise ValueError("Invalid MAC address.")
        if not self.person_repository.get_by_id(owner_id):
            raise ValueError(f"{SYMBOL_ERROR} Person does not exist.")

        new_device_person_connection_entity = DevicePersonConnectionEntity(device_mac=device_mac, owner_id=owner_id)
        self.repository.create(new_device_person_connection_entity)
        self.cache[device_mac] = owner_id

    def deassign_owner(self, device_mac):
        """Eltávolítja az eszköz és személy kapcsolatát az adatbázisból és a cache-ből."""
        if device_mac not in self.cache:
            raise ValueError(f"{SYMBOL_WARNING} Couldn't remove from cache. Device is not assigned to any person. ")

        self.repository.delete(device_mac)  # Adatbázisból törlés
        del self.cache[device_mac]  # Cache frissítése

    def get_all_connection_from_cache(self)-> dict[Any, Any]:
        return self.cache

    def get_owner_by_device_id_from_cache(self, device_mac:str)->Optional[int]:
        if device_mac not in self.cache:
            print(f"{SYMBOL_WARNING} Couldn't get cache. Device ({device_mac}) is not assigned to any person. ")
            return None
        return self.cache[device_mac]
