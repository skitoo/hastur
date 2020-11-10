from unittest.mock import Mock
from hastur.domain.shared_kernel.error import HasturError
from .download_list import DownloadList, DownloadListQuery, DownloadListResponse


def test_download_list_message_type():
    assert DownloadList(Mock()).message_type() == DownloadListQuery


def test_download_list_with_success():
    downloads = []
    projection, presenter = Mock(**{"list.return_value": downloads}), Mock()
    handler = DownloadList(projection)
    handler.execute(Mock(), presenter)

    projection.list.assert_called_once()
    presenter.present.assert_called_once()
    assert presenter.present.call_args.args[0] == DownloadListResponse(
        downloads=downloads
    )


def test_download_list_with_projection_fail():
    error = HasturError()
    projection, presenter = Mock(**{"list.side_effect": error}), Mock()
    handler = DownloadList(projection)
    handler.execute(Mock(), presenter)

    projection.list.assert_called_once()
    presenter.present.assert_called_once()
    assert presenter.present.call_args.args[0] == DownloadListResponse(error=error)
