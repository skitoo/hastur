# pylint: disable=no-name-in-module
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel
import pytest
from .event import DomainEvent, EventError


id_ = uuid4()
now = datetime.now()
VERSION = 1


class DownloadCreatedEvent(DomainEvent):
    class Payload(BaseModel):
        url: str


class CardSended(DomainEvent):
    class Payload(BaseModel):
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
        id_, now, VERSION, DownloadCreatedEvent.Payload(url="toto.com")
    )

    assert event.payload == DownloadCreatedEvent.Payload(url="toto.com")

    with pytest.raises(EventError):
        DownloadCreatedEvent(id_, now, VERSION, "toto.com")

    with pytest.raises(EventError):
        DownloadCreatedEvent(id_, now, VERSION, CardSended.Payload(name="Test"))
