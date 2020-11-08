from datetime import datetime
from hastur.domain.shared_kernel.entity import Aggregate, AggregateError
from hastur.domain.download.event import (
    BucketCreatedEvent,
)

now = datetime.now


class BucketError(AggregateError):
    pass


class Bucket(Aggregate):
    __urls: set

    def post_init(self, _):
        if not self.stream:
            self.apply_new_event(
                BucketCreatedEvent(self.get_id(), now(), self.next_version)
            )

    def on_bucket_created(self, _: BucketCreatedEvent):
        self.__urls = set()

    @property
    def urls(self):
        return self.__urls
