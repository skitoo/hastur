from unittest.mock import Mock
from uuid import uuid4, UUID
from datetime import datetime
from hastur.port.event import LocalEventBus
from .entity.download import (
    DownloadCreatedEvent,
    DownloadFileInfosSettedEvent,
    DownloadFileSettedOfflineEvent,
    DownloadFileSettedOnlineEvent,
    DownloadStatus,
)
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


def test_download_projection_on_download_file_infos_setted():
    id_ = uuid4()
    bus = LocalEventBus()
    event = DownloadFileInfosSettedEvent(
        id_,
        datetime.now(),
        1,
        DownloadFileInfosSettedEvent.Payload(size=1000, filename="foo.avi"),
    )
    download = Mock()
    projection = LocalProjection(bus)
    projection.get = Mock(return_value=download)
    projection.update = Mock()
    bus.dispatch([event])

    projection.get.assert_called_once_with(id_)
    assert download.size == 1000
    assert download.filename == "foo.avi"
    projection.update.assert_called_once_with(download)


def test_download_projection_on_download_setted_online():
    id_ = uuid4()
    bus = LocalEventBus()
    event = DownloadFileSettedOnlineEvent(
        id_,
        datetime.now(),
        1,
        DownloadFileSettedOnlineEvent.Payload(status=DownloadStatus.ONLINE),
    )
    download = Mock()
    projection = LocalProjection(bus)
    projection.get = Mock(return_value=download)
    projection.update = Mock()
    bus.dispatch([event])

    projection.get.assert_called_once_with(id_)
    assert download.status == DownloadStatus.ONLINE
    projection.update.assert_called_once_with(download)


def test_download_projection_on_download_setted_offline():
    id_ = uuid4()
    bus = LocalEventBus()
    event = DownloadFileSettedOfflineEvent(
        id_,
        datetime.now(),
        1,
        DownloadFileSettedOfflineEvent.Payload(status=DownloadStatus.OFFLINE),
    )
    download = Mock()
    projection = LocalProjection(bus)
    projection.get = Mock(return_value=download)
    projection.update = Mock()
    bus.dispatch([event])

    projection.get.assert_called_once_with(id_)
    assert download.status == DownloadStatus.OFFLINE
    projection.update.assert_called_once_with(download)
