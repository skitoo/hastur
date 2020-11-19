from typing import Set, Any
from hastur.core.locker import (
    Locker,
    AlreadyLockedError,
    LockNotExistsError,
)


class InMemoryLocker(Locker):
    def __init__(self):
        self.locks: Set[Any] = set()

    def lock(self, value: Any):
        if value in self.locks:
            raise AlreadyLockedError(value)
        self.locks.add(value)

    def unlock(self, value: Any):
        if value not in self.locks:
            raise LockNotExistsError(value)
        self.locks.remove(value)
