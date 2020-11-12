from hastur.core.error import HasturErrorMessage


class UrlAlreadyRegistered(HasturErrorMessage):
    msg: str = "Url is already registered"


class UnknownDownload(HasturErrorMessage):
    msg: str = "Download requested is unknown"
