""" Ordered attmap """

from collections import OrderedDict
from .attmap import AttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["OrdAttMap"]


class OrdAttMap(AttMap, OrderedDict):
    """ Insertion-ordered mapping with dot notation access """

    def __init__(self, entries=None):
        super(OrdAttMap, self).__init__(entries or {})

    def _new_empty_basic_map(self):
        return OrderedDict()

    @property
    def _lower_type_bound(self):
        return OrdAttMap
