from uuid import uuid4
from datetime import datetime
import pytest
from hastur.domain.download.event import DownloadCreatedEvent
from .download import Download, DownloadStatus, DownloadError


now = datetime.now


def test_download_post_init_with_payload_and_without_stream():
    download = Download(uuid4(), init_payload=DownloadCreatedEvent.Payload("toto.com"))
    assert len(download.new_events) == 1
    assert isinstance(download.new_events[0], DownloadCreatedEvent)
    assert download.url == "toto.com"
    assert download.status == DownloadStatus.NEW


def test_download_post_init_without_payload_and_without_stream():
    with pytest.raises(DownloadError):
        Download(uuid4())


def test_download_post_init_without_payload_and_with_stream():
    id_ = uuid4()
    download = Download(
        id_,
        [DownloadCreatedEvent(id_, now(), 1, DownloadCreatedEvent.Payload("toto.com"))],
    )
    assert len(download.new_events) == 0
    assert download.url == "toto.com"
    assert download.status == DownloadStatus.NEW


def test_download_post_init_with_payload_and_with_stream():
    with pytest.raises(DownloadError):
        id_ = uuid4()
        Download(
            id_,
            [
                DownloadCreatedEvent(
                    id_, now(), 1, DownloadCreatedEvent.Payload("toto.com")
                )
            ],
            DownloadCreatedEvent.Payload("toto.com"),
        )
