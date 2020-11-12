from unittest.mock import Mock
from datetime import datetime
from hastur.core.locker import AlreadyLockedError
from hastur.core.store import EventStoreError
from hastur.core.message import Response
from hastur.core.error import UnknownErrorMessage
from hastur.domain.download.entity import DownloadStatus
from ..error import UrlAlreadyRegistered
from .add_new_url import AddNewUrl, AddNewUrlCommand, AddNewUrlBodyResponse

now = datetime.now
URL = "http://foo.com"


def test_add_new_url_message_type():
    assert AddNewUrl(Mock(), Mock()).message_type() == AddNewUrlCommand


def test_add_new_url_success():
    manager, presenter, locker, command = (
        Mock(),
        Mock(),
        Mock(),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(manager, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    manager.save_and_dispatch.assert_called_once()
    presenter.present.assert_called_once()

    [download] = manager.save_and_dispatch.call_args.args[0]
    assert download.url == command.url
    assert download.status == DownloadStatus.NEW
    assert presenter.present.call_args.args[0] == Response(
        body=AddNewUrlBodyResponse(download_id=download.get_id())
    )


def test_add_new_url_when_lock_fail():
    error = AlreadyLockedError(URL)
    manager, presenter, locker, command = (
        Mock(),
        Mock(),
        Mock(**{"lock.side_effect": error}),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(manager, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    manager.save_and_dispatch.assert_not_called()
    presenter.present.assert_called_once()

    assert presenter.present.call_args.args[0] == Response(error=UrlAlreadyRegistered())


def test_add_new_url_when_save_fail():
    error = EventStoreError(URL)
    manager, presenter, locker, command = (
        Mock(**{"save_and_dispatch.side_effect": error}),
        Mock(),
        Mock(),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(manager, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    manager.save_and_dispatch.assert_called_once()
    presenter.present.assert_called_once()

    assert presenter.present.call_args.args[0] == Response(error=UnknownErrorMessage())
