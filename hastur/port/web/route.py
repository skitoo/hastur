from fastapi import APIRouter, status
from hastur.domain.download.command.add_new_url import (
    AddNewUrlCommand,
    AddNewUrlBodyResponse,
)
from hastur.domain.download.query.download_list import (
    DownloadListQuery,
    DownloadListBodyResponse,
)
from .presenter import HttpPresenter
from .resource import application as app


router = APIRouter()


@router.post(
    "/downloads",
    status_code=status.HTTP_201_CREATED,
    response_model=AddNewUrlBodyResponse,
)
async def add_new_url(command: AddNewUrlCommand):
    presenter = HttpPresenter()
    app.command_bus.execute(command, presenter)
    return presenter.result


@router.get("/downloads", response_model=DownloadListBodyResponse)
async def download_list():
    presenter = HttpPresenter()
    app.query_bus.execute(DownloadListQuery(), presenter)
    return presenter.result
