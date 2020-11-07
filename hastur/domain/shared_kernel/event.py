from uuid import UUID
from datetime import datetime
from typing import List
import re


class DomainEvent:
    def __init__(self, id_: UUID, created_at: datetime, version: int):
        self.id_: UUID = id_
        self.created_at: datetime = created_at
        self.version: int = version

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
