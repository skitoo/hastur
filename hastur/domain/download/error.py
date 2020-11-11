from hastur.domain.shared_kernel.error import HasturErrorMessage


class UrlAlreadyRegistered(HasturErrorMessage):
    msg: str = "Url is already registered"
