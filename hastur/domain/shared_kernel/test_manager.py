from unittest.mock import Mock
from .manager import AggregateManager


def test_aggregate_manager_load():
    stream, aggregate_type = Mock(), Mock(return_value="aggregate")
    store, bus, id_ = Mock(**{"load_stream.return_value": stream}), Mock(), Mock()

    manager = AggregateManager(store, bus)
    aggregate = manager.load(id_, aggregate_type)

    assert aggregate == "aggregate"
    store.load_stream.called_once_with(id_, Mock)
    aggregate_type.called_once_with(id_, stream)


def test_save_and_dispatch():
    store, bus = Mock(), Mock()
    evt1, evt2, evt3 = Mock(), Mock(), Mock()
    aggr1, aggr2 = Mock(new_events=[evt1, evt2]), Mock(new_events=[evt3])
    manager = AggregateManager(store, bus)
    manager.save_and_dispatch([aggr1, aggr2])

    store.save.assert_called_once_with([aggr1, aggr2])
    bus.dispatch.assert_called_once_with([evt1, evt2, evt3])
