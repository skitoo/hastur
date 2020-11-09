from typing import List, Any, NoReturn
from hastur.domain.shared_kernel.locker import (
    Locker,
    AlreadyLockedError,
    LockNotExistsError,
)


class InMemoryLocker(Locker):
    def __init__(self):
        self.locks: List[Any] = set()

    def lock(self, value: Any) -> NoReturn:
        if value in self.locks:
            raise AlreadyLockedError(value)
        self.locks.add(value)

    def unlock(self, value: Any) -> NoReturn:
        if value not in self.locks:
            raise LockNotExistsError(value)
        self.locks.remove(value)
