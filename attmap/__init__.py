""" Package-scope definitions """

from .attmap import AttMap
from .attmap_echo import AttMapEcho

AttributeDict = AttMap
AttributeDictEcho = AttMapEcho

__all__ = ["AttMap", "AttMapEcho", "AttributeDict", "AttributeDictEcho"]
