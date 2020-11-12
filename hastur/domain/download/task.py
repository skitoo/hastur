from abc import ABC, abstractmethod
from logging import getLogger, Logger
from hastur.core.event import EventBus
from hastur.core.message import CommandBus
from hastur.domain.download.entity.download import DownloadCreatedEvent


class Downloader(ABC):
    def __init__(self, event_bus: EventBus, command_bus: CommandBus):
        self.event_bus: EventBus = event_bus
        self.command_bus: CommandBus = command_bus
        self.logger: Logger = getLogger(str(type(self)))
        self.event_bus.add_handler(DownloadCreatedEvent, self.on_download_created)

    @abstractmethod
    def on_download_created(self, event: DownloadCreatedEvent):
        pass
