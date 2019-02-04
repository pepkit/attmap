""" The trait defining a multi-access data object """

import abc
import sys
if sys.version_info < (3, 3):
    from collections import Mapping, MutableMapping
else:
    from collections.abc import Mapping, MutableMapping
from .helpers import get_logger

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


_LOGGER = get_logger(__name__)


class AttMapLike(MutableMapping):
    """ Base class for multi-access-mode data objects. """

    __metaclass__ = abc.ABCMeta

    def __init__(self, entries=None):
        """
        Create a new instance, optionally with initial key-value pairs.

        :param Mapping | Iterable[(Hashable, object)] entries: initial
            KV pairs to store
        """
        self.add_entries(entries)

    @abc.abstractmethod
    def __getattr__(self, item, default=None):
        pass

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        try:
            # Ability to return requested item name itself is delegated.
            return self.__getattr__(item)
        except AttributeError:
            # Requested item is unknown, but request was made via
            # __getitem__ syntax, not attribute-access syntax.
            raise KeyError(item)

    def __delitem__(self, item):
        try:
            del self.__dict__[item]
        except KeyError:
            _LOGGER.debug("No item {} to delete".format(item))

    def __eq__(self, other):
        # TODO: check for equality across classes?
        if not isinstance(other, Mapping):
            return False
        if len(self) != len(other):
            # Ensure we don't have to worry about other containing self.
            return False
        for k, v in self.items():
            try:
                if v != other[k]:
                    return False
            except KeyError:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return iter([k for k in self.__dict__.keys()])

    def __len__(self):
        return sum(1 for _ in iter(self))

    def __repr__(self):
        return repr({k: v for k, v in self.__dict__.items()})

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, repr(self))

    def add_entries(self, entries):
        """
        Update this instance with provided key-value pairs.

        :param Iterable[(object, object)] | Mapping | pandas.Series entries:
            collection of pairs of keys and values
        """
        from pandas import Series
        if not entries:
            return
        # Permit mapping-likes and iterables/generators of pairs.
        if callable(entries):
            entries = entries()
        elif isinstance(entries, Series):
            entries = entries.to_dict()
        try:
            entries_iter = entries.items()
        except AttributeError:
            entries_iter = entries
        # Assume we now have pairs; allow corner cases to fail hard here.
        for key, value in entries_iter:
            self.__setitem__(key, value)

    def is_null(self, item):
        """
        Conjunction of presence in underlying mapping and value being None

        :param object item: Key to check for presence and null value
        :return bool: True iff the item is present and has null value
        """
        return item in self and self[item] is None

    def non_null(self, item):
        """
        Conjunction of presence in underlying mapping and value not being None

        :param object item: Key to check for presence and non-null value
        :return bool: True iff the item is present and has non-null value
        """
        return item in self and self[item] is not None
