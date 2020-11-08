from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from hastur.domain.shared_kernel.entity import Aggregate, AggregateError
from hastur.domain.shared_kernel.event import DomainEvent

now = datetime.now


class DownloadError(AggregateError):
    pass


class DownloadStatus(Enum):
    NEW = "new"


class DownloadCreatedEvent(DomainEvent):
    @dataclass
    class Payload:
        url: str


class Download(Aggregate):
    __url: str
    __status: DownloadStatus

    def post_init(self, payload: DownloadCreatedEvent.Payload):
        if not self.stream:
            if payload:
                self.apply_new_event(
                    DownloadCreatedEvent(
                        self.get_id(), now(), self.next_version, payload
                    )
                )
            else:
                raise DownloadError("Payload is required for new Download")
        elif payload:
            raise DownloadError("Payload is not required when Download already exists")

    def on_download_created(self, event: DownloadCreatedEvent):
        self.__url = event.payload.url
        self.__status = DownloadStatus.NEW

    @property
    def url(self) -> str:
        return self.__url

    @property
    def status(self) -> DownloadStatus:
        return self.__status
