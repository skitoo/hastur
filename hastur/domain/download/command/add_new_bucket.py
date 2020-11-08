from uuid import uuid4, UUID
from dataclasses import dataclass
from abc import ABC, abstractmethod
from hastur.domain.shared_kernel.store import EventStore, EventStoreError
from hastur.domain.shared_kernel.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
)
from hastur.domain.download.entity.bucket import Bucket


@dataclass
class AddNewBucketCommand(Command):
    pass


@dataclass
class AddNewBucketResponse(Response):
    bucket_id: UUID = None


class AddNewBucketPresenter(Presenter, ABC):
    @abstractmethod
    def present(self, response: AddNewBucketResponse):
        pass


class AddNewBucket(CommandHandler):
    def __init__(self, store: EventStore):
        self.store: EventStore = store

    def message_type(self) -> type:
        return AddNewBucketCommand

    def execute(self, _: AddNewBucketCommand, presenter: AddNewBucketPresenter):
        response = AddNewBucketResponse()
        try:
            bucket = Bucket(uuid4())
            self.store.save(bucket)
        except EventStoreError as error:
            response.error = error
        else:
            response.bucket_id = bucket.get_id()
        presenter.present(response)