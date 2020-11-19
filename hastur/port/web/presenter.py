# pylint: disable=no-name-in-module
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
from hastur.core.message import Presenter, Response
from hastur.core.error import UnknownErrorMessage
from hastur.domain.download.error import UrlAlreadyRegistered


class HttpPresenter(Presenter):
    result: Optional[BaseModel] = None

    def __init__(self):
        self.__map_error_with_http_code()

    def __map_error_with_http_code(self):
        self.__mapping = {
            UnknownErrorMessage: status.HTTP_500_INTERNAL_SERVER_ERROR,
            UrlAlreadyRegistered: status.HTTP_400_BAD_REQUEST,
        }

    def present(self, response: Response):
        if response.error:
            raise HTTPException(
                status_code=self.__mapping.get(
                    type(response.error), status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=response.error.dict(),
            )
        self.result = response.body
