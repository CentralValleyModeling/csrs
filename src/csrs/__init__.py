from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # csrs not installed, likely developer mode
    __version__ = None
from .clients import LocalClient, RemoteClient
from .schemas import Assumption, NamedPath, Run, Scenario, Timeseries
