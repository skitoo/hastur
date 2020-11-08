from uuid import UUID
from typing import Dict
from hastur.domain.shared_kernel.store import (
    EventStore,
    StreamNotFoundError,
    BaseVersionNotMatchError,
)
from hastur.domain.shared_kernel.entity import Aggregate
from hastur.domain.shared_kernel.event import EventStream


class InMemoryEventStore(EventStore):
    def __init__(self):
        self.events: Dict[UUID, EventStream] = {}

    def save(self, aggregate: Aggregate):
        id_, new_events, base_version = (
            aggregate.get_id(),
            aggregate.new_events,
            aggregate.base_version,
        )
        current_stream = self.events[id_] if id_ in self.events else []

        if len(current_stream) > 0 and current_stream[-1].version != base_version:
            raise BaseVersionNotMatchError(
                id_, current_stream[-1].version, base_version
            )

        self.events[id_] = current_stream + new_events

    def load_stream(self, id_: UUID) -> EventStream:
        if id_ in self.events:
            return self.events[id_]
        raise StreamNotFoundError(id_)
