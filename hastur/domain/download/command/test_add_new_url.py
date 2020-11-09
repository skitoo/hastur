from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from hastur.domain.shared_kernel.store import StreamNotFoundError, EventStoreError
from hastur.domain.download.entity.bucket import BucketCreatedEvent, Bucket
from hastur.domain.download.entity.download import DownloadStatus
from .add_new_url import AddNewUrl, AddNewUrlCommand

now = datetime.now


def test_add_new_url_message_type():
    assert AddNewUrl(Mock()).message_type() == AddNewUrlCommand


def test_add_new_url_success():
    id_ = uuid4()
    url = "toto.com"
    store, presenter, command = Mock(), Mock(), Mock(bucket_id=id_, url=url)
    store.load_stream.return_value = [BucketCreatedEvent(id_, now(), 1)]

    AddNewUrl(store).execute(command, presenter)

    store.load_stream.assert_called_once_with(id_, Bucket)

    assert len(store.save.mock_calls) == 1
    bucket, download = store.save.mock_calls[0].args[0]

    assert bucket.get_id() == id_
    assert url in bucket.urls
    assert download.url == url
    assert download.status == DownloadStatus.NEW

    response = presenter.present.call_args[0][0]
    assert response.download_id == download.get_id()
    assert response.error is None


def test_add_new_url_with_invalid_bucket_id():
    id_ = uuid4()
    url = "toto.com"
    store, presenter, command = Mock(), Mock(), Mock(bucket_id=id_, url=url)
    store.load_stream.side_effect = StreamNotFoundError(id_)

    AddNewUrl(store).execute(command, presenter)

    store.save.assert_not_called()
    response = presenter.present.call_args[0][0]
    assert response.download_id is None
    assert isinstance(response.error, StreamNotFoundError)


def test_add_new_url_when_save_fail():
    id_ = uuid4()
    url = "toto.com"
    store, presenter, command = Mock(), Mock(), Mock(bucket_id=id_, url=url)
    store.load_stream.return_value = [BucketCreatedEvent(id_, now(), 1)]
    store.save.side_effect = EventStoreError

    AddNewUrl(store).execute(command, presenter)

    store.load_stream.assert_called_once_with(id_, Bucket)
    response = presenter.present.call_args[0][0]
    assert response.download_id is None
    assert isinstance(response.error, EventStoreError)
