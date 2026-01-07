from abc import ABC, abstractmethod
from typing import Generic, TypeVar

OrmT = TypeVar("OrmT")
DomainT = TypeVar("DomainT")


class BaseSQLAMapping(ABC, Generic[OrmT, DomainT]):

    @staticmethod
    @abstractmethod
    def from_orm(
        orm_obj: OrmT,
    ) -> DomainT: ...

    @staticmethod
    @abstractmethod
    def to_orm(
        entity: DomainT,
    ) -> OrmT: ...
