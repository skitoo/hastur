from uuid import UUID
from typing import Optional
from hastur.domain.shared_kernel.error import HasturError, UnknownErrorMessage
from hastur.domain.shared_kernel.store import StreamNotFoundError
from hastur.domain.shared_kernel.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
)
from hastur.domain.shared_kernel.manager import AggregateManager
from hastur.domain.download.entity.download import Download
from hastur.domain.download.error import UnknownDownload


class UpdateFileInfosCommand(Command):
    id_: UUID
    size: Optional[int] = None
    filename: Optional[str] = None


class UpdateFileInfos(CommandHandler):
    def __init__(self, manager: AggregateManager):
        super().__init__()
        self.manager: AggregateManager = manager

    def message_type(self) -> type:
        return UpdateFileInfosCommand

    def execute(self, message: UpdateFileInfosCommand, presenter: Presenter):
        response = Response()
        try:
            download: Download = self.manager.load(message.id_, Download)
            download.set_online()
            download.set_infos(message.size, message.filename)
            self.manager.save_and_dispatch([download])
        except StreamNotFoundError:
            response.error = UnknownDownload()
        except HasturError as error:
            self.logger.exception(error)
            response.error = UnknownErrorMessage()
        presenter.present(response)
