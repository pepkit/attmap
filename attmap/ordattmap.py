""" Ordered attmap """

from collections import OrderedDict
import itertools
from .attmap import AttMap
from .helpers import get_logger, safedel_message

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["OrdAttMap"]


_LOGGER = get_logger(__name__)


class OrdAttMap(OrderedDict, AttMap):
    """ Insertion-ordered mapping with dot notation access """

    def __init__(self, entries=None):
        super(OrdAttMap, self).__init__(entries or {})

    def __iter__(self):
        return itertools.chain(
            super(OrdAttMap, self).__iter__(),
            filter(lambda k: not self._is_od_member(k), self.__dict__.keys()))

    def __reversed__(self):
        _LOGGER.warning("Reverse iteration as implemented may be inefficient")
        return iter(reversed(list(self.keys())))

    def __getitem__(self, item):
        try:
            return super(OrdAttMap, self).__getitem__(item)
        except KeyError:
            return AttMap.__getitem__(self, item)

    def __setitem__(self, key, value):
        super(OrdAttMap, self).__setitem__(key, self._finalize_value(value))

    def __delitem__(self, key):
        """ Make unmapped key deletion unexceptional. """
        try:
            super(OrdAttMap, self).__delitem__(key)
        except KeyError:
            _LOGGER.debug(safedel_message(key))

    def __eq__(self, other):
        return AttMap.__eq__(self, other) and \
               list(self.keys()) == list(other.keys())

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return AttMap.__repr__(self)

    def keys(self):
        return [k for k in self]

    def values(self):
        return [self[k] for k in self]

    def items(self):
        return [(k, self[k]) for k in self]

    def clear(self):
        raise NotImplementedError("Clearance isn't implemented for {}".
                                  format(self.__class__.__name__))

    __marker = object()

    def pop(self, key, default=__marker):
        try:
            return super(OrdAttMap, self).pop(key)
        except KeyError:
            try:
                return self.__dict__.pop(key)
            except KeyError:
                if default is self.__marker:
                    raise KeyError(key)
                return default

    def popitem(self, last=True):
        raise NotImplementedError("popitem isn't supported on a {}".
                                  format(self.__class__.__name__))

    @staticmethod
    def _is_od_member(name):
        return name.startswith("_OrderedDict")

    def _new_empty_basic_map(self):
        return OrderedDict()

    @property
    def _lower_type_bound(self):
        return OrdAttMap
