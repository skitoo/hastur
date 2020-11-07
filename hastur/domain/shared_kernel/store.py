from abc import ABC, abstractmethod
from uuid import UUID
from .entity import Aggregate
from .event import EventStream


class EventStoreError(Exception):
    pass


class StreamNotFoundError(EventStoreError):
    def __init__(self, id_: UUID):
        super().__init__(f"Aggregate with id '{id_}' was not found")


class BaseVersionNotMatchError(EventStoreError):
    def __init__(self, id_: UUID, current_version: int, base_version: int):
        super().__init__(
            f"Base version '{base_version}' for aggregate '{id_}' does not match \
            current stored version '{current_version}'"
        )


class EventStore(ABC):
    @abstractmethod
    def save(self, aggregate: Aggregate):
        pass

    @abstractmethod
    def load_stream(self, id_: UUID) -> EventStream:
        pass
