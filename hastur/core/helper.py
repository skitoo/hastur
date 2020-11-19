from typing import Any
from importlib import import_module


def fullname(obj: Any) -> str:
    module = obj.__class__.__module__
    return f"{module}.{obj.__class__.__name__}"


def class_(class_fullname: str) -> type:
    module_name, class_name = class_fullname.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, class_name)
