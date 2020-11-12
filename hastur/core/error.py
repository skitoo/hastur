# pylint: disable=no-name-in-module
from pydantic import BaseModel


class HasturError(Exception):
    pass


class HasturErrorMessage(BaseModel):
    msg: str
    type: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, type=self.__class__.__name__, **kwargs)


class UnknownErrorMessage(HasturErrorMessage):
    msg: str = "Things are a little unstable here. I suggest come back later"
