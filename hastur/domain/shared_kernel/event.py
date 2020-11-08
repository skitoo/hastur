from uuid import UUID
from dataclasses import dataclass, is_dataclass
from datetime import datetime
from typing import List
import re


class EventError(Exception):
    def __init__(self, event: "DomainEvent"):
        name = event.__class__.__name__
        type_ = type(event.payload)
        super().__init__(
            f"{name} waiting its own Payload (a <class: dataclass>) as parameter. Received: {type_}"
        )


class DomainEvent:
    @dataclass
    class Payload:
        pass

    def __init__(self, id_: UUID, created_at: datetime, version: int, payload=None):
        self.id_: UUID = id_
        self.created_at: datetime = created_at
        self.version: int = version
        self.payload = payload
        if payload is not None and (
            not is_dataclass(payload) or not isinstance(payload, self.__class__.Payload)
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
