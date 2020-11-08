from dataclasses import dataclass
from hastur.domain.shared_kernel.entity import DomainEvent


class BucketCreatedEvent(DomainEvent):
    pass


class DownloadCreatedEvent(DomainEvent):
    @dataclass
    class Payload:
        url: str
