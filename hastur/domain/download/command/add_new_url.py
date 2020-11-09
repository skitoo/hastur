# pylint: disable=no-name-in-module
from uuid import UUID, uuid4
from typing import Optional
from pydantic import HttpUrl
from hastur.domain.shared_kernel.store import EventStore
from hastur.domain.shared_kernel.error import HasturError
from hastur.domain.shared_kernel.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
)
from hastur.domain.download.entity.bucket import Bucket
from hastur.domain.download.entity.download import Download, DownloadCreatedEvent


class AddNewUrlCommand(Command):
    bucket_id: UUID
    url: HttpUrl


class AddNewUrlResponse(Response):
    download_id: Optional[UUID] = None


class AddNewUrl(CommandHandler):
    def __init__(self, store: EventStore):
        self.store: EventStore = store

    def message_type(self) -> type:
        return AddNewUrlCommand

    def execute(self, message: AddNewUrlCommand, presenter: Presenter):
        response = AddNewUrlResponse()
        try:
            stream = self.store.load_stream(message.bucket_id, Bucket)
            bucket = Bucket(message.bucket_id, stream)
            bucket.add_url(message.url)
            download = Download(
                uuid4(), init_payload=DownloadCreatedEvent.Payload(message.url)
            )
            self.store.save([bucket, download])
        except HasturError as error:
            response.error = error
        else:
            response.download_id = download.get_id()
        presenter.present(response)
