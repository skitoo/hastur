from .helper import fullname, class_
from .message import NullPresenter


def test_fullname():
    assert fullname(NullPresenter()) == "hastur.core.message.NullPresenter"
    assert fullname("") == "builtins.str"


def test_class_():
    assert class_(fullname(NullPresenter())) == NullPresenter
    assert class_(fullname("")) == str
