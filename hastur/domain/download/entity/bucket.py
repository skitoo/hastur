from datetime import datetime
from dataclasses import dataclass
from hastur.domain.shared_kernel.entity import Aggregate, AggregateError
from hastur.domain.shared_kernel.event import DomainEvent

now = datetime.now


class BucketError(AggregateError):
    pass


class BucketCreatedEvent(DomainEvent):
    pass


class UrlAddedEvent(DomainEvent):
    @dataclass
    class Payload:
        url: str


class Bucket(Aggregate):
    __urls: set

    def post_init(self, _):
        if not self.stream:
            self.apply_new_event(
                BucketCreatedEvent(self.get_id(), now(), self.next_version)
            )

    def add_url(self, url: str):
        if url in self.urls:
            raise BucketError(
                f"Url {url} is already registered in bucket '{self.get_id()}'"
            )
        self.apply_new_event(
            UrlAddedEvent(
                self.get_id(),
                now(),
                self.next_version,
                UrlAddedEvent.Payload(url),
            )
        )

    def on_bucket_created(self, _: BucketCreatedEvent):
        self.__urls = set()

    def on_url_added(self, event: UrlAddedEvent):
        self.__urls.add(event.payload.url)

    @property
    def urls(self):
        return self.__urls
