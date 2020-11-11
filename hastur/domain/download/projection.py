# pylint: disable=no-name-in-module
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from hastur.domain.shared_kernel.event import EventBus, DomainEvent
from hastur.domain.download.entity.download import (
    DownloadCreatedEvent,
    DownloadFileInfosSettedEvent,
    DownloadFileSettedOnlineEvent,
    DownloadFileSettedOfflineEvent,
)
from .entity.download import DownloadStatus


class Download(BaseModel):
    id_: UUID
    url: HttpUrl
    status: DownloadStatus
    created_at: datetime
    size: Optional[int] = None
    filename: Optional[str] = None


class DownloadProjection(ABC):
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.event_bus.add_handler(DownloadCreatedEvent, self.on_download_created)
        self.event_bus.add_handler(
            DownloadFileInfosSettedEvent, self.on_download_file_infos_setted
        )
        self.event_bus.add_handler(
            DownloadFileSettedOnlineEvent, self.on_download_status_change
        )
        self.event_bus.add_handler(
            DownloadFileSettedOfflineEvent, self.on_download_status_change
        )

    def on_download_created(self, event: DownloadCreatedEvent):
        self.add(
            Download(
                id_=event.id_,
                url=event.payload.url,
                status=event.payload.status,
                created_at=event.created_at,
            )
        )

    def on_download_file_infos_setted(self, event: DownloadFileInfosSettedEvent):
        download: Download = self.get(event.id_)
        download.size = event.payload.size
        download.filename = event.payload.filename
        self.update(download)

    def on_download_status_change(self, event: DomainEvent):
        download: Download = self.get(event.id_)
        download.status = event.payload.status
        self.update(download)

    @abstractmethod
    def add(self, download: Download):
        pass

    @abstractmethod
    def list(self) -> List[Download]:
        pass

    @abstractmethod
    def get(self, id_: UUID) -> Download:
        pass

    @abstractmethod
    def update(self, download: Download):
        pass


class ProjectionFactory(ABC):
    @abstractmethod
    def create_download_projection(self) -> DownloadProjection:
        pass
