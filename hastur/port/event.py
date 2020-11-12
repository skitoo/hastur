from typing import Dict, List, NoReturn
from hastur.core.event import (
    EventBus,
    EventBusError,
    EventHandler,
    EventType,
    EventStream,
)


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
            types = type(event).__bases__ + (type(event),)
            for type_ in types:
                handlers = self.handlers.get(type_, [])
                for handler in handlers:
                    handler(event)
