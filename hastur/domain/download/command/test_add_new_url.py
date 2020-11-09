from unittest.mock import Mock
from datetime import datetime
from hastur.domain.shared_kernel.locker import AlreadyLockedError
from hastur.domain.shared_kernel.store import EventStoreError
from hastur.domain.download.entity.download import DownloadStatus
from .add_new_url import AddNewUrl, AddNewUrlCommand, AddNewUrlResponse

now = datetime.now
URL = "http://foo.com"


def test_add_new_url_message_type():
    assert AddNewUrl(Mock(), Mock()).message_type() == AddNewUrlCommand


def test_add_new_url_success():
    store, presenter, locker, command = (
        Mock(),
        Mock(),
        Mock(),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(store, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    store.save.assert_called_once()
    presenter.present.assert_called_once()

    [download] = store.save.call_args.args[0]
    assert download.url == command.url
    assert download.status == DownloadStatus.NEW
    assert presenter.present.call_args.args[0] == AddNewUrlResponse(
        download_id=download.get_id()
    )


def test_add_new_url_when_lock_fail():
    error = AlreadyLockedError(URL)
    store, presenter, locker, command = (
        Mock(),
        Mock(),
        Mock(**{"lock.side_effect": error}),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(store, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    store.save.assert_not_called()
    presenter.present.assert_called_once()

    assert presenter.present.call_args.args[0] == AddNewUrlResponse(error=error)


def test_add_new_url_when_save_fail():
    error = EventStoreError(URL)
    store, presenter, locker, command = (
        Mock(**{"save.side_effect": error}),
        Mock(),
        Mock(),
        AddNewUrlCommand(url=URL),
    )

    AddNewUrl(store, locker).execute(command, presenter)

    locker.lock.assert_called_once_with(command.url)
    store.save.assert_called_once()
    presenter.present.assert_called_once()

    assert presenter.present.call_args.args[0] == AddNewUrlResponse(error=error)
