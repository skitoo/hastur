from unittest.mock import Mock
from .projection import InMemoryDownloadProjection, InMemoryProjectionFactory


def test_in_memory_download_projection():
    projection = InMemoryDownloadProjection(Mock())
    dl1 = Mock()
    dl2 = Mock()
    projection.add(dl1)
    projection.add(dl2)
    assert projection.list() == [dl1, dl2]

    projection.add(dl1)
    assert projection.list() == [dl1, dl2]


def test_in_memory_projection_factory():
    bus = Mock()
    factory = InMemoryProjectionFactory(bus)
    projection = factory.create_download_projection()
    assert isinstance(projection, InMemoryDownloadProjection)
    assert projection.event_bus == bus
