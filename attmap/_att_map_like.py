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
            if self._omit_from_eq(k):
                _LOGGER.debug("Excluding from comparison: {}".format(k))
                continue
            try:
                if not self._cmp(v, other[k]):
                    return False
            except KeyError:
                return False
        return True

    @staticmethod
    def _cmp(a, b):
        def same_type(obj1, obj2, typenames=None):
            t1, t2 = str(obj1.__class__), str(obj2.__class__)
            return (t1 in typenames and t2 in typenames) if typenames else t1 == t2
        if same_type(a, b, ["<type 'numpy.ndarray'>",
                            "<class 'numpy.ndarray'>"]) or \
            same_type(a, b, ["<class 'pandas.core.series.Series'>"]):
            check = lambda x, y: (x == y).all()
        elif same_type(a, b, ["<class 'pandas.core.frame.DataFrame'>"]):
            check = lambda x, y: (x == y).all().all()
        else:
            check = lambda x, y: x == y
        try:
            return check(a, b)
        except ValueError:
            # ValueError arises if, e.g., the pair of Series have
            # have nonidentical labels.
            return False

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return iter([k for k in self.__dict__.keys()])

    def __len__(self):
        return sum(1 for _ in iter(self))

    def __repr__(self):
        return repr({k: v for k, v in self.__dict__.items()
                    if not self._omit_from_repr(k, self.__class__)})

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, repr(self))

    def add_entries(self, entries):
        """
        Update this instance with provided key-value pairs.

        :param Iterable[(object, object)] | Mapping | pandas.Series entries:
            collection of pairs of keys and values
        """
        if not entries:
            return
        # Permit mapping-likes and iterables/generators of pairs.
        if callable(entries):
            entries = entries()
        elif "pandas.core.series.Series" in type(entries).__bases__:
            entries = entries.to_dict()
        try:
            entries_iter = entries.items()
        except AttributeError:
            entries_iter = entries
        for k, v in entries_iter:
            if k not in self or not \
                    (isinstance(v, Mapping) and isinstance(self[k], AttMapLike)):
                self[k] = v
            else:
                self[k] = self[k].add_entries(v)
        return self

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

    def to_map(self):
        """
        Convert this instance to a dict.

        :return dict[str, object]:
        """
        def go(kvs, acc):
            try:
                h, t = kvs[0], kvs[1:]
            except IndexError:
                return acc
            k, v = h
            acc[k] = go(list(v.items()), {}) \
                if isinstance(v, Mapping) and not isinstance(v, dict) else v
            return go(t, acc)
        return go(list(self.items()), {})

    def _omit_from_eq(self, k):
        """
        Hook for exclusion of particular value from a representation

        :param hashable k: key to consider for omission
        :return bool: whether the given key k should be omitted from comparison
        """
        return False

    def _omit_from_repr(self, k, cls):
        """
        Hook for exclusion of particular value from a representation

        :param hashable k: key to consider for omission
        :param type cls: data type on which to base the exclusion
        :return bool: whether the given key k should be omitted from
            text representation
        """
        return False
