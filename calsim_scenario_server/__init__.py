from importlib.metadata import PackageNotFoundError, version

from .clients import LocalClient, RemoteClient
from .main import app
from .schemas import Assumption, NamedDatasetPath, Run, Scenario, Timeseries

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # pandss not installed, likely developer mode
    __version__ = None
