# pylint: disable=no-name-in-module
from uuid import UUID, uuid4
from typing import Optional
from pydantic import HttpUrl
from hastur.domain.shared_kernel.manager import AggregateManager
from hastur.domain.shared_kernel.locker import Locker
from hastur.domain.shared_kernel.error import HasturError
from hastur.domain.shared_kernel.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
)
from hastur.domain.download.entity.download import (
    Download,
    DownloadCreatedEvent,
    DownloadStatus,
)


class AddNewUrlCommand(Command):
    url: HttpUrl


class AddNewUrlResponse(Response):
    download_id: Optional[UUID] = None


class AddNewUrl(CommandHandler):
    def __init__(self, manager: AggregateManager, locker: Locker):
        self.manager: AggregateManager = manager
        self.locker: Locker = locker

    def message_type(self) -> type:
        return AddNewUrlCommand

    def execute(self, message: AddNewUrlCommand, presenter: Presenter):
        response = AddNewUrlResponse()
        try:
            self.locker.lock(message.url)
            download = Download(
                uuid4(),
                init_payload=DownloadCreatedEvent.Payload(
                    url=message.url, status=DownloadStatus.NEW
                ),
            )
            self.manager.save_and_dispatch([download])
        except HasturError as error:
            response.error = error
        else:
            response.download_id = download.get_id()
        presenter.present(response)
