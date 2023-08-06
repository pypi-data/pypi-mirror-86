from importlib.metadata import version, PackageNotFoundError

from . import sources, types
from .main import gbq, mysql, pickle, requests, mongodb

__all__ = ["gbq", "mysql", "requests", "mongodb", "pickle", "types", "sources"]

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
