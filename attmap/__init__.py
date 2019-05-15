""" Package-scope definitions """

from .attmap import AttMap
from .attmap_echo import AttMapEcho
from .helpers import *
from .ordattmap import OrdAttMap
from .pathex_attmap import PathExAttMap
from ._version import __version__

AttributeDict = AttMap
AttributeDictEcho = AttMapEcho

__all__ = ["AttMap", "AttMapEcho", "AttributeDict", "AttributeDictEcho",
           "OrdAttMap", "PathExAttMap", "get_data_lines"]
