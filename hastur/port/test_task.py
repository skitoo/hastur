import asyncio
from unittest.mock import Mock, patch
from uuid import uuid4
from hastur.domain.download.command.update_file_infos import UpdateFileInfosCommand
from hastur.domain.download.command.set_download_offline import (
    SetDownloadOfflineCommand,
)
from .task import AsyncDownloader


@patch("hastur.port.task.requests")
def test_async_download_fetch_file_infos_when_file_exists(mocked_requests):
    id_, url = uuid4(), "http://foo.com/bar.avi"
    event_bus, command_bus, response = (
        Mock(),
        Mock(),
        Mock(status_code=200, headers={"Content-length": 1000}),
    )
    mocked_requests.head.return_valued = response
    loop = asyncio.get_event_loop()

    downloader = AsyncDownloader(event_bus, command_bus)
    loop.run_until_complete(downloader.fetch_file_infos(id_, url))

    mocked_requests.head.assert_called_once_with(url)
    command_bus.execute.called_once_with(
        UpdateFileInfosCommand(id_=id_, size=10000, filename="bar.avi")
    )


@patch("hastur.port.task.requests")
def test_async_download_fetch_file_infos_when_file_not_exists(mocked_requests):
    id_, url = uuid4(), "http://foo.com/bar.avi"
    event_bus, command_bus, response = Mock(), Mock(), Mock(status_code=404)
    mocked_requests.head.return_valued = response
    loop = asyncio.get_event_loop()

    downloader = AsyncDownloader(event_bus, command_bus)
    loop.run_until_complete(downloader.fetch_file_infos(id_, url))

    mocked_requests.head.assert_called_once_with(url)
    command_bus.execute.called_once_with(SetDownloadOfflineCommand(id_=id_))
