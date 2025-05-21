from typing import Type, TypeVar, Generic, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from configuration.symbols import SYMBOL_WARNING, SYMBOL_ERROR

# Define a generic type variable
T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, entity: Type[T]):
        self.db = session
        self.entity = entity  # Store the entity type

    def get_all(self) -> list[T]:
        """Fetch all records of the given entity type."""
        return self.db.query(self.entity).all()

    def get_by_id(self, entity_id: int) -> T | None:
        """Fetch a record by ID."""
        return self.db.query(self.entity).filter_by(id=entity_id).first()

    def get_by_ids(self, entity_class: Type[T], entity_ids: list[int]) -> list[T]:
        return self.db.query(entity_class).filter(entity_class.id.in_(entity_ids)).all()

    def create(self, entity_obj: T) -> T:
        """Add a new record."""
        try:
            self.db.add(entity_obj)
            self.db.commit()
            self.db.refresh(entity_obj)
            return entity_obj
        except IntegrityError as ie:
            self.db.rollback()
            error_msg = str(ie.orig)  # Az eredeti DB hibaüzenet
            if "UNIQUE constraint failed" in error_msg or "Duplicate entry" in error_msg:
                print(f"{SYMBOL_WARNING} Warning: Duplicate record detected, not inserting: {entity_obj}")
            else:
                print(f"{SYMBOL_ERROR} Database record creation failed for: {entity_obj}, error: {ie}")
                 # Ha nem duplikáció, akkor dobjuk tovább a hibát
        except Exception as e:
            self.db.rollback()
            raise e

    def create_bulk(self, entity_list: Sequence[T])  -> Sequence[T]:
        """Insert multiple entities in bulk and return them."""
        try:
            self.db.add_all(entity_list)
            self.db.commit()

            # Refresh each entity to ensure the database-assigned IDs are available
            for entity in entity_list:
                self.db.refresh(entity)

            return entity_list

        except Exception as e:
            self.db.rollback()
            raise e  # Re-raise the exception for better debugging

    def update(self, entity_obj: T) -> T:
        """Update an existing record."""
        try:
            merged_entity = self.db.merge(entity_obj)  # A merge metódus frissíti a meglévő entitást
            self.db.commit()
            self.db.refresh(merged_entity)
            return entity_obj
        except IntegrityError as ie:
            self.db.rollback()
            error_msg = str(ie.orig)  # Az eredeti DB hibaüzenet
            if "UNIQUE constraint failed" in error_msg or "Duplicate entry" in error_msg:
                print(f"{SYMBOL_WARNING} Warning: Duplicate record detected, not updating: {entity_obj}")
            else:
                print(f"{SYMBOL_ERROR} Database record update failed for: {entity_obj}, error: {ie}")
            # Ha nem duplikáció, akkor dobjuk tovább a hibát
            raise ie
        except Exception as e:
            self.db.rollback()
            print(f"{SYMBOL_ERROR} Unexpected error during update: {e}")
            raise e

    def save(self, entity: T) -> T:
        if entity.id is None:  # Ha új entitás, akkor hozzáadjuk
            try:
                self.db.add(entity)
            except Exception as e:
                self.db.rollback()
                raise e

        else:
            try:
                self.db.merge(entity)  # Ha már létezik, frissítjük
            except Exception as e:
                self.db.rollback()
                raise e

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        """Delete a record by ID."""
        obj = self.get_by_id(entity_id)
        if obj:
            try:
                self.db.delete(obj)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                raise e
        return False
