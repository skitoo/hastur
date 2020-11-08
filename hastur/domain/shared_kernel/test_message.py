from unittest import TestCase
from unittest.mock import Mock
from dataclasses import dataclass
import pytest
from .message import (
    CommandBus,
    QueryBus,
    Command,
    Query,
    CommandHandler,
    QueryHandler,
    Presenter,
    CommandBusError,
    QueryBusError,
    MessageBusError,
)


@dataclass
class AddUrlCommand(Command):
    url: str


@dataclass
class FetchUrlQuery(Query):
    id_: str


class AddUrl(CommandHandler):
    def __init__(self, mock: Mock = None):
        self.mock = mock

    def execute(self, message: Command, presenter: Presenter):
        self.mock.execute(message, presenter)

    def message_type(self) -> type:
        return AddUrlCommand


class FetchUrl(QueryHandler):
    def __init__(self, mock: Mock = None):
        self.mock = mock

    def execute(self, message: Query, presenter: Presenter):
        self.mock.execute(message, presenter)

    def message_type(self) -> type:
        return FetchUrlQuery


class TestCommandBus(TestCase):
    def setUp(self):
        self.instance = CommandBus()
        self.mock = Mock()

    def test_register_handler_with_sucess(self):
        handler = AddUrl()
        self.instance.register_handler(handler)

    def test_register_handler_with_handler_already_registered(self):
        handler = AddUrl()
        self.instance.register_handler(handler)
        with pytest.raises(MessageBusError):
            self.instance.register_handler(handler)

    def test_register_handler_with_bad_handler_type(self):
        handler = FetchUrl()
        with pytest.raises(CommandBusError):
            self.instance.register_handler(handler)

    def test_execute_with_success(self):
        handler = AddUrl(self.mock)
        command = AddUrlCommand("toto.com")
        presenter = Mock()
        self.instance.register_handler(handler)

        self.instance.execute(command, presenter)

        self.mock.execute.assert_called_once_with(command, presenter)

    def test_execute_with_bad_command_type(self):
        handler = AddUrl(self.mock)
        command = FetchUrlQuery("toto.com")
        presenter = Mock()
        self.instance.register_handler(handler)

        with pytest.raises(CommandBusError):
            self.instance.execute(command, presenter)

        self.mock.execute.assert_not_called()

    def test_execute_with_unkown_command(self):
        command = AddUrlCommand("toto.com")
        presenter = Mock()

        with pytest.raises(MessageBusError):
            self.instance.execute(command, presenter)

        self.mock.execute.assert_not_called()


class TestQueryBus(TestCase):
    def setUp(self):
        self.instance = QueryBus()
        self.mock = Mock()

    def test_register_handler_with_sucess(self):
        handler = FetchUrl()
        self.instance.register_handler(handler)

    def test_register_handler_with_handler_already_registered(self):
        handler = FetchUrl()
        self.instance.register_handler(handler)
        with pytest.raises(MessageBusError):
            self.instance.register_handler(handler)

    def test_register_handler_with_bad_handler_type(self):
        handler = AddUrl()
        with pytest.raises(QueryBusError):
            self.instance.register_handler(handler)

    def test_execute_with_success(self):
        handler = FetchUrl(self.mock)
        query = FetchUrlQuery("toto.com")
        presenter = Mock()
        self.instance.register_handler(handler)

        self.instance.execute(query, presenter)

        self.mock.execute.assert_called_once_with(query, presenter)

    def test_execute_with_bad_command_type(self):
        handler = FetchUrl(self.mock)
        query = AddUrlCommand("toto.com")
        presenter = Mock()
        self.instance.register_handler(handler)

        with pytest.raises(QueryBusError):
            self.instance.execute(query, presenter)

        self.mock.execute.assert_not_called()

    def test_execute_with_unkown_command(self):
        query = FetchUrlQuery("toto.com")
        presenter = Mock()

        with pytest.raises(MessageBusError):
            self.instance.execute(query, presenter)

        self.mock.execute.assert_not_called()
