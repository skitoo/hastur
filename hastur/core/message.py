# pylint: disable=no-name-in-module
from abc import ABC, abstractmethod
from logging import Logger, getLogger
from typing import Dict, Optional
from pydantic import BaseModel
from .error import HasturError, HasturErrorMessage


class MessageBusError(HasturError):
    pass


class CommandBusError(MessageBusError):
    pass


class QueryBusError(MessageBusError):
    pass


class Message(BaseModel, ABC):
    pass


class Command(Message, ABC):
    pass


class Query(Message, ABC):
    pass


class Response(BaseModel):
    error: Optional[HasturErrorMessage] = None
    body: Optional[BaseModel] = None


class Presenter(ABC):
    @abstractmethod
    def present(self, response: Response):
        pass


class NullPresenter(Presenter):
    def present(self, _: Response):
        pass


class MessageHandler(ABC):
    def __init__(self):
        self.logger: Logger = getLogger(str(type(self)))

    @abstractmethod
    def execute(self, message: Message, presenter: Presenter):
        pass

    @abstractmethod
    def message_type(self) -> type:
        pass


class CommandHandler(MessageHandler, ABC):
    pass


class QueryHandler(MessageHandler, ABC):
    pass


class MessageBus(ABC):
    def __init__(self):
        self.__handlers: Dict[type, MessageHandler] = {}

    def register_handler(self, handler: MessageHandler):
        self.check_handler_type(handler)
        if handler.message_type() in self.__handlers:
            raise MessageBusError(
                f"Handler '{handler.message_type()}' is already registered"
            )
        self.__handlers[handler.message_type()] = handler

    def execute(self, message: Message, presenter: Presenter):
        self.check_message_type(message)
        message_type = type(message)
        if message_type not in self.__handlers:
            raise MessageBusError(f"Handler '{message_type}' not found")
        self.__handlers[message_type].execute(message, presenter)

    @abstractmethod
    def check_handler_type(self, handler: MessageHandler):
        pass

    @abstractmethod
    def check_message_type(self, message: Message):
        pass


class CommandBus(MessageBus):
    def check_handler_type(self, handler: MessageHandler):
        if not isinstance(handler, CommandHandler):
            raise CommandBusError(f"Bad handler type. Received: {type(handler)}")

    def check_message_type(self, message: Message):
        if not isinstance(message, Command):
            raise CommandBusError(f"Bad message type. Received: {type(message)}")


class QueryBus(MessageBus):
    def check_handler_type(self, handler: MessageHandler):
        if not isinstance(handler, QueryHandler):
            raise QueryBusError(f"Bad handler type. Received: {type(handler)}")

    def check_message_type(self, message: Message):
        if not isinstance(message, Query):
            raise QueryBusError(f"Bad message type. Received: {type(message)}")
