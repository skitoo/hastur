from sqlalchemy import create_engine
from hastur.port.store.postgresql import PgEventStore
from hastur.port.locker import InMemoryLocker
from hastur.port.projection import InMemoryProjectionFactory
from hastur.port.event import LocalEventBus
from hastur.port.task import AsyncDownloader
from hastur.app import Application


database = create_engine("postgresql://hastur:hastur@localhost:5432/hastur")

event_store = PgEventStore(database.connect())
event_bus = LocalEventBus()

application = Application(
    event_store,
    event_bus,
    InMemoryLocker(),
    InMemoryProjectionFactory(event_bus),
)
AsyncDownloader(event_bus, application.command_bus)
