""" Package-scope definitions """

from .attmap import AttMap
from .attmap_echo import AttMapEcho
from ._version import __version__

AttributeDict = AttMap
AttributeDictEcho = AttMapEcho

__all__ = ["AttMap", "AttMapEcho", "AttributeDict", "AttributeDictEcho"]
