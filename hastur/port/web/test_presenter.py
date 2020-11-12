# pylint: disable=no-name-in-module
from fastapi import HTTPException, status
from pydantic import BaseModel
import pytest
from hastur.core.error import UnknownErrorMessage
from hastur.core.message import Response
from hastur.domain.download.error import UrlAlreadyRegistered
from .presenter import HttpPresenter


class Sample(BaseModel):
    foo_: str


def test_present_with_success_response():
    expected_result = Sample(foo_="bar")
    response = Response(body=expected_result)
    presenter = HttpPresenter()
    presenter.present(response)
    assert presenter.result == expected_result


def test_present_with_unknown_error_message():
    response = Response(error=UnknownErrorMessage())
    presenter = HttpPresenter()
    with pytest.raises(HTTPException) as error:
        presenter.present(response)
        assert error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert error.detail == response.error.dict()


def test_present_with_url_already_registered():
    response = Response(error=UrlAlreadyRegistered())
    presenter = HttpPresenter()
    with pytest.raises(HTTPException) as error:
        presenter.present(response)
        assert error.status_code == status.HTTP_400_BAD_REQUEST
        assert error.detail == response.error.dict()
