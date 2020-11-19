from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4
import pytest
from .memory import InMemoryEventStore, BaseVersionNotMatchError, StreamNotFoundError


class TestInMemoryEventStore(TestCase):
    def setUp(self):
        self.instance = InMemoryEventStore()

    def test_save_first_insert_with_sucess(self):
        myid = uuid4()
        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid}",
        )
        self.instance.save([aggregate])

        self.assertEqual(self.instance.events, {f"Mock:{myid}": aggregate.new_events})

    def test_save_another_insert_with_sucess(self):
        myid = uuid4()

        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid}",
        )
        self.instance.save([aggregate])

        first_events = aggregate.new_events

        aggregate = Mock(
            base_version=3,
            new_events=[
                Mock(version=4),
                Mock(version=5),
                Mock(version=6),
            ],
            index=f"Mock:{myid}",
        )
        self.instance.save([aggregate])

        self.assertEqual(
            self.instance.events,
            {f"Mock:{myid}": first_events + aggregate.new_events},
        )

    def test_save_another_insert_with_different_id_with_sucess(self):
        myid1, myid2 = uuid4(), uuid4()
        aggregate1 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid1}",
        )
        self.instance.save([aggregate1])

        aggregate2 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid2}",
        )
        self.instance.save([aggregate2])

        self.assertEqual(
            self.instance.events,
            {
                f"Mock:{myid1}": aggregate1.new_events,
                f"Mock:{myid2}": aggregate2.new_events,
            },
        )

    def test_save_with_fail(self):
        myid = uuid4()
        aggregate1 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid}",
        )
        self.instance.save([aggregate1])

        aggregate2 = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=aggregate1.index,
        )
        with pytest.raises(BaseVersionNotMatchError):
            self.instance.save([aggregate2])

    def test_load_stream_with_success(self):
        myid = uuid4()
        aggregate = Mock(
            base_version=0,
            new_events=[
                Mock(version=1),
                Mock(version=2),
                Mock(version=3),
            ],
            index=f"Mock:{myid}",
        )
        self.instance.save([aggregate])

        stream = self.instance.load_stream(myid, Mock)
        self.assertEqual(stream, aggregate.new_events)

    def test_load_stream_with_fail(self):
        with pytest.raises(StreamNotFoundError):
            self.instance.load_stream(uuid4(), Mock)
