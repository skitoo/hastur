#  from hastur.domain.shared_kernel.event import Domain
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
import pytest
from hastur.domain.shared_kernel.event import DomainEvent
from .event import LocalEventBus, EventBusError


class MyEvent(DomainEvent):
    pass


def test_local_event_bus_add_handler_success():
    bus = LocalEventBus()
    my_handler = Mock()
    bus.add_handler(DomainEvent, my_handler)
    assert bus.handlers == {DomainEvent: [my_handler]}


def test_local_event_bus_add_handler_fail():
    bus = LocalEventBus()
    my_handler = Mock()
    bus.add_handler(DomainEvent, my_handler)
    with pytest.raises(EventBusError):
        bus.add_handler(DomainEvent, my_handler)


def test_local_event_bus_dispatch():
    bus = LocalEventBus()
    my_handler1, my_handler2 = Mock(), Mock()
    event = DomainEvent(uuid4(), datetime.now(), 1)
    bus.add_handler(DomainEvent, my_handler1)
    bus.add_handler(MyEvent, my_handler2)

    bus.dispatch([event])
    my_handler1.assert_called_once_with(event)
    my_handler2.assert_not_called()


def test_local_event_bus_dispatch_bubbling():
    bus = LocalEventBus()
    my_handler1, my_handler2 = Mock(), Mock()
    event = MyEvent(uuid4(), datetime.now(), 1)
    bus.add_handler(DomainEvent, my_handler1)
    bus.add_handler(MyEvent, my_handler2)

    bus.dispatch([event])
    my_handler1.assert_called_once_with(event)
    my_handler2.assert_called_once_with(event)
