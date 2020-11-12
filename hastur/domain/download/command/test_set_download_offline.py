from unittest.mock import Mock
from uuid import uuid4
from hastur.core.message import Response
from hastur.core.store import StreamNotFoundError
from hastur.core.error import HasturError, UnknownErrorMessage
from hastur.domain.download.entity.download import Download
from hastur.domain.download.error import UnknownDownload
from .set_download_offline import SetDownloadOffline, SetDownloadOfflineCommand


def test_set_download_offline_message_type():
    assert SetDownloadOffline(Mock()).message_type() == SetDownloadOfflineCommand


def test_set_download_offline_success():
    id_ = uuid4()
    download = Mock()
    manager, presenter, command = (
        Mock(**{"load.return_value": download}),
        Mock(),
        SetDownloadOfflineCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    SetDownloadOffline(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    download.set_offline.assert_called_once()
    manager.save_and_dispatch.assert_called_once_with([download])
    presenter.present.assert_called_once_with(Response())


def test_set_download_offline_with_unknown_id():
    id_ = uuid4()
    manager, presenter, command = (
        Mock(**{"load.side_effect": StreamNotFoundError(id_)}),
        Mock(),
        SetDownloadOfflineCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    SetDownloadOffline(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    manager.save_and_dispatch.assert_not_called()
    presenter.present.assert_called_once_with(Response(error=UnknownDownload()))


def test_set_download_offline_with_unknown_error():
    id_ = uuid4()
    manager, presenter, command = (
        Mock(**{"load.side_effect": HasturError()}),
        Mock(),
        SetDownloadOfflineCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    SetDownloadOffline(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    manager.save_and_dispatch.assert_not_called()
    presenter.present.assert_called_once_with(Response(error=UnknownErrorMessage()))
