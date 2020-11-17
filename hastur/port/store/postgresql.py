from uuid import UUID
from typing import Type, NoReturn
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import text
from hastur.core.store import EventStore
from hastur.core.helper import fullname, class_
from hastur.core.entity import Aggregate, AggregateCollection
from hastur.core.event import EventStream


class PgEventStore(EventStore):
    def __init__(self, connection: Connection):
        self.connection: Connection = connection
        self.__create_table()

    def __create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS event (
            id SERIAL PRIMARY KEY,
            type VARCHAR(255) NOT NULL,
            aggregate_id UUID NOT NULL,
            aggregate_type VARCHAR(255) NOT NULL,
            version INT NOT NULL,
            payload JSON,
            created_at TIMESTAMP NOT NULL,
            UNIQUE(aggregate_id, aggregate_type, version)
        );
        """
        self.connection.execute(query)

    def save(self, aggregates: AggregateCollection) -> NoReturn:
        query = """
        INSERT INTO event(type, aggregate_id, aggregate_type, version, payload, created_at)
        VALUES(:type, :aggregate_id, :aggregate_type, :version, :payload, :created_at)
        """
        values = []
        for aggregate in aggregates:
            for event in aggregate.new_events:
                value = {
                    "type": fullname(event),
                    "aggregate_id": aggregate.get_id(),
                    "aggregate_type": fullname(aggregate),
                    "version": event.version,
                    "payload": event.payload.json() if event.payload else None,
                    "created_at": event.created_at,
                }
                values.append(value)
        self.connection.execute(text(query), values)

    def load_stream(self, id_: UUID, aggregate_type: Type[Aggregate]) -> EventStream:
        query = """
        SELECT type, aggregate_id, created_at, version, payload
        FROM event
        WHERE aggregate_id = :id
        ORDER BY version
        """
        res = self.connection.execute(text(query), id=id_)
        result = []
        for row in res.fetchall():
            event_type = class_(row[0])
            result.append(
                event_type(
                    row[1],
                    row[2],
                    row[3],
                    event_type.Payload(**row[4]) if row[4] else None,
                )
            )
        return result
