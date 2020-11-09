from uuid import UUID
from typing import Dict, Type, NoReturn
from hastur.domain.shared_kernel.store import (
    EventStore,
    StreamNotFoundError,
    BaseVersionNotMatchError,
)
from hastur.domain.shared_kernel.entity import Aggregate, AggregateCollection
from hastur.domain.shared_kernel.event import EventStream


class InMemoryEventStore(EventStore):
    def __init__(self):
        self.events: Dict[str, EventStream] = {}

    def __check_version(self, aggregate: Aggregate):
        current_stream = self.events.get(aggregate.index, [])

        if (
            len(current_stream) > 0
            and current_stream[-1].version != aggregate.base_version
        ):
            raise BaseVersionNotMatchError(
                aggregate.get_id(), current_stream[-1].version, aggregate.base_version
            )

    def __save(self, aggregate: Aggregate):
        current_stream = self.events.get(aggregate.index, [])
        self.events[aggregate.index] = current_stream + aggregate.new_events

    def save(self, aggregates: AggregateCollection) -> NoReturn:
        for aggregate in aggregates:
            self.__check_version(aggregate)
        for aggregate in aggregates:
            self.__save(aggregate)

    def load_stream(self, id_: UUID, aggregate_type: Type[Aggregate]) -> EventStream:
        index = f"{aggregate_type.__name__}:{id_}"
        if index in self.events:
            return self.events[index]
        raise StreamNotFoundError(id_)
