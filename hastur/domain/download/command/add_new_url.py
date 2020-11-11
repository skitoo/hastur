# pylint: disable=no-name-in-module
from uuid import UUID, uuid4
from pydantic import BaseModel, HttpUrl
from hastur.domain.shared_kernel.manager import AggregateManager
from hastur.domain.shared_kernel.error import UnknownErrorMessage
from hastur.domain.shared_kernel.locker import Locker, AlreadyLockedError
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

    def execute(self, message: AddNewUrlCommand, presenter: Presenter):
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
