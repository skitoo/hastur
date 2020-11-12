from unittest.mock import Mock
from uuid import uuid4
from hastur.core.message import Response
from hastur.core.store import StreamNotFoundError
from hastur.core.error import HasturError, UnknownErrorMessage
from hastur.domain.download.entity import Download
from hastur.domain.download.error import UnknownDownload
from .update_file_infos import UpdateFileInfos, UpdateFileInfosCommand


def test_update_file_infos_message_type():
    assert UpdateFileInfos(Mock()).message_type() == UpdateFileInfosCommand


def test_update_file_infos_success():
    id_ = uuid4()
    download = Mock()
    manager, presenter, command = (
        Mock(**{"load.return_value": download}),
        Mock(),
        UpdateFileInfosCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    UpdateFileInfos(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    download.set_infos.assert_called_once_with(1000, "foo.avi")
    download.set_online.assert_called_once()
    manager.save_and_dispatch.assert_called_once_with([download])
    presenter.present.assert_called_once_with(Response())


def test_update_file_infos_with_unknown_id():
    id_ = uuid4()
    manager, presenter, command = (
        Mock(**{"load.side_effect": StreamNotFoundError(id_)}),
        Mock(),
        UpdateFileInfosCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    UpdateFileInfos(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    manager.save_and_dispatch.assert_not_called()
    presenter.present.assert_called_once_with(Response(error=UnknownDownload()))


def test_update_file_infos_with_unknown_error():
    id_ = uuid4()
    manager, presenter, command = (
        Mock(**{"load.side_effect": HasturError()}),
        Mock(),
        UpdateFileInfosCommand(id_=id_, size=1000, filename="foo.avi"),
    )

    UpdateFileInfos(manager).execute(command, presenter)

    manager.load.assert_called_once_with(id_, Download)
    manager.save_and_dispatch.assert_not_called()
    presenter.present.assert_called_once_with(Response(error=UnknownErrorMessage()))
