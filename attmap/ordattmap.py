""" Ordered attmap """

from collections import OrderedDict
from .attmap import AttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["OrdAttMap"]


class OrdAttMap(AttMap, OrderedDict):
    """ Insertion-ordered mapping with dot notation access """

    def __init__(self, entries=None):
        super(OrdAttMap, self).__init__()
        self.__dict__ = OrderedDict()
        self.add_entries(entries)

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        #OrderedDict.__setitem__(self, key, self._finalize_value(value))

    def __getitem__(self, item):
        # DEBUG
        print("self.__dict__: {}".format(self.__dict__))
        OrderedDict.__getitem__(self, item)

    #def __eq__(self, other):
    #    AttMap.__eq__(self, other) and list(self.keys()) == list(other.keys())

    def _new_empty_basic_map(self):
        return OrderedDict()

    @property
    def _lower_type_bound(self):
        return OrdAttMap
