# pylint: disable=no-name-in-module
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from typing import List
from pydantic import BaseModel, HttpUrl
from hastur.domain.shared_kernel.event import EventBus
from hastur.domain.download.entity.download import DownloadCreatedEvent
from .entity.download import DownloadStatus


class Download(BaseModel):
    id_: UUID
    url: HttpUrl
    status: DownloadStatus
    created_at: datetime


class DownloadProjection(ABC):
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.event_bus.add_handler(DownloadCreatedEvent, self.on_download_created)

    def on_download_created(self, event: DownloadCreatedEvent):
        self.add(
            Download(
                id_=event.id_,
                url=event.payload.url,
                status=event.payload.status,
                created_at=event.created_at,
            )
        )

    @abstractmethod
    def add(self, download: Download):
        pass

    @abstractmethod
    def list(self) -> List[Download]:
        pass
