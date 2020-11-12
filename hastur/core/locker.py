from abc import ABC, abstractmethod
from typing import Any, NoReturn
from .error import HasturError


class LockError(HasturError):
    pass


class AlreadyLockedError(LockError):
    def __init__(self, value: Any):
        super().__init__(self, f"{value} is already locked")


class LockNotExistsError(LockError):
    def __init__(self, value: Any):
        super().__init__(self, f"{value} lock not exists")


class Locker(ABC):
    @abstractmethod
    def lock(self, value: Any) -> NoReturn:
        pass

    @abstractmethod
    def unlock(self, value: Any) -> NoReturn:
        pass
