from unittest.mock import Mock
from .projection import InMemoryDownloadProjection


def test_in_memory_download_projection():
    projection = InMemoryDownloadProjection(Mock())
    dl1 = Mock()
    dl2 = Mock()
    projection.add(dl1)
    projection.add(dl2)
    assert projection.list() == [dl1, dl2]

    projection.add(dl1)
    assert projection.list() == [dl1, dl2]
