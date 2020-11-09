from typing import Dict, List, NoReturn
from hastur.domain.shared_kernel.error import HasturError
from hastur.domain.shared_kernel.event import (
    EventBus,
    EventHandler,
    EventType,
    EventStream,
)


class EventBusError(HasturError):
    pass


class LocalEventBus(EventBus):
    def __init__(self):
        self.handlers: Dict[EventType, List[EventHandler]] = {}

    def add_handler(self, event_type: EventType, handler: EventHandler) -> NoReturn:
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        if handler in self.handlers[event_type]:
            raise EventBusError(
                f"Handler '{handler}' already registered for {event_type.__name__}"
            )
        self.handlers[event_type].append(handler)

    def dispatch(self, stream: EventStream) -> NoReturn:
        for event in stream:
            print(type(event))
            print(self.handlers)
            handlers = self.handlers.get(type(event), [])
            print(handlers)
            for handler in handlers:
                handler(event)
