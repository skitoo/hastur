# pylint: disable=no-name-in-module
from uuid import UUID, uuid4
from typing import cast
from pydantic import BaseModel, HttpUrl
from hastur.core.manager import AggregateManager
from hastur.core.error import UnknownErrorMessage
from hastur.core.locker import Locker, AlreadyLockedError
from hastur.core.error import HasturError
from hastur.core.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
    Message,
)
from hastur.domain.download.entity import (
    Download,
    DownloadCreatedEvent,
    DownloadStatus,
)
from ..error import UrlAlreadyRegistered


class AddNewUrlCommand(Command):
    url: HttpUrl


class AddNewUrlBodyResponse(BaseModel):
    download_id: UUID


class AddNewUrl(CommandHandler):
    def __init__(self, manager: AggregateManager, locker: Locker):
        super().__init__()
        self.manager: AggregateManager = manager
        self.locker: Locker = locker

    def message_type(self) -> type:
        return AddNewUrlCommand

    def execute(self, message: Message, presenter: Presenter):
        message = cast(AddNewUrlCommand, message)
        response = Response()
        try:
            self.locker.lock(message.url)
            download = Download(
                uuid4(),
                init_payload=DownloadCreatedEvent.Payload(
                    url=message.url, status=DownloadStatus.NEW
                ),
            )
            self.manager.save_and_dispatch([download])
        except AlreadyLockedError:
            response.error = UrlAlreadyRegistered()
        except HasturError as error:
            self.logger.exception(error)
            response.error = UnknownErrorMessage()
        else:
            response.body = AddNewUrlBodyResponse(download_id=download.get_id())
        presenter.present(response)
