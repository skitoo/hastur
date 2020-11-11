from uuid import uuid4, UUID
from datetime import datetime
from hastur.port.event import LocalEventBus
from .entity.download import DownloadCreatedEvent, DownloadStatus
from .projection import DownloadProjection, Download


class LocalProjection(DownloadProjection):
    download: Download

    def add(self, download: Download):
        self.download = download

    def list(self):
        return

    def get(self, id_: UUID) -> Download:
        return

    def update(self, download: Download):
        pass


def test_download_projection_on_created_event():
    bus = LocalEventBus()
    event = DownloadCreatedEvent(
        uuid4(),
        datetime.now(),
        1,
        DownloadCreatedEvent.Payload(url="http://foo.com", status=DownloadStatus.NEW),
    )
    projection = LocalProjection(bus)
    bus.dispatch([event])

    assert projection.download == Download(
        id_=event.id_,
        created_at=event.created_at,
        status=DownloadStatus.NEW,
        url="http://foo.com",
    )
