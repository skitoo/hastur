from uuid import UUID
from typing import cast
from hastur.core.error import HasturError, UnknownErrorMessage
from hastur.core.store import StreamNotFoundError
from hastur.core.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
    Message,
)
from hastur.core.manager import AggregateManager
from hastur.domain.download.entity import Download
from hastur.domain.download.error import UnknownDownload


class UpdateFileInfosCommand(Command):
    id_: UUID
    size: int
    filename: str


class UpdateFileInfos(CommandHandler):
    def __init__(self, manager: AggregateManager):
        super().__init__()
        self.manager: AggregateManager = manager

    def message_type(self) -> type:
        return UpdateFileInfosCommand

    def execute(self, message: Message, presenter: Presenter):
        message = cast(UpdateFileInfosCommand, message)
        response = Response()
        try:
            download: Download = cast(
                Download, self.manager.load(message.id_, Download)
            )
            download.set_online()
            download.set_infos(message.size, message.filename)
            self.manager.save_and_dispatch([download])
        except StreamNotFoundError:
            response.error = UnknownDownload()
        except HasturError as error:
            self.logger.exception(error)
            response.error = UnknownErrorMessage()
        presenter.present(response)
