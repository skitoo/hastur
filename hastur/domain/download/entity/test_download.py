from uuid import uuid4
from datetime import datetime
import pytest
from .download import (
    Download,
    DownloadStatus,
    DownloadError,
    DownloadCreatedEvent,
    DownloadFileInfosSettedEvent,
)


now = datetime.now
URL = "http://foo.com"
status = DownloadStatus.NEW


def test_download_post_init_with_payload_and_without_stream():
    download = Download(
        uuid4(), init_payload=DownloadCreatedEvent.Payload(url=URL, status=status)
    )
    assert len(download.new_events) == 1
    assert isinstance(download.new_events[0], DownloadCreatedEvent)
    assert download.url == URL
    assert download.status == DownloadStatus.NEW


def test_download_post_init_without_payload_and_without_stream():
    with pytest.raises(DownloadError):
        Download(uuid4())


def test_download_post_init_without_payload_and_with_stream():
    id_ = uuid4()
    download = Download(
        id_,
        [
            DownloadCreatedEvent(
                id_, now(), 1, DownloadCreatedEvent.Payload(url=URL, status=status)
            )
        ],
    )
    assert len(download.new_events) == 0
    assert download.url == URL
    assert download.status == DownloadStatus.NEW


def test_download_post_init_with_payload_and_with_stream():
    with pytest.raises(DownloadError):
        id_ = uuid4()
        Download(
            id_,
            [
                DownloadCreatedEvent(
                    id_, now(), 1, DownloadCreatedEvent.Payload(url=URL, status=status)
                )
            ],
            DownloadCreatedEvent.Payload(url=URL, status=status),
        )


def test_download_set_infos():
    id_ = uuid4()
    download = Download(
        id_,
        [
            DownloadCreatedEvent(
                id_, now(), 1, DownloadCreatedEvent.Payload(url=URL, status=status)
            )
        ],
    )
    download.set_infos(1000, "foo.avi")
    assert download.size == 1000
    assert download.filename == "foo.avi"
    assert isinstance(download.new_events[0], DownloadFileInfosSettedEvent)
