from uuid import uuid4
from datetime import datetime
from hastur.domain.download.event import BucketCreatedEvent
from .bucket import Bucket

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
