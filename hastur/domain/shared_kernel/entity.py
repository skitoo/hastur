from abc import ABC
from uuid import UUID
from .event import EventStream, DomainEvent
from .error import HasturError


class AggregateError(HasturError):
    pass


class HandlerNotFoundError(AggregateError):
    def __init__(self, handler: str, aggregate: "Aggregate"):
        name = aggregate.__class__.__name__
        super().__init__(f"Handle '{handler}' not found on '{name}' aggregate")


class EventVersionError(AggregateError):
    def __init__(self, event: DomainEvent, aggregate: "Aggregate"):
        e_version = event.version
        a_version = aggregate.next_version
        name = aggregate.__class__.__name__
        super().__init__(
            f"Event version '{e_version}' does not match expected version '{a_version}' of '{name}'"
        )


class Aggregate(ABC):
    def __init__(self, id_: UUID, stream: EventStream = None, init_payload=None):
        self.__id: UUID = id_
        self.__stream: EventStream = stream or []
        self.__version: int = 0
        self.__new_events: EventStream = []
        self.__replay_events()
        self.post_init(init_payload)

    def post_init(self, payload):
        pass

    def __replay_events(self):
        for event in self.__stream:
            self.__apply(event)
            self.__version = event.version

    def __apply(self, event: DomainEvent):
        handler = event.handler_name
        if hasattr(self, handler) and callable(getattr(self, handler)):
            getattr(self, handler)(event)
        else:
            raise HandlerNotFoundError(handler, self)

    def apply_new_event(self, event: DomainEvent):
        if event.version != self.next_version:
            raise EventVersionError(event, self)
        self.__apply(event)
        self.__new_events.append(event)

    def get_id(self):
        return self.__id

    @property
    def new_events(self) -> EventStream:
        return self.__new_events.copy()

    @property
    def stream(self) -> EventStream:
        return self.__stream.copy()

    @property
    def next_version(self) -> int:
        return self.__version + len(self.__new_events) + 1

    @property
    def base_version(self) -> int:
        return self.__version
