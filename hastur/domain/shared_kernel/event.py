# pylint: disable=no-name-in-module
from uuid import UUID
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, NoReturn, Callable, Type
import re
from pydantic import BaseModel
from .error import HasturError


class EventError(HasturError):
    def __init__(self, event: "DomainEvent"):
        name = event.__class__.__name__
        type_ = type(event.payload)
        super().__init__(
            f"{name} waiting its own Payload (a <class: dataclass>) as parameter. Received: {type_}"
        )


class DomainEvent:
    class Payload(BaseModel):
        pass

    def __init__(self, id_: UUID, created_at: datetime, version: int, payload=None):
        self.id_: UUID = id_
        self.created_at: datetime = created_at
        self.version: int = version
        self.payload = payload
        if payload and (
            not isinstance(payload, BaseModel)
            or not isinstance(payload, self.__class__.Payload)
        ):
            raise EventError(self)

    def __str__(self):
        name = self.__class__.__name__
        return f"<{name} id: {self.id_} created_at: {self.created_at} version: {self.version}>"

    def __repr__(self):
        return str(self)

    @property
    def handler_name(self) -> str:
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()
        if name.endswith("_event"):
            name = name[: -len("_event")]
        return f"on_{name}"


EventStream = List[DomainEvent]
EventType = Type[DomainEvent]
EventHandler = Callable[[DomainEvent], NoReturn]


class EventBusError(HasturError):
    pass


class EventBus(ABC):
    @abstractmethod
    def add_handler(self, event_type: EventType, handler: EventHandler) -> NoReturn:
        pass

    @abstractmethod
    def dispatch(self, stream: EventStream) -> NoReturn:
        pass
