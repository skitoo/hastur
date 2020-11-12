from hastur.port.store import InMemoryEventStore
from hastur.port.locker import InMemoryLocker
from hastur.port.projection import InMemoryProjectionFactory
from hastur.port.event import LocalEventBus
from hastur.port.task import AsyncDownloader
from hastur.app import Application

event_bus = LocalEventBus()
application = Application(
    InMemoryEventStore(),
    event_bus,
    InMemoryLocker(),
    InMemoryProjectionFactory(event_bus),
)
AsyncDownloader(event_bus, application.command_bus)
