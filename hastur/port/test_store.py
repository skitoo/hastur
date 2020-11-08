from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4
import pytest
from .store import InMemoryEventStore, BaseVersionNotMatchError, StreamNotFoundError


class TestInMemoryEventStore(TestCase):
    def setUp(self):
        self.instance = InMemoryEventStore()

    def test_save_first_insert_with_sucess(self):
        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": uuid4()},
        )
        self.instance.save(aggregate)

        self.assertEqual(
            self.instance.events, {aggregate.get_id(): aggregate.new_events}
        )

    def test_save_another_insert_with_sucess(self):
        myid = uuid4()

        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": myid},
        )
        self.instance.save(aggregate)

        first_events = aggregate.new_events

        aggregate = Mock(
            base_version=3,
            new_events=[
                Mock(version=4),
                Mock(version=5),
                Mock(version=6),
            ],
            **{"get_id.return_value": myid},
        )
        self.instance.save(aggregate)

        self.assertEqual(
            self.instance.events,
            {aggregate.get_id(): first_events + aggregate.new_events},
        )

    def test_save_another_insert_with_different_id_with_sucess(self):
        aggregate1 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": uuid4()},
        )
        self.instance.save(aggregate1)

        aggregate2 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": uuid4()},
        )
        self.instance.save(aggregate2)

        self.assertEqual(
            self.instance.events,
            {
                aggregate1.get_id(): aggregate1.new_events,
                aggregate2.get_id(): aggregate2.new_events,
            },
        )

    def test_save_with_fail(self):
        aggregate1 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": uuid4()},
        )
        self.instance.save(aggregate1)

        aggregate2 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": aggregate1.get_id()},
        )
        with pytest.raises(BaseVersionNotMatchError):
            self.instance.save(aggregate2)

    def test_load_stream_with_success(self):
        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            **{"get_id.return_value": uuid4()},
        )
        self.instance.save(aggregate)

        stream = self.instance.load_stream(aggregate.get_id())
        self.assertEqual(stream, aggregate.new_events)

    def test_load_stream_with_fail(self):
        with pytest.raises(StreamNotFoundError):
            self.instance.load_stream(uuid4())
