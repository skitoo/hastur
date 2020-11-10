from typing import Optional, List
from hastur.domain.shared_kernel.message import Query, QueryHandler, Response, Presenter
from hastur.domain.shared_kernel.error import HasturError
from hastur.domain.download.projection import Download, DownloadProjection


class DownloadListQuery(Query):
    pass


class DownloadListResponse(Response):
    downloads: Optional[List[Download]] = None


class DownloadList(QueryHandler):
    def __init__(self, projection: DownloadProjection):
        self.projection: DownloadProjection = projection

    def message_type(self) -> type:
        return DownloadListQuery

    def execute(self, _: DownloadListQuery, presenter: Presenter):
        response = DownloadListResponse()
        try:
            response.downloads = self.projection.list()
        except HasturError as error:
            response.error = error
        presenter.present(response)
