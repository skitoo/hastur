from uuid import UUID
from typing import Dict, List
from hastur.domain.shared_kernel.event import EventBus
from hastur.domain.download.projection import DownloadProjection, Download


class InMemoryDownloadProjection(DownloadProjection):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.downloads: Dict[UUID, List[Download]] = {}

    def add(self, download: Download):
        self.downloads[download.id_] = download

    def list(self) -> List[Download]:
        return list(self.downloads.values())

    def get(self, id_: UUID) -> Download:
        return self.downloads[id_]