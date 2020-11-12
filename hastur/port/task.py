# pylint: disable=no-name-in-module
from uuid import UUID
import asyncio
from pydantic import HttpUrl
import requests
from hastur.domain.shared_kernel.message import NullPresenter
from hastur.domain.download.task import Downloader
from hastur.domain.download.entity.download import DownloadCreatedEvent
from hastur.domain.download.command.update_file_infos import UpdateFileInfosCommand
from hastur.domain.download.command.set_download_offline import (
    SetDownloadOfflineCommand,
)


class AsyncDownloader(Downloader):
    def on_download_created(self, event: DownloadCreatedEvent):
        asyncio.create_task(self.fetch_file_infos(event.id_, event.payload.url))

    async def fetch_file_infos(self, id_: UUID, url: HttpUrl):
        self.logger.info("Fetch file infos: '%s'", url)
        response = requests.head(url)
        if response.status_code == 200:
            filename = url.split("/")[-1]
            self.command_bus.execute(
                UpdateFileInfosCommand(
                    id_=id_,
                    size=int(response.headers["Content-length"]),
                    filename=filename,
                ),
                NullPresenter(),
            )
        else:
            self.logger.warning("'%s' is offline", url)
            self.command_bus.execute(
                SetDownloadOfflineCommand(id_=id_),
                NullPresenter(),
            )
