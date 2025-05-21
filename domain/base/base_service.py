from typing import TypeVar, Generic, Sequence, Type, get_type_hints, Any, Optional
from domain.base.base_repository import BaseRepository  # Assuming a base repository exists
from configuration.symbols import SYMBOL_ERROR

T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def get_all(self) -> Sequence[T]:
        return self.repository.get_all()

    def get_by_id(self, entity_id: int) -> T | None:
        return self.repository.get_by_id(entity_id)

    def get_by_ids(self, entity_class: Type[T], entity_ids: list[int]) -> list[T] | None:
        return self.repository.get_by_ids(entity_class, entity_ids)

    def delete(self, entity_id: int) -> bool:
        return self.repository.delete(entity_id)

    def update(self, entity) -> Optional[T]:
        return self.repository.update(entity)

    def update_entity_field(self, entity_id: int, field_name: str, new_value: Any) -> T:
        """
        This can be used as a general function to update a field if i do not want to write that many functions.
        cons: it lacks the check of parameters because i do not know which field i update
        :param entity_id: entity id to update
        :param field_name: attribute to update
        :param new_value:  new value to update
        :return: none
        """
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise ValueError(f"{SYMBOL_ERROR} Entity with ID {entity_id} not found")

        if not hasattr(entity, field_name):
            raise AttributeError(f"{SYMBOL_ERROR} Field '{field_name}' does not exist in the entity {entity_id}")

        # Get the expected type of the field from the entity's type hints
        field_type = get_type_hints(type(entity)).get(field_name)
        if field_type and not isinstance(new_value, field_type):
            raise TypeError(
                f"{SYMBOL_ERROR} Expected type '{field_type}' for field '{field_name}', but got '{type(new_value)}'")

        setattr(entity, field_name, new_value)
        self.repository.update(entity)

        return entity
