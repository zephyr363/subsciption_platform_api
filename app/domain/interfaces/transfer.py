from abc import ABC, abstractmethod
from typing import Any


class IDomainObjectsTransfer(ABC):
    @abstractmethod
    def to_entity(self):
        pass

    @abstractmethod
    def from_entity(self, entity: Any):
        pass
