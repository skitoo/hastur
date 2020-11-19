# pylint: disable=no-name-in-module
from typing import List
from pydantic import BaseModel
from hastur.core.message import Query, QueryHandler, Response, Presenter, Message
from hastur.core.error import HasturError, UnknownErrorMessage
from hastur.domain.download.projection import Download, DownloadProjection


class DownloadListQuery(Query):
    pass


class DownloadListBodyResponse(BaseModel):
    downloads: List[Download]


class DownloadList(QueryHandler):
    def __init__(self, projection: DownloadProjection):
        super().__init__()
        self.projection: DownloadProjection = projection

    def message_type(self) -> type:
        return DownloadListQuery

    def execute(self, _: Message, presenter: Presenter):
        response = Response()
        try:
            response.body = DownloadListBodyResponse(downloads=self.projection.list())
        except HasturError as error:
            self.logger.exception(error)
            response.error = UnknownErrorMessage()
        presenter.present(response)
