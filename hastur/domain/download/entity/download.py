# pylint: disable=no-name-in-module
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, HttpUrl
from hastur.domain.shared_kernel.entity import Aggregate, AggregateError
from hastur.domain.shared_kernel.event import DomainEvent

now = datetime.now


class DownloadError(AggregateError):
    pass


class DownloadStatus(Enum):
    NEW = "new"
    OFFLINE = "offline"
    ONLINE = "online"


class DownloadCreatedEvent(DomainEvent):
    class Payload(BaseModel):
        url: HttpUrl
        status: DownloadStatus


class DownloadFileSettedOnlineEvent(DomainEvent):
    class Payload(BaseModel):
        status: DownloadStatus


class DownloadFileSettedOfflineEvent(DomainEvent):
    class Payload(BaseModel):
        status: DownloadStatus


class DownloadFileInfosSettedEvent(DomainEvent):
    class Payload(BaseModel):
        size: int
        filename: str


class Download(Aggregate):
    __url: str
    __status: DownloadStatus
    __size: int
    __filename: str

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

    def set_infos(self, size: int, filename: str):
        self.apply_new_event(
            DownloadFileInfosSettedEvent(
                self.get_id(),
                now(),
                self.next_version,
                DownloadFileInfosSettedEvent.Payload(size=size, filename=filename),
            )
        )

    def set_online(self):
        self.apply_new_event(
            DownloadFileSettedOnlineEvent(
                self.get_id(),
                now(),
                self.next_version,
                DownloadFileSettedOnlineEvent.Payload(status=DownloadStatus.ONLINE),
            )
        )

    def set_offline(self):
        self.apply_new_event(
            DownloadFileSettedOfflineEvent(
                self.get_id(),
                now(),
                self.next_version,
                DownloadFileSettedOfflineEvent.Payload(status=DownloadStatus.OFFLINE),
            )
        )

    def on_download_created(self, event: DownloadCreatedEvent):
        self.__url = event.payload.url
        self.__status = DownloadStatus.NEW

    def on_download_file_infos_setted(self, event: DownloadFileInfosSettedEvent):
        self.__size = event.payload.size
        self.__filename = event.payload.filename

    def on_download_file_setted_online(self, _: DownloadFileSettedOnlineEvent):
        self.__status = DownloadStatus.ONLINE

    def on_download_file_setted_offline(self, _: DownloadFileSettedOfflineEvent):
        self.__status = DownloadStatus.OFFLINE

    @property
    def url(self) -> str:
        return self.__url

    @property
    def status(self) -> DownloadStatus:
        return self.__status

    @property
    def size(self) -> int:
        return self.__size

    @property
    def filename(self) -> str:
        return self.__filename
