import pytest
from hastur.domain.shared_kernel.locker import AlreadyLockedError, LockNotExistsError
from .locker import InMemoryLocker


def test_in_memory_locker_lock():
    locker = InMemoryLocker()
    locker.lock("test")

    with pytest.raises(AlreadyLockedError):
        locker.lock("test")

    locker.lock("another lock")


def test_in_memory_locker_unlock():
    locker = InMemoryLocker()
    locker.lock("test")
    locker.unlock("test")

    with pytest.raises(LockNotExistsError):
        locker.unlock("test")

    locker.lock("test")
