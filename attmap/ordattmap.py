""" Ordered attmap """

from collections import OrderedDict
from .attmap import AttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["OrdAttMap"]


class OrdAttMap(OrderedDict, AttMap):
    """ Insertion-ordered mapping with dot notation access """

    def __init__(self, entries=None):
        super(OrdAttMap, self).__init__(entries or {})

    def __setitem__(self, key, value):
        super(OrdAttMap, self).__setitem__(key, self._finalize_value(value))

    def __eq__(self, other):
        return AttMap.__eq__(self, other) and list(self.keys()) == list(other.keys())

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return AttMap.__repr__(self)

    def _new_empty_basic_map(self):
        return OrderedDict()

    @property
    def _lower_type_bound(self):
        return OrdAttMap
