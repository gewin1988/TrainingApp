# /repositories/person_repository.py

from domain.Person.person_entity import PersonEntity
from sqlalchemy.orm import Session

from domain.base.base_repository import BaseRepository


class PersonRepository(BaseRepository[PersonEntity]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, PersonEntity)


