from unittest.mock import Mock
from hastur.domain.shared_kernel.store import EventStoreError
from hastur.domain.download.entity.bucket import Bucket
from .add_new_bucket import AddNewBucket, AddNewBucketCommand, AddNewBucketResponse


def test_add_new_bucket_message_type():
    assert AddNewBucket(Mock()).message_type() == AddNewBucketCommand


def test_add_new_bucket_success():
    store, presenter, command = Mock(), Mock(), Mock()

    AddNewBucket(store).execute(command, presenter)

    store.save.assert_called_once()
    presenter.present.assert_called_once()

    bucket = store.save.call_args[0][0]
    assert isinstance(bucket, Bucket)

    response = presenter.present.call_args[0][0]
    assert isinstance(response, AddNewBucketResponse)

    assert response.bucket_id == bucket.get_id()
    assert response.error is None


def test_add_new_bucket_with_store_fail():
    store, presenter, command = (
        Mock(**{"save.side_effect": EventStoreError}),
        Mock(),
        Mock(),
    )

    AddNewBucket(store).execute(command, presenter)

    store.save.assert_called_once()

    response = presenter.present.call_args[0][0]
    assert response.bucket_id is None
    assert isinstance(response.error, EventStoreError)
