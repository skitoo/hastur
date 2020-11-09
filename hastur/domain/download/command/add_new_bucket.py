from uuid import uuid4, UUID
from typing import Optional
from hastur.domain.shared_kernel.store import EventStore, EventStoreError
from hastur.domain.shared_kernel.message import (
    Command,
    CommandHandler,
    Response,
    Presenter,
)
from hastur.domain.download.entity.bucket import Bucket


class AddNewBucketCommand(Command):
    pass


class AddNewBucketResponse(Response):
    bucket_id: Optional[UUID] = None


class AddNewBucket(CommandHandler):
    def __init__(self, store: EventStore):
        self.store: EventStore = store

    def message_type(self) -> type:
        return AddNewBucketCommand

    def execute(self, _: AddNewBucketCommand, presenter: Presenter):
        response = AddNewBucketResponse()
        try:
            bucket = Bucket(uuid4())
            self.store.save([bucket])
        except EventStoreError as error:
            response.error = error
        else:
            response.bucket_id = bucket.get_id()
        presenter.present(response)
