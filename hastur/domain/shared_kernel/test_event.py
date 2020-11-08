from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime
import pytest
from .event import DomainEvent, EventError


id_ = uuid4()
now = datetime.now()
VERSION = 1


class DownloadCreatedEvent(DomainEvent):
    @dataclass
    class Payload:
        url: str


class CardSended(DomainEvent):
    @dataclass
    class Payload:
        name: str


def test_to_string():
    event = DomainEvent(id_, now, VERSION)
    assert str(event) == f"<DomainEvent id: {id_} created_at: {now} version: {VERSION}>"

    event = DownloadCreatedEvent(id_, now, VERSION)
    assert (
        str(event)
        == f"<DownloadCreatedEvent id: {id_} created_at: {now} version: {VERSION}>"
    )

    event = CardSended(id_, now, VERSION)
    assert str(event) == f"<CardSended id: {id_} created_at: {now} version: {VERSION}>"


def test_handler_name():
    event = DomainEvent(id_, now, VERSION)
    assert event.handler_name == "on_domain"

    event = DownloadCreatedEvent(id_, now, VERSION)
    assert event.handler_name == "on_download_created"

    event = CardSended(id_, now, VERSION)
    assert event.handler_name == "on_card_sended"


def test_payload():
    event = DownloadCreatedEvent(
        id_, now, VERSION, DownloadCreatedEvent.Payload("toto.com")
    )

    assert event.payload == DownloadCreatedEvent.Payload("toto.com")

    with pytest.raises(EventError):
        DownloadCreatedEvent(id_, now, VERSION, "toto.com")

    with pytest.raises(EventError):
        DownloadCreatedEvent(id_, now, VERSION, CardSended.Payload("Test"))
