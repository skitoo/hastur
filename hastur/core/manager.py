from uuid import UUID
from typing import Type, NoReturn
from .entity import Aggregate, AggregateCollection
from .store import EventStore
from .event import EventBus


class AggregateManager:
    def __init__(self, store: EventStore, bus: EventBus):
        self.store: EventStore = store
        self.bus: EventBus = bus

    def load(self, id_: UUID, aggregate_type: Type[Aggregate]) -> Aggregate:
        stream = self.store.load_stream(id_, aggregate_type)
        return aggregate_type(id_, stream=stream)

    def save_and_dispatch(self, aggregates: AggregateCollection) -> NoReturn:
        self.store.save(aggregates)
        self.bus.dispatch(
            [event for aggregate in aggregates for event in aggregate.new_events]
        )
