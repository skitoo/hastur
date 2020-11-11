from hastur.domain.shared_kernel.locker import Locker
from hastur.domain.shared_kernel.message import CommandBus, QueryBus
from hastur.domain.shared_kernel.manager import AggregateManager
from hastur.domain.shared_kernel.event import EventBus
from hastur.domain.shared_kernel.store import EventStore
from hastur.domain.download.command.add_new_url import AddNewUrl
from hastur.domain.download.query.download_list import DownloadList
from hastur.domain.download.projection import ProjectionFactory


class Application:
    def __init__(
        self,
        store: EventStore,
        event_bus: EventBus,
        locker: Locker,
        projection_factory: ProjectionFactory,
    ):
        self.__manager: AggregateManager = AggregateManager(store, event_bus)
        self.__locker: Locker = locker
        self.__projection_factory: ProjectionFactory = projection_factory

        self.__init_command_bus()
        self.__init_query_bus()

    def __init_command_bus(self):
        self.command_bus: CommandBus = CommandBus()
        self.command_bus.register_handler(AddNewUrl(self.__manager, self.__locker))

    def __init_query_bus(self):
        self.query_bus: QueryBus = QueryBus()
        self.query_bus.register_handler(
            DownloadList(self.__projection_factory.create_download_projection())
        )
