# pylint: disable=no-name-in-module
from typing import List
from pydantic import BaseModel
from hastur.domain.shared_kernel.message import Query, QueryHandler, Response, Presenter
from hastur.domain.shared_kernel.error import HasturError, UnknownErrorMessage
from hastur.domain.download.projection import Download, DownloadProjection


class DownloadListQuery(Query):
    pass


class DownloadListBodyResponse(BaseModel):
    downloads: List[Download]


class DownloadList(QueryHandler):
    def __init__(self, projection: DownloadProjection):
        self.projection: DownloadProjection = projection

    def message_type(self) -> type:
        return DownloadListQuery

    def execute(self, _: DownloadListQuery, presenter: Presenter):
        response = Response()
        try:
            response.body = DownloadListBodyResponse(downloads=self.projection.list())
        except HasturError:
            response.error = UnknownErrorMessage()
        presenter.present(response)
