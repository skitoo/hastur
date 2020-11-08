from uuid import uuid4
from datetime import datetime
import pytest
from .bucket import Bucket, BucketCreatedEvent, UrlAddedEvent, BucketError

now = datetime.now


def test_bucket_post_init_without_stream():
    bucket = Bucket(uuid4())
    assert len(bucket.new_events) == 1
    assert isinstance(bucket.new_events[0], BucketCreatedEvent)
    assert bucket.urls == set()


def test_bucket_post_init_with_stream():
    id_ = uuid4()
    stream = [BucketCreatedEvent(id_, now(), 1)]
    bucket = Bucket(id_, stream)
    assert len(bucket.new_events) == 0
    assert bucket.urls == set()


def test_bucket_add_url_with_success():
    bucket = Bucket(uuid4())
    bucket.add_url("toto.com")
    assert len(bucket.new_events) == 2
    assert isinstance(bucket.new_events[1], UrlAddedEvent)
    assert bucket.urls == {"toto.com"}


def test_bucket_add_url_with_fail():
    bucket = Bucket(uuid4())
    bucket.add_url("toto.com")
    with pytest.raises(BucketError):
        bucket.add_url("toto.com")
