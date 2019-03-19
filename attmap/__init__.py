""" Package-scope definitions """

from .attmap import AttMap
from .attmap_echo import AttMapEcho
from .pathex_attmap import PathExAttMap
from ._version import __version__

AttributeDict = AttMap
AttributeDictEcho = AttMapEcho

__all__ = ["AttMap", "AttMapEcho", "AttributeDict", "AttributeDictEcho",
           "PathExAttMap"]
