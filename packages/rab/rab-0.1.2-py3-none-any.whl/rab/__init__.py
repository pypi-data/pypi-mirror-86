# Standard Libraries
from importlib import metadata
from .utils.logging_utils import _configure_rab_loggers


_configure_rab_loggers(root_module_name=__name__)
__version__ = metadata.version(__package__)

__all__ = []
