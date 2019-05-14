""" Package-scope definitions """

from .attmap import AttMap
from .attmap_echo import AttMapEcho
from .helpers import *
from .ordattmap import OrdAttMap
from .ordpathex_attmap import OrdPathExAttMap
from ._version import __version__

AttributeDict = AttMap
AttributeDictEcho = AttMapEcho

__all__ = ["AttMap", "AttMapEcho", "AttributeDict", "AttributeDictEcho",
           "OrdAttMap", "OrdPathExAttMap", "get_data_lines"]
