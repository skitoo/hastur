from unittest import TestCase
from unittest.mock import Mock, call
from uuid import uuid4, UUID
from dataclasses import dataclass
from datetime import datetime
import pytest
from .entity import Aggregate, EventVersionError, HandlerNotFoundError
from .event import DomainEvent, EventStream


class DownloadCreatedEvent(DomainEvent):
    @dataclass
    class Payload:
        url: str


class UnknownEvent(DomainEvent):
    pass


class MyEntity(Aggregate):
    def __init__(
        self, id_: UUID, mock: Mock, stream: EventStream = None, init_payload=None
    ):
        self.mock = mock
        super().__init__(id_, stream, init_payload)

    def post_init(self, payload):
        self.mock.post_init(payload)

    def on_download_created(self, event: DownloadCreatedEvent):
        self.mock.event_called(event)


class TestAggregate(TestCase):
    def setUp(self):
        self.id_ = uuid4()
        self.stream = []
        self.now = datetime.now()
        self.version = 1
        self.mock = Mock()
        self.instance = MyEntity(self.id_, self.mock, self.stream)

    def test_get_id(self):
        self.assertEqual(self.instance.get_id(), self.id_)

    def test_stream(self):
        self.assertEqual(self.instance.stream, self.stream)
        self.assertNotEqual(id(self.instance.stream), id(self.stream))

    def test_base_version(self):
        self.assertEqual(self.instance.base_version, 0)

    def test_apply_new_event_with_success(self):
        event = DownloadCreatedEvent(self.id_, self.now, self.version)
        self.instance.apply_new_event(event)

        self.mock.event_called.assert_called_once_with(event)
        self.assertEqual(self.instance.new_events, [event])
        self.assertEqual(self.instance.stream, [])

    def test_apply_new_event_with_invalid_version(self):
        event = DownloadCreatedEvent(self.id_, self.now, 100)
        with pytest.raises(EventVersionError):
            self.instance.apply_new_event(event)

        self.mock.event_called.assert_not_called()
        self.assertEqual(self.instance.new_events, [])

    def test_apply_new_event_with_unknown_event(self):
        event = UnknownEvent(self.id_, self.now, self.version)
        with pytest.raises(HandlerNotFoundError):
            self.instance.apply_new_event(event)

        self.mock.event_called.assert_not_called()
        self.assertEqual(self.instance.new_events, [])

    def test_next_version(self):
        event = DownloadCreatedEvent(self.id_, self.now, self.version)

        self.assertEqual(self.instance.next_version, 1)
        self.instance.apply_new_event(event)
        self.assertEqual(self.instance.next_version, 2)

    def test___replay_events_with_success(self):
        event1 = DownloadCreatedEvent(self.id_, self.now, 1)
        event2 = DownloadCreatedEvent(self.id_, self.now, 2)
        event3 = DownloadCreatedEvent(self.id_, self.now, 3)
        stream = [event1, event2, event3]
        instance = MyEntity(self.id_, self.mock, stream)

        self.mock.event_called.assert_has_calls(
            [
                call(event1),
                call(event2),
                call(event3),
            ],
        )
        self.assertEqual(self.mock.event_called.call_count, 3)
        self.assertEqual(instance.new_events, [])
        self.assertEqual(instance.stream, stream)
        self.assertNotEqual(id(instance.stream), id(stream))
        self.assertEqual(instance.next_version, 4)
        self.assertEqual(instance.base_version, 3)

    def test___replay_events_with_fail(self):
        event1 = DownloadCreatedEvent(self.id_, self.now, 1)
        event2 = UnknownEvent(self.id_, self.now, 2)
        stream = [event1, event2]

        with pytest.raises(HandlerNotFoundError):
            MyEntity(self.id_, self.mock, stream)

    def test_post_init(self):
        payload = DownloadCreatedEvent.Payload("toto.com")
        mock = Mock()
        MyEntity(self.id_, mock, init_payload=payload)

        mock.post_init.assert_called_once_with(payload)
